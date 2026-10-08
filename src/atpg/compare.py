"""So sanh D-algorithm va PODEM tren CUNG mot loi (P6).

    python -m atpg.compare circuits/c17.bench --fault 11 0 --trace
    python -m atpg.compare circuits/backtrack_example.bench --fault t 0 --trace
    python -m atpg.compare circuits/c17.bench --all
    python -m atpg.compare circuits/c17.bench --fault 11 0 --md results/so_sanh_c17_11sa0.md --csv ... --tex ...

Moi pattern cua ca hai thuat toan deu duoc fault simulator doc lap (fault_sim.py) kiem chung.
"""
from __future__ import annotations

import argparse
import csv
import os
import platform
import statistics
import sys
import time
from datetime import datetime

from atpg import dalg as dalg_mod
from atpg.circuit import Circuit
from atpg.dalg import d_algorithm
from atpg.fault_sim import compact, coverage, detects, detects_cube, trace_rows
from atpg.faults import Fault, all_faults, collapse, validate_fault
from atpg.run import _git_commit, _int_at_least, _safe_console, md_table

ALGOS = ("D-algorithm", "PODEM")

# Ket qua chay tay da co trong repo, dung de doi chieu (cube theo thu tu PI cua mach).
HAND = {
    ("c17", "11/SA0"): {
        "D-algorithm": {"cube": "X100X", "decisions": 4, "backtracks": 0,
                        "src": "Chương 3 (P2), bảng chạy tay"},
        "PODEM": {"cube": "X10XX", "decisions": 2, "backtracks": 0,
                  "src": "results/golden_trace_c17_11sa0.md (P3)"},
    },
    ("backtrack_example", "t/SA0"): {
        "PODEM": {"cube": "01", "decisions": 2, "backtracks": 1,
                  "src": "results/golden_trace_backtrack.md (P3)"},
    },
}


# --------------------------------------------------------------------- chay
def _load_podem():
    try:
        from atpg import podem as podem_mod
        return podem_mod
    except ImportError:
        return None


def run_podem(c, fault, podem_mod, max_backtracks, trace):
    """Chay PODEM cua P5, dem so lan goi imply va so lan danh gia cong (boc tam thoi)."""
    counts = {"imply": 0, "eval": 0}
    orig_imply, orig_eval = podem_mod.imply, podem_mod.eval_gate

    def imply(*a, **k):
        counts["imply"] += 1
        return orig_imply(*a, **k)

    def eval_gate(*a, **k):
        counts["eval"] += 1
        return orig_eval(*a, **k)

    podem_mod.imply, podem_mod.eval_gate = imply, eval_gate
    try:
        r = podem_mod.podem(c, fault, max_backtracks=max_backtracks, trace=trace)
    finally:
        podem_mod.imply, podem_mod.eval_gate = orig_imply, orig_eval
    return r, counts


def podem_decisions(steps):
    """So lan PODEM chon gan mot PI moi qua backtrace (khong tinh lan dao gia tri khi quay lui)."""
    return sum(1 for s in steps if s.get("Objective (net, giá trị)") is not None)


def podem_pis(steps):
    out = []
    for s in steps:
        if s.get("Objective (net, giá trị)") is None:
            continue
        pi = s.get("Backtrace → PI")
        if pi and pi[0] not in out:
            out.append(pi[0])
    return out


def timed(fn, repeat):
    """Trung vi thoi gian (ms) cua `repeat` lan chay `fn` (time.perf_counter)."""
    ts = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        fn()
        ts.append((time.perf_counter() - t0) * 1000)
    return statistics.median(ts)


def cube_str(c, pattern):
    return "".join(pattern.get(i, "X") for i in c.inputs) if pattern else "-"


def verify(c, pattern, fault):
    """(kiem chung voi X=0, moi cach dien X, cac PO quan sat duoc khi X=0)."""
    if not pattern:
        return "-", "-", "-"
    vec = {i: (0 if pattern.get(i, "X") == "X" else int(pattern[i])) for i in c.inputs}
    ok = detects(c, vec, fault)
    allx = detects_cube(c, {i: pattern.get(i, "X") for i in c.inputs}, fault)
    rows = trace_rows(c, vec, fault)
    pos = [o for o in c.outputs if any(r[0] == o and r[3] in ("D", "D'") for r in rows)]
    return ("OK" if ok else "SAI"), {True: "có", False: "không", None: "chưa kiểm chứng hết"}[allx], \
        (", ".join(pos) if pos else "không")


