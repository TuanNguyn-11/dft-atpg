"""Chuong trinh chinh (CLI) cua P6.

    python -m atpg.run circuits/c17.bench --fault 11 0 --trace     # 1 loi, in trace
    python -m atpg.run circuits/c17.bench --all                    # moi loi + coverage
    python -m atpg.run circuits/seq_example.bench --unroll 2 --all # mach tuan tu

Che do tran khung (--unroll K) mac dinh coi trang thai dau Q@0 la CHUA BIET (khong scan/reset):
chi pattern phat hien duoc voi moi trang thai dau moi duoc tinh la DETECTED. Dung
--init controllable neu Q@0 dieu khien duoc nho scan/reset (ket qua co dieu kien Q@0).
"""
from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass, field

from atpg.circuit import Circuit
from atpg.fault_sim import (compact, coverage, detects, detects_cube, detects_unknown_state,
                            exhaustive_test, guaranteed_sequence_test, trace_rows)
from atpg.faults import Fault, all_faults, collapse

MAX_BITS = 20          # gioi han so to hop khi chung minh phat hien voi trang thai dau chua biet


@dataclass
class GenResult:
    fault: object
    status: str                  # DETECTED | UNTESTABLE | ABORTED (che do tuan tu co them trang thai khac)
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


PODEM_ERRORS = set()    # thong bao loi PODEM da gap (de ghi vao bao cao)


def podem_error_note():
    if not PODEM_ERRORS:
        return ""
    return ("Luu y: PODEM cua P5 bao loi o mot so loi (" + "; ".join(sorted(PODEM_ERRORS))
            + "); cac loi do dung vet can tham chieu, cot thuat toan ghi ro.")


def generate_test(c, fault, podem_fn, max_backtracks=1000, trace=False):
    """Sinh pattern cho `fault` (Fault hoac list/tuple Fault). Dung PODEM cua P5 neu co,
    neu chua co (hoac PODEM bao loi, vd cong chua ho tro) thi dung vet can lam mau tham chieu
    (chi hop cho mach it dau vao); truong hop sau duoc ghi ro trong cot thuat toan."""
    algo = "vet can (tham chieu)"
    if podem_fn is not None:
        arg = list(fault) if isinstance(fault, tuple) else fault   # podem nhan Fault hoac list[Fault]
        try:
            r = podem_fn(c, arg, max_backtracks=max_backtracks, trace=trace)
            return GenResult(fault, r.status, dict(r.pattern), r.backtracks, "PODEM",
                             list(getattr(r, "steps", [])))
        except ValueError as e:              # vd "Backtrace chua ho tro loai cong: XOR"
            PODEM_ERRORS.add(str(e))
            algo = "vet can (PODEM khong chay duoc)"
    cube, exhausted = exhaustive_test(c, fault)
    if cube is not None:
        return GenResult(fault, "DETECTED", cube, "-", algo)
    return GenResult(fault, "UNTESTABLE" if exhausted else "ABORTED", {}, "-", algo)


def cube_str(c, cube):
    return "".join(str(cube.get(i, "X")) for i in c.inputs) if cube else "-"


def fill0(c, cube):
    return {i: (0 if cube.get(i, "X") in ("X", "x") else int(cube[i])) for i in c.inputs}


def x_text(v, max_x):
    """Dien giai ket qua tam-gia-tri cua detects_cube."""
    if v is True:
        return "co"
    if v is False:
        return "khong"
    return f"chua kiem chung het (>{max_x} bit X)"


def verify(c, res, max_x):
    """Kiem chung doc lap bang fault simulation. Tra ve (kiem chung, moi cach dien X)."""
    if res.status == "DETECTED":
        ok0 = detects(c, fill0(c, res.pattern), res.fault)
        okx = detects_cube(c, {i: res.pattern.get(i, "X") for i in c.inputs}, res.fault, max_x=max_x)
        return ("OK" if ok0 else "SAI"), x_text(okx, max_x)
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


def pct(a, b):
    return f"{100.0 * a / b:.1f}%" if b else "n/a"


def write_report(text, args):
    print(text)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"\nDa ghi {args.md}")


