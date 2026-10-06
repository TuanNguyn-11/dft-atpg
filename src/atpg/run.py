"""Chuong trinh chinh (CLI) cua P6.

    python -m atpg.run circuits/c17.bench --fault 11 0 --trace     # 1 loi, in trace
    python -m atpg.run circuits/c17.bench --all                    # moi loi + coverage
    python -m atpg.run circuits/seq_example.bench --unroll 2 --all # mach tuan tu
"""
from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass, field

from atpg.circuit import Circuit
from atpg.fault_sim import (compact, coverage, detects, detects_cube, exhaustive_test,
                            trace_rows)
from atpg.faults import Fault, all_faults, collapse


@dataclass
class GenResult:
    fault: object
    status: str                  # DETECTED | UNTESTABLE | ABORTED
    pattern: dict                # PI -> "0"/"1"/"X"
    backtracks: object           # so nguyen hoac "-"
    algo: str
    steps: list = field(default_factory=list)


def _load_podem():
    try:
        from atpg.podem import podem          # P5
        return podem
    except ImportError:
        return None


def generate_test(c, fault, podem_fn, max_backtracks=1000, trace=False):
    """Sinh pattern cho `fault` (Fault hoac list[Fault]). Dung PODEM cua P5 neu co,
    neu chua co thi dung vet can lam mau tham chieu (chi hop cho mach it dau vao)."""
    if podem_fn is not None:
        arg = list(fault) if isinstance(fault, tuple) else fault   # podem nhan Fault hoac list[Fault]
        r = podem_fn(c, arg, max_backtracks=max_backtracks, trace=trace)
        return GenResult(fault, r.status, dict(r.pattern), r.backtracks, "PODEM",
                         list(getattr(r, "steps", [])))
    cube, exhausted = exhaustive_test(c, fault)
    if cube is not None:
        return GenResult(fault, "DETECTED", cube, "-", "vet can (tham chieu)")
    return GenResult(fault, "UNTESTABLE" if exhausted else "ABORTED", {}, "-", "vet can (tham chieu)")


def cube_str(c, cube):
    return "".join(str(cube.get(i, "X")) for i in c.inputs) if cube else "-"


def fill0(c, cube):
    return {i: (0 if cube.get(i, "X") in ("X", "x") else int(cube[i])) for i in c.inputs}


def verify(c, res):
    """Kiem chung doc lap bang fault simulation. Tra ve (kiem chung, X-an-toan)."""
    if res.status == "DETECTED":
        ok0 = detects(c, fill0(c, res.pattern), res.fault)
        okx = detects_cube(c, {i: res.pattern.get(i, "X") for i in c.inputs}, res.fault)
        return ("OK" if ok0 else "SAI"), ("co" if okx else "khong")
    if res.status == "UNTESTABLE":
        cube, exhausted = exhaustive_test(c, res.fault)
        if not exhausted:
            return "-", "-"
        return ("SAI (co pattern)" if cube is not None else "OK (vet can)"), "-"
    return "-", "-"


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(x) for x in r) + " |" for r in rows]
    return "\n".join(out)


def label(f):
    """Nhan loi ngan gon: neu la list (mach da trai khung) thi lay loi dau, bo hau to @t."""
    f0 = f[0] if isinstance(f, (list, tuple)) else f
    base = Fault(f0.net.split("@")[0], f0.stuck_at,
                 None if f0.branch_to is None else f0.branch_to.split("@")[0])
    return str(base)


def run_single(c, fault, args, podem_fn):
    if args.pattern:
        cube = dict(zip(c.inputs, args.pattern.upper()))
        res = GenResult(fault, "DETECTED", cube, "-", "pattern cho truoc")
        ok = detects_cube(c, cube, fault)
        print(f"Pattern {args.pattern} {'PHAT HIEN' if ok else 'KHONG chac chan phat hien'} "
              f"{label(fault)} (X dien 0 hoac 1 deu xet)")
    else:
        res = generate_test(c, fault, podem_fn, args.max_backtracks, args.trace)
        print(f"{label(fault)}: {res.status}, pattern {cube_str(c, res.pattern)}, "
              f"backtrack {res.backtracks} ({res.algo})")
        v, x = verify(c, res)
        print(f"Kiem chung bang fault simulation: {v}; moi cach dien X deu phat hien: {x}")
    if args.trace and res.pattern:
        vec = fill0(c, res.pattern)
        print(f"\nTrace mo phong (X dien 0 -> {''.join(str(vec[i]) for i in c.inputs)})")
        print(md_table(["net", "mach tot", "mach loi", "gia tri 5"],
                       trace_rows(c, vec, fault)))
        rows = trace_rows(c, vec, fault)
        det = [o for o in c.outputs if any(r[0] == o and r[3] in ("D", "D'") for r in rows)]
        print("\nPhat hien tai PO:", ", ".join(det) if det else "KHONG")
        if res.steps:
            print("\nTrace PODEM (P5):")
            cols = list(res.steps[0].keys())
            print(md_table(cols, [[s.get(k, "") for k in cols] for s in res.steps]))
    return 0