def compare_one(c, fault, args, podem_mod, trace=False):
    """Chay hai thuat toan cho mot loi; tra ve dict so lieu cho tung thuat toan."""
    out = {}
    d = d_algorithm(c, fault, max_backtracks=args.max_backtracks, order=args.order, trace=trace)
    other = "first" if args.order == "last" else "last"
    d2 = d_algorithm(c, fault, max_backtracks=args.max_backtracks, order=other)
    other_text = (f"order={other}: {d2.status}, {cube_str(c, d2.pattern)}, "
                  f"{d2.decisions} quyết định, {d2.backtracks} quay lui")
    v = verify(c, d.pattern, fault)
    out["D-algorithm"] = {
        "status": d.status, "cube": cube_str(c, d.pattern), "pattern": d.pattern,
        "decisions": d.decisions, "backtracks": d.backtracks, "implications": d.implications,
        "gate_evals": d.gate_evals, "internal": list(d.internal_assigned),
        "decided_pis": [], "justifications": d.justifications, "steps": d.steps,
        "verify": v, "other_order": other_text,
        "time": timed(lambda: d_algorithm(c, fault, max_backtracks=args.max_backtracks,
                                          order=args.order), args.repeat) if args.repeat else None,
    }
    if podem_mod is None:
        out["PODEM"] = None
        return out
    p, cnt = run_podem(c, fault, podem_mod, args.max_backtracks, True)
    v = verify(c, dict(p.pattern), fault)
    out["PODEM"] = {
        "status": p.status, "cube": cube_str(c, dict(p.pattern)), "pattern": dict(p.pattern),
        "decisions": podem_decisions(p.steps), "backtracks": p.backtracks, "implications": cnt["imply"],
        "gate_evals": cnt["eval"], "internal": [], "decided_pis": podem_pis(p.steps),
        "justifications": 0, "steps": list(p.steps) if trace else [],
        "verify": v,
        "time": timed(lambda: podem_mod.podem(c, fault, max_backtracks=args.max_backtracks),
                      args.repeat) if args.repeat else None,
    }
    return out


# --------------------------------------------------------------------- bao cao
def _xbits(cube):
    return cube.count("X") if cube != "-" else "-"


def hand_text(c, fault, algo, r):
    ref = HAND.get((c.name, str(fault)), {}).get(algo)
    if ref is None:
        return "không có chạy tay để đối chiếu"
    same = (r["cube"] == ref["cube"] and r["decisions"] == ref["decisions"]
            and r["backtracks"] == ref["backtracks"])
    detail = f"{ref['cube']}, {ref['decisions']} quyết định, {ref['backtracks']} quay lui"
    return ("khớp" if same else "KHÔNG khớp") + f" ({ref['src']}: {detail})"


