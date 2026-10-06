"""Kiểm chứng hợp đồng P3 bằng lõi P5, parser/simulator P6 và golden thật.

Chạy từ gốc repo: python -B notes/p3_doi_chieu_code.py
Không gọi implementation tham chiếu p3_kiem_chung, không sửa trace P5.
"""
from itertools import product
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from atpg.circuit import Circuit
from atpg.faults import Fault
from atpg.fault_sim import detects, simulate
from atpg.podem import podem
from scripts.export_podem_trace import COLUMNS, render_trace


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def table(text):
    header = "| " + " | ".join(COLUMNS) + " |"
    require(text.count(header) == 1, "Phải có một bảng trace đúng tiêu đề")
    text = text.split(header, 1)[1].strip().split("\n\n", 1)[0]
    rows = [[v.strip() for v in line.split("|")[1:-1]]
            for line in text.splitlines() if re.match(r"^\| \d+ \|", line)]
    require(rows and all(len(row) == 7 for row in rows), "Bảng phải đủ 7 cột")
    return rows


def pair(cell):
    if cell.startswith("—"):
        return None
    match = re.fullmatch(r"\((\w+),\s*([01])\)", cell)
    if not match:
        match = re.search(r"(\w+)=([01])$", cell)
    require(match is not None, f"Không đọc được objective/PI: {cell}")
    return match[1], int(match[2])


def normalized(row, circuit):
    values = dict(re.findall(r"(\w+)=(D'|D|X|0|1)(?=[,;\s]|$)", row[4]))
    pi = re.search(r"PI=\(([^)]+)\)", row[4])
    if pi:
        bits = pi[1].split(",")
        require(len(bits) == len(circuit.inputs), "Sai số PI")
        values.update(zip(circuit.inputs, bits))
    require(set(values) == set(circuit.nets), "Thiếu/thừa net trong bảng")
    frontier = [] if row[5] == "∅" else row[5].strip("{}").split(",")
    return [int(row[0]), pair(row[1]), pair(row[2]), row[3], values,
            frontier, row[6]]


def display(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True).replace("|", "\\|")