def parse_pattern(c, s):
    s = s.upper()
    if len(s) != len(c.inputs) or any(ch not in "01X" for ch in s):
        sys.exit(f"--pattern phai la chuoi {len(c.inputs)} ky tu 0/1/X theo thu tu INPUT: "
                 + ", ".join(c.inputs))
    return dict(zip(c.inputs, s))


def print_trace(c, res, fault, note=""):
    vec = fill0(c, res.pattern)
    print(f"\nTrace mo phong (X dien 0 -> {''.join(str(vec[i]) for i in c.inputs)}){note}")
    rows = trace_rows(c, vec, fault)
    print(md_table(["net", "mach tot", "mach loi", "gia tri 5"], rows))
    det = [o for o in c.outputs if any(r[0] == o and r[3] in ("D", "D'") for r in rows)]
    print("\nPhat hien tai PO:", ", ".join(det) if det else "KHONG")
    if res.steps:
        print("\nTrace PODEM (P5):")
        cols = list(res.steps[0].keys())
        print(md_table(cols, [[s.get(k, "") for k in cols] for s in res.steps]))


# ------------------------------------------------------------------ mach to hop
def run_single(c, fault, args, podem_fn):
    if args.pattern:
        cube = parse_pattern(c, args.pattern)
        res = GenResult(fault, "DETECTED", cube, "-", "pattern cho truoc")
        ok = detects_cube(c, cube, fault, max_x=args.max_x)
        verdict = {True: "PHAT HIEN voi moi cach dien X",
                   False: "KHONG phat hien voi moi cach dien X (co cach dien X khong phat hien)",
                   None: f"CHUA KIEM CHUNG HET (>{args.max_x} bit X, chua co phan vi du)"}[ok]
        print(f"Pattern {args.pattern.upper()} {label(fault)}: {verdict}")
    else:
        res = generate_test(c, fault, podem_fn, args.max_backtracks, args.trace)
        print(f"{label(fault)}: {res.status}, pattern {cube_str(c, res.pattern)}, "
              f"backtrack {res.backtracks} ({res.algo})")
        v, x = verify(c, res, args.max_x)
        print(f"Kiem chung bang fault simulation: {v}; moi cach dien X deu phat hien: {x}")
    if args.trace and res.pattern:
        print_trace(c, res, fault)
    return 0


def run_all(c, faults, n_before, n_after, args, podem_fn, notes=()):
    t0 = time.time()
    results, rows = [], []
    for f in faults:
        r = generate_test(c, f, podem_fn, args.max_backtracks, False)
        v, x = verify(c, r, args.max_x)
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
    x_bad = sum(1 for r in rows if r[5] == "khong")
    x_unp = sum(1 for r in rows if r[5].startswith("chua"))
    bt = [r.backtracks for r in results if isinstance(r.backtracks, int)]

    text = [f"# Ket qua toan bo loi - {c.name}\n"]
    algos = sorted({r.algo for r in results})
    text.append(f"Thuat toan sinh pattern: {', '.join(algos)}. "
                f"Tong thoi gian: {elapsed:.3f} s. Pattern co X duoc dien 0 khi mo phong loi.\n")
    for line in notes:
        text.append(line + "\n")
    if podem_error_note():
        text.append(podem_error_note() + "\n")
    s = c.stats()
    text.append(md_table(["PI", "PO", "cong", "DFF"], [[s["PI"], s["PO"], s["gates"], s["DFF"]]]) + "\n")
    text.append(n_after if isinstance(n_after, str) else
                f"So loi truoc gop: {n_before}; sau gop (equivalence): {n_after}.\n")
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
        ["Pattern co X ma co cach dien X khong phat hien", x_bad],
        [f"Pattern chua kiem chung het moi cach dien X (>{args.max_x} bit X)", x_unp],
    ]))
    write_report("\n".join(text), args)
    return 1 if (sai or x_bad) else 0