def criteria_rows(c, fault, res):
    """Bang tieu chi: (nhom, tieu chi, gia tri D-alg, gia tri PODEM, y nghia)."""
    d, p = res["D-algorithm"], res["PODEM"] or {}
    g = lambda r, k, default="-": r.get(k, default) if r else default
    rows = [
        ("A. Kết quả", "Trạng thái", d["status"], g(p, "status"),
         "DETECTED = tìm được pattern"),
        ("A. Kết quả", f"Test cube (thứ tự PI {', '.join(c.inputs)})", d["cube"], g(p, "cube"),
         "X = đầu vào tùy ý"),
        ("A. Kết quả", "Số bit X trong cube", _xbits(d["cube"]), _xbits(g(p, "cube")),
         "nhiều X hơn thì cube linh hoạt hơn, dễ nén tập test"),
        ("A. Kết quả", "Kiểm chứng bằng fault simulation (X điền 0)", d["verify"][0], g(p, "verify", "---")[0],
         "mô phỏng độc lập mạch tốt và mạch lỗi"),
        ("A. Kết quả", "Đúng với mọi cách điền X", d["verify"][1], g(p, "verify", "---")[1],
         "vét cạn mọi cách điền X"),
        ("A. Kết quả", "PO quan sát được lỗi (X điền 0)", d["verify"][2], g(p, "verify", "---")[2],
         "đầu ra có D/D'"),
        ("B. Quá trình tìm kiếm", "Nơi ra quyết định",
         "net nội bộ (cube của từng cổng)", "chỉ ở PI" if p else "-",
         "khác biệt cốt lõi giữa hai thuật toán"),
        ("B. Quá trình tìm kiếm", "Số quyết định (kể cả lần chọn thất bại)", d["decisions"], g(p, "decisions"),
         "D-alg: chọn PDCF/PDC/cover; PODEM: gán PI qua backtrace"),
        ("B. Quá trình tìm kiếm", "Net nội bộ được gán trực tiếp",
         f"{len(d['internal'])} ({', '.join(d['internal'])})" if d["internal"] else "0",
         "0" if p else "-", "PODEM chỉ gán PI, net nội bộ suy ra bằng mô phỏng"),
        ("B. Quá trình tìm kiếm", "PI được chọn trực tiếp", "-",
         ", ".join(g(p, "decided_pis", [])) or "-", ""),
        ("B. Quá trình tìm kiếm", "Số lần justify (J-frontier)", d["justifications"],
         "0 (không cần)" if p else "-", "PODEM không có bước justify riêng"),
        ("B. Quá trình tìm kiếm", "Số lần quay lui (backtrack)", d["backtracks"], g(p, "backtracks"),
         "phụ thuộc thứ tự thử, không phải thước đo tuyệt đối"),
        ("B. Quá trình tìm kiếm", "Nếu đổi thứ tự thử cube của D-algorithm", d["other_order"], "-",
         "cùng thuật toán, chỉ đổi thứ tự thử"),
        ("C. Chi phí tính toán", "Số lần gọi implication", d["implications"], g(p, "implications"),
         "D-alg: implication tiến + lùi; PODEM: mô phỏng tiến"),
        ("C. Chi phí tính toán", "Số lần đánh giá cổng", d["gate_evals"], g(p, "gate_evals"),
         "đếm trong code của từng thuật toán; chỉ so sánh tương đối"),
        ("C. Chi phí tính toán", "Thời gian (trung vị, ms)",
         "-" if d["time"] is None else f"{d['time']:.3f}",
         "-" if not p or p.get("time") is None else f"{p['time']:.3f}",
         "phụ thuộc máy chạy"),
        ("D. Đối chiếu", "Khớp chạy tay", hand_text(c, fault, "D-algorithm", d),
         hand_text(c, fault, "PODEM", p) if p else "-", ""),
    ]
    return rows


def dalg_trace_table(steps):
    rows = []
    for s in steps:
        known = ", ".join(f"{k}={v}" for k, v in s["Giá trị các net"].items() if v != "X")
        rows.append([s["Bước"], s["Loại"], s["Cổng"], s["Cube"], known or "-",
                     "{" + ", ".join(s["D-frontier"]) + "}", "{" + ", ".join(s["J-frontier"]) + "}",
                     s["Hành động"]])
    return md_table(["Bước", "Loại", "Cổng", "Cube", "Net đã biết sau implication", "D-frontier",
                     "J-frontier", "Hành động"], rows)


def podem_trace_table(steps):
    if not steps:
        return "(không có)"
    cols = list(steps[0].keys())
    return md_table(cols, [[s.get(k, "") for k in cols] for s in steps])


def env_lines(args, c, extra=()):
    cmd = "python -m atpg.compare " + " ".join(args.argv_used)
    return "\n".join([
        "## Môi trường và tái lập\n",
        f"- Lệnh tái tạo (từ gốc repo, PYTHONPATH=src): `{cmd}`",
        f"- Python {platform.python_version()}, {platform.system()} {platform.release()}",
        f"- Commit mã nguồn: {_git_commit()}",
        f"- Thời điểm chạy: {datetime.now().isoformat(timespec='seconds')}",
        f"- Thứ tự PI: {', '.join(c.inputs)}; D-algorithm thử cube theo thứ tự `{args.order}`, "
        "D-frontier ưu tiên cổng gần PO nhất",
        (f"- Thời gian: trung vị {args.repeat} lần chạy (time.perf_counter), phụ thuộc máy"
         if args.repeat else "- Không đo thời gian (--repeat 0)"),
        *extra]) + "\n"


def report_single(c, fault, res, args):
    rows = criteria_rows(c, fault, res)
    out = [f"# So sánh D-algorithm và PODEM — {c.name}, lỗi {fault}\n", env_lines(args, c)]
    if res["PODEM"] is None:
        out.append("> Chưa có `atpg/podem.py` (P5): chỉ có cột D-algorithm.\n")
    out.append("## Bảng tiêu chí\n")
    out.append(md_table(["Nhóm", "Tiêu chí", "D-algorithm", "PODEM", "Ý nghĩa"], rows) + "\n")
    if args.trace:
        out.append("## Trace D-algorithm\n")
        out.append(dalg_trace_table(res["D-algorithm"]["steps"]) + "\n")
        if res["PODEM"]:
            out.append("## Trace PODEM (P5)\n")
            out.append(podem_trace_table(res["PODEM"]["steps"]) + "\n")
    return "\n".join(out), rows


