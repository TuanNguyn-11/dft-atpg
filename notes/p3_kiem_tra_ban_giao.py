"""Đối chiếu file bàn giao với tham chiếu P3; chỉ thư viện chuẩn."""
from pathlib import Path
import re
import p3_kiem_chung as reference

ROOT = Path(__file__).resolve().parents[1]


def bench(path):
    inputs, outputs, gates, kinds = [], [], {}, {}
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r"(INPUT|OUTPUT)\((\w+)\)", line)
        if match:
            (inputs if match[1] == "INPUT" else outputs).append(match[2])
            continue
        match = re.fullmatch(r"(\w+)\s*=\s*(\w+)\(([^)]+)\)", line)
        assert match, line
        gates[match[1]] = [value.strip() for value in match[3].split(",")]
        kinds[match[1]] = match[2]
    return inputs, outputs, gates, kinds


def check_trace(path, fault):
    rows = [[cell.strip() for cell in line.split("|")[1:-1]]
            for line in path.read_text(encoding="utf-8").splitlines()
            if re.match(r"^\| [1-9]\d* \|", line) and len(line.split("|")) == 9]
    success, pattern, backtracks, expected = reference.run(fault)
    assert success and len(rows) == len(expected)
    for number, (cells, row) in enumerate(zip(rows, expected), 1):
        assert len(cells) == 7 and cells[0] == str(number), cells
        if row["flip"]:
            assert cells[1] == "— (đảo quyết định trước)" and cells[2] == "—"
        else:
            assert cells[1].replace(" ", "") == f"({row['obj'][0]},{row['obj'][1]})"
            assert cells[2].endswith(f"{row['pi']}={row['value']}")
        assert cells[3] == f"{row['pi']}={row['value']}"
        actual = dict(re.findall(r"(\w+)=(D'|[01XD])", cells[4]))
        expected_nets = {net: row["v"][net] for net in reference.G}
        assert {net: actual[net] for net in reference.G} == expected_nets
        if "PI=(" in cells[4]:
            values = re.search(r"PI=\(([^)]+)\)", cells[4])[1].split(",")
            assert values == [row["v"][pi] for pi in reference.PI]
        else:
            assert [actual[pi] for pi in reference.PI] == [row["v"][pi] for pi in reference.PI]
        frontier = [] if cells[5] == "∅" else cells[5].strip("{}").replace(" ", "").split(",")
        assert frontier == row["front"]
        action = {"fail": "backtrack", "continue": "tiếp tục", "success": "thành công"}[row["state"]]
        assert cells[6] == action
    print(f"PASS: {path.name}: {len(rows)} rows, pattern={''.join(pattern[p] for p in reference.PI)}, backtracks={backtracks}")


if __name__ == "__main__":
    c17 = ROOT / "circuits/c17.bench"
    if c17.exists():
        assert bench(c17) == (reference.PI, reference.PO, reference.G, reference.TYPES)
        print("PASS: c17.bench agrees with specification")
    else:
        print("PENDING: circuits/c17.bench (P6); c17 reference uses the published group specification")
    check_trace(ROOT / "results/golden_trace_c17_11sa0.md", ("11", 0))
    aux = bench(ROOT / "circuits/backtrack_example.bench")
    assert aux == (["a", "b"], ["out"], {"t": ["a", "b"], "n": ["a"], "out": ["t", "n"]},
                   {"t": "OR", "n": "NOT", "out": "AND"})
    reference.PI, reference.PO, reference.G, reference.TYPES = aux
    check_trace(ROOT / "results/golden_trace_backtrack.md", ("t", 0))
    chapter = (ROOT / "report/chapters/04_podem.tex").read_text(encoding="utf-8")
    assert chapter.startswith(r"\chapter{")
    assert not re.search(r"\\(?:usepackage|newcommand|renewcommand)\b", chapter)
    sources = [chapter] + [p.read_text(encoding="utf-8") for p in (ROOT / "report/figures/p3").glob("*.tex")]
    assert all(re.match(r"(?:sec|fig|tab|eq):p3-", label) for source in sources
               for label in re.findall(r"\\label\{([^}]+)\}", source))
    bib = (ROOT / "report/bib/p3.bib").read_text(encoding="utf-8")
    keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    assert keys and all(key.startswith("p3_") for key in keys)
    # P1 gộp sách Wang 2006 về khóa chung p1_wang2006 để tránh trùng mục tài liệu.
    shared = set(re.findall(r"@\w+\{([^,]+),", (ROOT / "report/bib/p1.bib").read_text(encoding="utf-8")))
    assert all(key in keys | shared for cite in re.findall(r"\\cite\{([^}]+)\}", chapter) for key in cite.split(","))
    slides = (ROOT / "slides/parts/p3.tex").read_text(encoding="utf-8")
    assert 2 <= slides.count(r"\begin{frame}") == slides.count(r"\end{frame}") <= 3
    print("PASS: auxiliary netlist, P3 labels/citations/chapter and 3 slide frames")