# ------------------------------------------------------------ mach da trai khung
def seq_generate(c, fault, podem_fn, state_nets, args):
    """Sinh pattern cho mach da trai khung, Q@0 chua biet. Tra ve (GenResult, loai) voi loai:
    'bao dam' | 'co dieu kien' | 'chua' | '-'. Q@0 trong pattern cua bo sinh bi coi la
    dau vao gia; pattern chi tinh DETECTED khi da chung minh dung voi moi trang thai dau."""
    r = generate_test(c, fault, podem_fn, args.max_backtracks, args.trace)
    if r.status == "UNTESTABLE":                 # khong tin mu quang: doi chieu bang vet can
        cube, _ = exhaustive_test(c, fault)
        if cube is not None:
            return GenResult(fault, "KIEM CHUNG SAI (UNTESTABLE nhung co pattern)", cube, r.backtracks, r.algo), "-"
    if r.status != "DETECTED":
        return r, "-"
    ctrl = {i: r.pattern.get(i, "X") for i in c.inputs if i not in state_nets}
    g = detects_unknown_state(c, ctrl, fault, state_nets, MAX_BITS)
    if g is True:
        r.pattern = ctrl
        return r, "bao dam"
    cube, _ = guaranteed_sequence_test(c, fault, state_nets)      # tim chuoi khong phu thuoc Q@0
    if cube is not None:
        return GenResult(fault, "DETECTED", cube, "-", "vet can chuoi (tham chieu)"), "bao dam"
    if g is False and detects(c, fill0(c, r.pattern), fault):
        return GenResult(fault, "CO DIEU KIEN Q@0", dict(r.pattern), r.backtracks, r.algo, r.steps), "co dieu kien"
    return GenResult(fault, "CHUA KIEM CHUNG HET", dict(r.pattern), r.backtracks, r.algo, r.steps), "chua"


def seq_str(c, cube, state_nets, show_state=False):
    """Moi nhom ky tu la cac PI (theo thu tu INPUT) cua mot khung, ngan cach bang dau phay."""
    frames = {}
    for i in c.inputs:
        if i in state_nets or "@" not in i:
            continue
        frames.setdefault(int(i.rsplit("@", 1)[1]), []).append(str(cube.get(i, "X")))
    s = ",".join("".join(frames[t]) for t in sorted(frames)) or "-"
    if show_state:
        s += " ; " + ",".join(f"{q}={cube.get(q, 'X')}" for q in state_nets)
    return s


def scope_line(base, k, n):
    return (f"Pham vi: {n} loi stem vat ly cua {base.name} (moi net 2 loi), moi loi duoc sao sang ca {k} khung; "
            f"khong gop loi (equivalence cua mach to hop khong mac nhien dung cho mach tuan tu), "
            f"khong co loi nhanh, mau so = {n}.")


def run_seq_single(c, base, fault, args, podem_fn, state_nets):
    if args.pattern:
        cube = parse_pattern(c, args.pattern)
        ctrl = {i: cube[i] for i in c.inputs if i not in state_nets}
        g = detects_unknown_state(c, ctrl, fault, state_nets, MAX_BITS)
        cond = detects_cube(c, cube, fault, max_x=args.max_x)
        print(f"Pattern {args.pattern.upper()} {label(fault)}:")
        print("  - Phat hien BAO DAM voi moi trang thai dau (bo qua Q@0 trong pattern): "
              + {True: "co", False: "khong", None: "chua kiem chung het"}[g])
        print("  - Phat hien co dieu kien (Q@0 dung nhu trong pattern, X dien moi cach): "
              + {True: "co", False: "khong", None: "chua kiem chung het"}[cond])
        res = GenResult(fault, "DETECTED", cube, "-", "pattern cho truoc")
    else:
        res, kind = seq_generate(c, fault, podem_fn, state_nets, args)
        shown = seq_str(c, res.pattern, state_nets, show_state=(kind == "co dieu kien")) if res.pattern else "-"
        print(f"{label(fault)}: {res.status}, chuoi (PI moi khung) {shown}, backtrack {res.backtracks} ({res.algo})")
        print({"bao dam": "Phat hien BAO DAM voi moi trang thai dau cua mach tot va mach loi.",
               "co dieu kien": "Chi phat hien neu trang thai dau dung nhu da ghi (Q@0); KHONG bao dam tu trang thai dau chua biet.",
               "chua": "Chua kiem chung het (qua nhieu to hop).",
               "-": "Khong tim thay pattern hoac bo sinh dung som."}[kind])
    if args.trace and res.pattern:
        print_trace(c, res, fault, " [Q@0 dien 0 chi de minh hoa, mach tot va mach loi cung trang thai dau]")
    return 0