def main():
    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    lines = ["# Bằng chứng P3 đối chiếu code thật — 06/10/2026", "",
             f"- Checkout HEAD khi chạy: `{base}`.",
             f"- Python: `{platform.python_version()}`; lệnh: `python -B notes/p3_doi_chieu_code.py`.",
             "- Dùng Circuit.from_bench, podem(trace=True), simulate/detects và exporter thật.",
             "- PASS chỉ được ghi sau khi tất cả assertion đạt; không sửa golden hoặc trace P5.", ""]
    cases = [("c17", "11", "c17_11sa0", "X10XX", 0, 2),
             ("backtrack_example", "t", "backtrack", "01", 1, 3)]
    for name, net, suffix, pattern, backtracks, count in cases:
        circuit = Circuit.from_bench(str(ROOT / "circuits" / f"{name}.bench"))
        fault = Fault(net, 0)
        result = podem(circuit, fault, max_backtracks=1, trace=True)
        require((result.status, ''.join(result.pattern[i] for i in circuit.inputs), result.backtracks)
                == ("DETECTED", pattern, backtracks), f"Sai kết quả {name}")
        golden = table((ROOT / "results" / f"golden_trace_{suffix}.md").read_text(encoding="utf-8"))
        stored = (ROOT / "results" / f"trace_{suffix}.md").read_text(encoding="utf-8")
        require(render_trace(circuit, result) == stored, f"Trace P5 không tái lập: {name}")
        exported = table(stored)
        require(len(result.steps) == len(golden) == len(exported) == count, "Sai số hàng")
        lines += [f"## {name}, {net}/SA0", "",
                  f"PASS: DETECTED, pattern `{pattern}`, backtracks={backtracks}; file P5 tái sinh trùng nội dung.", "",
                  "| Hàng | Cột | Golden sau chuẩn hóa | API thực tế | File P5 sau chuẩn hóa | Đánh giá |",
                  "|---|---|---|---|---|---|"]
        for index, (g, e, step) in enumerate(zip(golden, exported, result.steps)):
            require(set(step) == set(COLUMNS), "API phải đủ đúng 7 key")
            expected, actual_export = normalized(g, circuit), normalized(e, circuit)
            require(expected == actual_export, f"Exporter khác golden: {name} hàng {index+1}")
            actual = [step[key] for key in COLUMNS]
            for col, (want, got, out) in enumerate(zip(expected, actual, actual_export)):
                action_difference = name == "backtrack_example" and index < 2 and col == 6
                if action_difference:
                    require((want, got) == [("backtrack", "tiếp tục"), ("tiếp tục", "backtrack")][index],
                            "Khác biệt nhãn hành động đã thay đổi, cần review")
                else:
                    require(want == got, f"{name} hàng {index+1}, cột {COLUMNS[col]}: {want} != {got}")
                verdict = "Khác ngữ nghĩa API; exporter khớp" if action_difference else "Khớp giá trị"
                lines.append(f"| {index+1} | {COLUMNS[col]} | {display(want)} | {display(got)} | {display(out)} | {verdict} |")
        positions = [i for i in circuit.inputs if result.pattern[i] == "X"]
        found = 0
        for bits in product((0, 1), repeat=len(positions)):
            vector = {i: int(v) for i, v in result.pattern.items() if v != "X"}
            vector.update(zip(positions, bits))
            require(detects(circuit, vector, fault), f"P6 không phát hiện {vector}")
            found += 1
        zero = {i: int(result.pattern[i].replace("X", "0")) for i in circuit.inputs}
        good, bad = simulate(circuit, zero), simulate(circuit, zero, fault)
        good_po, bad_po = tuple(good[i] for i in circuit.outputs), tuple(bad[i] for i in circuit.outputs)
        require((good_po, bad_po) == (((1, 1), (0, 0)) if name == "c17" else ((1,), (0,))), "Sai PO")
        lines += ["", f"Simulator P6: {found}/{2**len(positions)} cách điền X phát hiện; điền X=0: PO tốt {good_po}, lỗi {bad_po}.", ""]
        if name == "backtrack_example":
            aborted = podem(circuit, fault, max_backtracks=0, trace=True)
            require((aborted.status, aborted.pattern, aborted.backtracks) ==
                    ("ABORTED", {"a": "1", "b": "X"}, 0), "Sai giới hạn 0")
            require(len(aborted.steps) == 2, "Sai số hàng API ABORTED")
            require(aborted.steps[0] == result.steps[0], "ABORTED phải thử đường đầu tiên")
            final = aborted.steps[-1]
            require(final == dict(zip(COLUMNS, [2, None, None, None,
                    result.steps[0][COLUMNS[4]], [], "thất bại"])), "Sai hàng dừng giới hạn")
            abort_rows = table(render_trace(circuit, aborted))
            require(len(abort_rows) == 1 and abort_rows[0][-1] == "backtrack", "Sai exporter ABORTED")
            lines += ["Giới hạn 0: ABORTED, pattern 1X, backtracks=0; API có hàng kết thúc không gán PI,",
                      "exporter gộp vào kết luận và giữ một hàng gán với hành động backtrack (bị chặn).",
                      "Giới hạn 1: DETECTED, pattern 01, backtracks=1. Không coi nhãn thất bại của hàng cuối API là UNTESTABLE.", ""]
    lines += ["## Phạm vi", "", "35 ô (5 hàng × 7 cột) được so giữa golden/API/file P5, bao gồm đầy đủ PI/net và thứ tự frontier.",
              "Chuẩn hóa cách viết tuple/đường backtrace và PI nhóm; hai khác biệt hành động API được kiểm tra tường minh.",
              "Không chứng minh mọi mạch/lỗi hoặc mọi heuristic bằng hai ví dụ này."]
    output = ROOT / "results" / "p3_doi_chieu_code.md"
    output.write_text('\n'.join(lines) + '\n', encoding="utf-8")
    print("PASS: 35 ô golden/API/export; c17 8/8 completions; P6 PO; giới hạn 0/1. " + str(output))


if __name__ == "__main__":
    main()