def run_all(c, faults, base_faults, collapsed, args, podem_fn):
    t0 = time.time()
    results, rows = [], []
    for f in faults:
        r = generate_test(c, f, podem_fn, args.max_backtracks, False)
        v, x = verify(c, r)
        results.append(r)
        rows.append([label(f), r.status, cube_str(c, r.pattern), r.backtracks, v, x])
    elapsed = time.time() - t0

    n = len(faults)
    dt = sum(1 for r in results if r.status == "DETECTED")
    ut = sum(1 for r in results if r.status == "UNTESTABLE")
    ab = sum(1 for r in results if r.status == "ABORTED")
    pats = [fill0(c, r.pattern) for r in results if r.status == "DETECTED"]
    kept = compact(c, pats, faults)
    cov = coverage(c, kept, faults)
    sai = sum(1 for r in rows if r[4].startswith("SAI"))
    bt = [r.backtracks for r in results if isinstance(r.backtracks, int)]

    pct = lambda a, b: f"{100.0 * a / b:.1f}%" if b else "n/a"
    text = []
    text.append(f"# Ket qua toan bo loi - {c.name}\n")
    algos = sorted({r.algo for r in results})
    text.append(f"Thuat toan sinh pattern: {', '.join(algos)}. "
                f"Tong thoi gian: {elapsed:.3f} s. Pattern co X duoc dien 0 khi mo phong loi.\n")
    s = c.stats()
    text.append(md_table(["PI", "PO", "cong", "DFF"], [[s["PI"], s["PO"], s["gates"], s["DFF"]]]) + "\n")
    text.append(f"So loi truoc gop: {len(base_faults)}; sau gop (equivalence): {len(collapsed)}"
                f"{' (dung ' + str(n) + ' loi)' if args.no_collapse else ''}.\n")
    text.append(md_table(["Loi", "Trang thai", "Pattern", "Backtrack", "Kiem chung", "Moi cach dien X"], rows) + "\n")
    text.append(md_table(["Chi so", "Gia tri"], [
        ["Fault coverage (DETECTED / tong)", f"{dt}/{n} = {pct(dt, n)}"],
        ["Test coverage (DETECTED / (tong - UNTESTABLE))", f"{dt}/{n - ut} = {pct(dt, n - ut)}"],
        ["Fault efficiency ((DETECTED + UNTESTABLE) / tong)", f"{dt + ut}/{n} = {pct(dt + ut, n)}"],
        ["ABORTED", ab],
        ["Backtrack trung binh", f"{sum(bt) / len(bt):.2f}" if bt else "-"],
        ["Pattern truoc nen", len(pats)],
        ["Pattern sau nen", f"{len(kept)} (phu {cov['detected']}/{n} loi)"],
        ["Pattern bi kiem chung SAI", sai],
    ]))
    out = "\n".join(text)
    print(out)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
        print(f"\nDa ghi {args.md}")
    return 1 if sai else 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="atpg.run", description="ATPG PODEM: sinh pattern, kiem chung, coverage")
    ap.add_argument("bench")
    ap.add_argument("--fault", nargs=2, metavar=("NET", "SV"), help="mot loi, vd: --fault 11 0")
    ap.add_argument("--branch", metavar="GATE", help="loi tren nhanh cua NET di vao cong GATE")
    ap.add_argument("--all", action="store_true", help="chay moi loi, tinh coverage")
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--unroll", type=int, metavar="K", help="trai K khung thoi gian (unroll.py cua P4)")
    ap.add_argument("--no-collapse", action="store_true", help="khong gop loi tuong duong")
    ap.add_argument("--pattern", help="chuoi 0/1/X theo thu tu INPUT: kiem tra pattern co phat hien loi")
    ap.add_argument("--max-backtracks", type=int, default=1000)
    ap.add_argument("--md", metavar="FILE", help="ghi bao cao Markdown (vd results/c17_all_faults.md)")
    args = ap.parse_args(argv)

    base = Circuit.from_bench(args.bench)
    c = base
    expand = lambda f: f
    if args.unroll:
        try:
            from atpg.unroll import fault_in_frames, unroll   # P4
        except ImportError:
            sys.exit("Chua co atpg/unroll.py cua P4 (can ham unroll va fault_in_frames).")
        c = unroll(base, args.unroll)
        expand = lambda f: tuple(fault_in_frames(f, args.unroll))   # tuple de lam khoa dict

    s = c.stats()
    print(f"Mach {c.name}: {s['PI']} PI, {s['PO']} PO, {s['gates']} cong, {s['DFF']} DFF")
    podem_fn = _load_podem()
    if podem_fn is None:
        print("(Chua co atpg/podem.py cua P5 - dung vet can tham chieu thay PODEM)")

    if args.fault:
        net, sv = args.fault[0], int(args.fault[1])
        if net not in base.nets:
            sys.exit(f"Khong co net {net} trong mach")
        return run_single(c, expand(Fault(net, sv, args.branch)), args, podem_fn)
    if args.all:
        base_faults = all_faults(base)
        used = base_faults if args.no_collapse else collapse(base, base_faults)
        return run_all(c, [expand(f) for f in used], base_faults,
                       collapse(base, base_faults), args, podem_fn)
    ap.error("can --fault NET SV hoac --all")


if __name__ == "__main__":
    sys.exit(main())