def run_seq_all(c, base, k, expand, args, podem_fn, state_nets):
    faults = [Fault(n, sv) for n in base.nets for sv in (0, 1)]
    n = len(faults)
    t0 = time.time()
    rows, kinds, results = [], [], []
    for f in faults:
        r, kind = seq_generate(c, expand(f), podem_fn, state_nets, args)
        results.append(r)
        kinds.append(kind)
        show_state = kind in ("co dieu kien", "chua")
        scope = {"bao dam": "bao dam moi trang thai dau",
                 "co dieu kien": "chi khi Q@0 nhu ghi",
                 "chua": "chua chung minh",
                 "-": "-"}[kind]
        rows.append([label(f), r.status, seq_str(c, r.pattern, state_nets, show_state) if r.pattern else "-",
                     r.backtracks, scope])
    elapsed = time.time() - t0
    dt = sum(1 for r in results if r.status == "DETECTED")
    cond = sum(1 for r in results if r.status == "CO DIEU KIEN Q@0")
    unp = sum(1 for r in results if r.status == "CHUA KIEM CHUNG HET")
    ut = sum(1 for r in results if r.status == "UNTESTABLE")
    ab = sum(1 for r in results if r.status == "ABORTED")
    sai = sum(1 for r in results if r.status.startswith("KIEM CHUNG SAI"))
    s = c.stats()
    text = [f"# Ket qua mach tuan tu - {base.name}, trai {k} khung\n",
            "Che do: trang thai dau Q@0 CHUA BIET (khong scan/reset). `DETECTED` nghia la phat hien BAO DAM voi "
            "moi trang thai dau cua mach tot va mach loi (cung dinh nghia voi scripts/p4_seq_experiment.py); "
            "pattern chi con cac PI dieu khien duoc, Q@0 khong nam trong pattern.\n",
            f"Thuat toan sinh pattern: {', '.join(sorted({r.algo for r in results}))}. "
            f"Tong thoi gian: {elapsed:.3f} s.\n",
            scope_line(base, k, n) + "\n",
            *([podem_error_note() + "\n"] if podem_error_note() else []),
            md_table(["PI moi khung", "PO moi khung", "cong moi khung", "DFF"],
                     [[len(base.inputs), len(base.outputs), len(base.topo_order), len(base.dffs)]]) + "\n",
            f"Pattern: moi nhom ky tu la cac PI ({', '.join(base.inputs)}) cua mot khung, theo thoi gian.\n",
            md_table(["Loi", "Trang thai", "Chuoi (PI moi khung)", "Backtrack", "Pham vi dam bao"], rows) + "\n",
            md_table(["Chi so", "Gia tri"], [
                ["Phat hien BAO DAM (DETECTED / tong)", f"{dt}/{n} = {pct(dt, n)}"],
                ["Chi phat hien CO DIEU KIEN Q@0", cond],
                ["Coverage neu Q@0 dieu khien duoc (scan/reset): (DETECTED + co dieu kien) / tong",
                 f"{dt + cond}/{n} = {pct(dt + cond, n)}"],
                ["UNTESTABLE (ke ca khi Q@0 dieu khien duoc, trong gioi han khung)", ut],
                ["ABORTED", ab],
                ["Chua kiem chung het", unp],
                ["Ket luan UNTESTABLE bi kiem chung SAI (vet can tim ra pattern)", sai],
                ["Nen tap test", "khong ap dung o che do tran khung"],
            ])]
    write_report("\n".join(text), args)
    return 1 if sai else 0