def report_all(c, faults, universe, args, podem_mod):
    per, data = [], {a: [] for a in ALGOS}
    t0 = time.perf_counter()
    for f in faults:
        res = compare_one(c, f, args, podem_mod)
        row = [str(f)]
        for a in ALGOS:
            r = res[a]
            data[a].append(r)
            row += ["-"] * 5 if r is None else [r["status"], r["cube"], r["decisions"], r["backtracks"],
                                                  r["verify"][0]]
        per.append(row)
    elapsed = time.perf_counter() - t0

    def summ(a):
        rs = [r for r in data[a] if r]
        if not rs:
            return ["-"] * 9
        det = [r for r in rs if r["status"] == "DETECTED"]
        pats = [{i: (0 if r["pattern"].get(i, "X") == "X" else int(r["pattern"][i])) for i in c.inputs}
                for r in det]
        kept = compact(c, pats, faults)
        cov_all = coverage(c, kept, universe)["detected"]
        n = len(rs)
        same_as_ref = sum(1 for r in rs if r["verify"][0] == "OK" and r["verify"][1] == "có")
        return [f"{len(det)}/{n}", sum(r["decisions"] for r in rs), f"{sum(r['decisions'] for r in rs) / n:.2f}",
                sum(r["backtracks"] for r in rs),
                sum(len(r["internal"]) for r in rs),
                f"{sum(_xbits(r['cube']) for r in det) / max(len(det), 1):.2f}",
                f"{same_as_ref}/{n}", f"{len(pats)} → {len(kept)} (phủ {cov_all}/{len(universe)} lỗi gốc)",
                f"{sum(r['implications'] for r in rs)}"]

    names = ["Phát hiện (DETECTED / tổng)", "Tổng số quyết định", "Quyết định trung bình mỗi lỗi",
             "Tổng số lần quay lui", "Tổng net nội bộ gán trực tiếp", "Số bit X trung bình mỗi cube",
             "Pattern đúng (X=0 và mọi cách điền X)", "Pattern trước → sau nén", "Tổng số lần implication"]
    sd, sp = summ("D-algorithm"), summ("PODEM")
    summary = [[n, a, b] for n, a, b in zip(names, sd, sp)]
    diff = sum(1 for r in per if r[2] != r[7])
    text = [f"# So sánh D-algorithm và PODEM — {c.name}, toàn bộ lỗi\n",
            env_lines(args, c, [f"- Phạm vi: {len(faults)} lỗi"
                                + (" đại diện sau gộp tương đương" if len(faults) != len(universe) else " gốc")
                                + f" (từ {len(universe)} lỗi gốc)",
                                f"- Tổng thời gian chạy cả hai thuật toán và kiểm chứng: {elapsed:.3f} s"]),
            "## Tổng hợp\n",
            md_table(["Tiêu chí", "D-algorithm", "PODEM"], summary) + "\n",
            f"Số lỗi hai thuật toán cho cube khác nhau: {diff}/{len(faults)} "
            "(khác cube vẫn có thể cùng đúng; cột kiểm chứng cho biết đúng hay sai).\n",
            "## Từng lỗi\n",
            md_table(["Lỗi", "D-alg: trạng thái", "D-alg: cube", "D-alg: quyết định", "D-alg: quay lui",
                      "D-alg: kiểm chứng", "PODEM: trạng thái", "PODEM: cube", "PODEM: quyết định",
                      "PODEM: quay lui", "PODEM: kiểm chứng"], per)]
    bad = sum(1 for r in per if "SAI" in (r[5], r[10]))
    return "\n".join(text), summary, bad


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:      # utf-8-sig: Excel doc dung dau
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def _tex(s):
    s = str(s)
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"),
                 ("{", r"\{"), ("}", r"\}"), ("→", r"$\rightarrow$"), ("D'", r"$\overline{D}$")):
        s = s.replace(a, b)
    return s