def run_seq_controllable(c, base, k, expand, args, podem_fn):
    """Che do --init controllable: Q@0 coi nhu dieu khien duoc (scan/reset). Ket qua co dieu kien Q@0."""
    faults = [expand(Fault(n, sv)) for n in base.nets for sv in (0, 1)]
    n = len(faults)
    notes = ["CHE DO Q@0 DIEU KHIEN DUOC (scan/reset): pattern gom ca Q@0; ket qua CO DIEU KIEN, "
             "khong phai phat hien bao dam tu trang thai dau chua biet. " + scope_line(base, k, n)]
    return run_all(c, faults, n, f"So loi: {n} (stem vat ly, khong gop).\n", args, podem_fn, notes)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="atpg.run", description="ATPG PODEM: sinh pattern, kiem chung, coverage")
    ap.add_argument("bench")
    ap.add_argument("--fault", nargs=2, metavar=("NET", "SV"), help="mot loi, vd: --fault 11 0")
    ap.add_argument("--branch", metavar="GATE", help="loi tren nhanh cua NET di vao cong GATE (chi mach to hop)")
    ap.add_argument("--all", action="store_true", help="chay moi loi, tinh coverage")
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--unroll", type=int, metavar="K", help="trai K khung thoi gian (unroll.py cua P4)")
    ap.add_argument("--init", choices=["unknown", "controllable"], default="unknown",
                    help="chi dung voi --unroll: trang thai dau chua biet (mac dinh) hoac dieu khien duoc")
    ap.add_argument("--no-collapse", action="store_true", help="khong gop loi tuong duong (mach to hop)")
    ap.add_argument("--pattern", help="chuoi 0/1/X theo thu tu INPUT: kiem tra pattern co phat hien loi")
    ap.add_argument("--max-backtracks", type=int, default=1000)
    ap.add_argument("--max-x", type=int, default=16, metavar="N",
                    help="vet can moi cach dien X neu pattern co toi da N bit X (mac dinh 16)")
    ap.add_argument("--md", metavar="FILE", help="ghi bao cao Markdown (vd results/c17_all_faults.md)")
    args = ap.parse_args(argv)

    base = Circuit.from_bench(args.bench)
    c = base
    expand = None
    if args.unroll:
        if args.branch:
            sys.exit("--branch chua ho tro khi --unroll: fault_in_frames cua P4 chi nhan loi stem "
                     "(loi nhanh can anh xa dung canh, dac biet canh vao DFF).")
        try:
            from atpg.unroll import fault_in_frames, unroll   # P4
        except ImportError:
            sys.exit("Chua co atpg/unroll.py cua P4 (can ham unroll va fault_in_frames).")
        c = unroll(base, args.unroll)
        expand = lambda f: tuple(fault_in_frames(f, args.unroll))   # tuple de lam khoa dict
        if args.no_collapse:
            print("(--no-collapse: che do tran khung luon khong gop loi)")
    elif args.init != "unknown":
        ap.error("--init chi dung cung --unroll")

    s = c.stats()
    print(f"Mach {c.name}: {s['PI']} PI, {s['PO']} PO, {s['gates']} cong, {s['DFF']} DFF")
    podem_fn = _load_podem()
    if podem_fn is None:
        print("(Chua co atpg/podem.py cua P5 - dung vet can tham chieu thay PODEM)")
    state_nets = [f"{g.output}@0" for g in base.dffs]

    if args.fault:
        net, sv = args.fault[0], int(args.fault[1])
        if net not in base.nets:
            sys.exit(f"Khong co net {net} trong mach")
        if args.unroll:
            fault = expand(Fault(net, sv))
            if args.init == "controllable":
                return run_single(c, fault, args, podem_fn)
            return run_seq_single(c, base, fault, args, podem_fn, state_nets)
        return run_single(c, Fault(net, sv, args.branch), args, podem_fn)
    if args.all:
        if args.unroll:
            if args.init == "controllable":
                return run_seq_controllable(c, base, args.unroll, expand, args, podem_fn)
            return run_seq_all(c, base, args.unroll, expand, args, podem_fn, state_nets)
        base_faults = all_faults(base)
        used = base_faults if args.no_collapse else collapse(base, base_faults)
        return run_all(c, used, len(base_faults), len(collapse(base, base_faults)), args, podem_fn)
    ap.error("can --fault NET SV hoac --all")


if __name__ == "__main__":
    sys.exit(main())