def write_tex(path, c, fault, rows):
    """Bang tabular (khong khai bao goi) de P1 \\input vao slide/bao cao."""
    keep = [r for r in rows if r[1] not in ("PI được chọn trực tiếp",)]
    lines = [f"% Sinh tu dong boi: python -m atpg.compare (P6). Mach {c.name}, loi {fault}.",
             r"\begin{tabular}{@{}lll@{}}", r"\toprule",
             r"Tiêu chí & D-algorithm & PODEM\\", r"\midrule"]
    group = None
    for g, name, a, b, _ in keep:
        if g != group:
            if group is not None:
                lines.append(r"\midrule")
            group = g
        if name == "Khớp chạy tay":
            a = "khớp" if str(a).startswith("khớp") else ("-" if str(a).startswith("không có") else "không khớp")
            b = "khớp" if str(b).startswith("khớp") else ("-" if str(b).startswith("không có") else "không khớp")
        if name.startswith("Test cube"):
            name = "Test cube"
        lines.append(f"{_tex(name)} & {_tex(a)} & {_tex(b)}\\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main(argv=None):
    _safe_console()
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(prog="atpg.compare",
                                 description="So sánh D-algorithm và PODEM trên cùng một lỗi")
    ap.add_argument("bench")
    ap.add_argument("--fault", nargs=2, metavar=("NET", "SV"), help="vd: --fault 11 0")
    ap.add_argument("--branch", metavar="GATE", help="lỗi trên nhánh của NET đi vào cổng GATE")
    ap.add_argument("--all", action="store_true", help="so sánh trên toàn bộ lỗi (sau gộp)")
    ap.add_argument("--no-collapse", action="store_true", help="với --all: dùng toàn bộ lỗi gốc")
    ap.add_argument("--trace", action="store_true", help="in trace từng bước của hai thuật toán")
    ap.add_argument("--order", choices=["last", "first"], default="last",
                    help="thứ tự D-algorithm thử cube (mặc định last: trùng chạy tay của P2)")
    ap.add_argument("--repeat", type=_int_at_least(0, "--repeat"), default=200,
                    help="số lần chạy để đo thời gian (0 = không đo)")
    ap.add_argument("--max-backtracks", type=_int_at_least(0, "--max-backtracks"), default=1000)
    ap.add_argument("--md", metavar="FILE", help="ghi báo cáo Markdown (UTF-8)")
    ap.add_argument("--csv", metavar="FILE", help="ghi bảng tiêu chí ra CSV (mở bằng Excel)")
    ap.add_argument("--tex", metavar="FILE", help="ghi bảng tiêu chí dạng LaTeX tabular")
    args = ap.parse_args(argv)
    args.argv_used = argv

    if args.fault and args.fault[1] not in ("0", "1"):
        ap.error(f"SV phai la 0 hoac 1, nhan {args.fault[1]!r}")
    if args.branch and not args.fault:
        ap.error("--branch can di kem --fault NET SV")
    c = Circuit.from_bench(args.bench)
    if c.dffs:
        ap.error(f"Mach {c.name} co DFF: so sanh chi chay tren mach to hop")
    podem_mod = _load_podem()

    if args.fault:
        net, sv = args.fault[0], int(args.fault[1])
        try:
            fault = Fault(net, sv, args.branch)
            validate_fault(c, fault)
        except ValueError as e:
            ap.error(str(e))
        if args.repeat:
            args.repeat = min(args.repeat, 2000)
        res = compare_one(c, fault, args, podem_mod, trace=True)
        text, rows = report_single(c, fault, res, args)
        print(text)
        if args.md:
            os.makedirs(os.path.dirname(args.md) or ".", exist_ok=True)
            with open(args.md, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
        if args.csv:
            write_csv(args.csv, ["Nhóm", "Tiêu chí", "D-algorithm", "PODEM", "Ý nghĩa"], rows)
        if args.tex:
            write_tex(args.tex, c, fault, rows)
        bad = any(r and r["verify"][0] == "SAI" for r in res.values())
        return 1 if bad else 0
    if args.all:
        if args.repeat:
            args.repeat = min(args.repeat, 20)
        universe = all_faults(c)
        faults = universe if args.no_collapse else collapse(c, universe)
        text, summary, bad = report_all(c, faults, universe, args, podem_mod)
        print(text)
        if args.md:
            os.makedirs(os.path.dirname(args.md) or ".", exist_ok=True)
            with open(args.md, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
        if args.csv:
            write_csv(args.csv, ["Tiêu chí", "D-algorithm", "PODEM"], summary)
        return 1 if bad else 0
    ap.error("can --fault NET SV hoac --all")


if __name__ == "__main__":
    sys.exit(main())
