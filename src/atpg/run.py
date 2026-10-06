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
import os
import platform
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime

from atpg.circuit import Circuit
from atpg.fault_sim import (compact, coverage, detects, detects_cube, detects_unknown_state,
                            exhaustive_test, guaranteed_sequence_test, trace_rows)
from atpg.faults import Fault, all_faults, collapse, validate_fault

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


# Chi fallback sang vet can khi PODEM bao THUAT TOAN CHUA HO TRO (vd loai cong); moi loi khac
# (dau vao sai, loi noi bo cua PODEM) deu duoc nem ra, khong che giau bang ket qua vet can.
UNSUPPORTED_MARKERS = ("chưa hỗ trợ", "không được hỗ trợ", "chua ho tro", "khong duoc ho tro", "not supported")


def _is_unsupported(err):
    if isinstance(err, NotImplementedError):
        return True
    msg = str(err).lower()
    return any(m in msg for m in UNSUPPORTED_MARKERS)


def generate_test(c, fault, podem_fn, max_backtracks=1000, trace=False):
    """Sinh pattern cho `fault` (Fault hoac list/tuple Fault).
    - Kiem tra dau vao truoc (ValueError neu loi khong thuoc mach, nhanh khong ton tai, ...).
    - Dung PODEM cua P5 neu co; chi khi PODEM bao chua ho tro (vd loai cong) moi dung vet can
      tham chieu cho loi do, va ghi ro trong cot thuat toan va ghi chu bao cao.
    - Neu chua co podem.py thi dung vet can tham chieu (chi hop cho mach it dau vao)."""
    validate_fault(c, fault)
    if max_backtracks < 0:
        raise ValueError("max_backtracks phai >= 0")
    algo = "vet can (tham chieu)"
    if podem_fn is not None:
        arg = list(fault) if isinstance(fault, tuple) else fault   # podem nhan Fault hoac list[Fault]
        try:
            r = podem_fn(c, arg, max_backtracks=max_backtracks, trace=trace)
            return GenResult(fault, r.status, dict(r.pattern), r.backtracks, "PODEM",
                             list(getattr(r, "steps", [])))
        except (ValueError, NotImplementedError) as e:
            if not _is_unsupported(e):
                raise
            PODEM_ERRORS.add(str(e))
            algo = "vet can (PODEM chua ho tro)"
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


def _git_commit():
    """Commit ma nguon luc chay; ghi ro neu src/ hoac circuits/ con thay doi chua commit."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True,
                             text=True, timeout=5).stdout.strip()
        if not sha:
            return "khong xac dinh (khong co git)"
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "src", "circuits"], cwd=root,
                               capture_output=True, text=True, timeout=5).stdout.strip()
        return sha + (" + thay doi chua commit trong src/ hoac circuits/" if dirty else "")
    except Exception:
        return "khong xac dinh"


def meta_lines(args, base, extra=()):
    """Phan moi truong va tai lap dat dau bao cao Markdown."""
    cmd = "python -m atpg.run " + " ".join(getattr(args, "argv_used", []) or [])
    lines = ["## Moi truong va tai lap\n",
             f"- Lenh tai tao (tu goc repo, PYTHONPATH=src): `{cmd.strip()}`",
             f"- Python {platform.python_version()} ({platform.python_implementation()}), "
             f"{platform.system()} {platform.release()}",
             f"- Commit ma nguon: {_git_commit()}",
             f"- Thoi diem chay: {datetime.now().isoformat(timespec='seconds')}",
             f"- Thu tu PI trong cot pattern: {', '.join(base.inputs)}",
             *extra]
    return "\n".join(lines) + "\n"


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


def run_all(c, faults, n_before, n_after, args, podem_fn, notes=(), universe=None, base=None):
    """Chay moi loi trong `faults`. `universe` la toan bo loi goc cua mach (de bao coverage toan mach
    cua tap test sau nen); mac dinh bang `faults`."""
    universe = list(universe) if universe is not None else list(faults)
    base = base or c
    t_gen = 0.0
    t0 = time.perf_counter()
    results, rows = [], []
    for f in faults:
        t1 = time.perf_counter()
        r = generate_test(c, f, podem_fn, args.max_backtracks, False)
        t_gen += time.perf_counter() - t1
        v, x = verify(c, r, args.max_x)
        results.append(r)
        rows.append([label(f), r.status, cube_str(c, r.pattern), r.algo, r.backtracks, v, x])

    n = len(faults)
    dt = sum(1 for r in results if r.status == "DETECTED")
    ut = sum(1 for r in results if r.status == "UNTESTABLE")
    ab = sum(1 for r in results if r.status == "ABORTED")
    pats = [fill0(c, r.pattern) for r in results if r.status == "DETECTED"]
    kept = compact(c, pats, faults)
    cov = coverage(c, kept, faults)
    cov_all = coverage(c, kept, universe)
    t_all = time.perf_counter() - t0
    sai = sum(1 for r in rows if r[5].startswith("SAI"))
    x_bad = sum(1 for r in rows if r[6] == "khong")
    x_unp = sum(1 for r in rows if r[6].startswith("chua"))
    bt = [r.backtracks for r in results if isinstance(r.backtracks, int)]

    n_stem = sum(1 for f in universe if not isinstance(f, (list, tuple)) and f.branch_to is None)
    n_branch = len(universe) - n_stem
    if isinstance(n_after, str):
        scope = n_after.strip()
    elif n == len(universe):
        scope = f"Dang chay {n} loi goc, khong gop."
    else:
        scope = (f"Dang chay {n} loi dai dien sau gop tuong duong (tu {n_before} loi goc). "
                 f"Tap {n} loi dai dien nay KHAC tap {n_stem} loi stem, du hai so co the trung nhau.")
    text = [f"# Ket qua toan bo loi - {c.name}\n",
            meta_lines(args, base, [
                f"- Pham vi loi goc: {len(universe)} loi"
                + (f" = {n_stem} stem + {n_branch} nhanh" if n_branch or n_stem else ""),
                f"- {scope}",
                "- Pattern co X duoc dien 0 khi mo phong loi; cot \"Moi cach dien X\" la vet can moi cach dien "
                f"(toi da {args.max_x} bit X).",
                f"- Thoi gian sinh pattern: {t_gen:.4f} s (time.perf_counter, chi tinh bo sinh pattern); "
                f"ca kiem chung va nen: {t_all:.4f} s. So do phu thuoc may chay."])]
    for line in notes:
        text.append(line + "\n")
    if podem_error_note():
        text.append(podem_error_note() + "\n")
    s = c.stats()
    text.append(md_table(["PI", "PO", "cong", "DFF"], [[s["PI"], s["PO"], s["gates"], s["DFF"]]]) + "\n")
    if not isinstance(n_after, str):
        text.append(f"So loi truoc gop: {n_before}; sau gop (equivalence): {n_after}.\n")
    text.append("## Ket qua tung loi\n")
    text.append(md_table(["Loi", "Trang thai", "Pattern", "Thuat toan", "Backtrack", "Kiem chung",
                          "Moi cach dien X"], rows) + "\n")
    text.append("## Tong hop\n")
    text.append(md_table(["Chi so", "Gia tri"], [
        ["Fault coverage (DETECTED / tong)", f"{dt}/{n} = {pct(dt, n)}"],
        ["Test coverage (DETECTED / (tong - UNTESTABLE))", f"{dt}/{n - ut} = {pct(dt, n - ut)}"],
        ["Fault efficiency ((DETECTED + UNTESTABLE) / tong)", f"{dt + ut}/{n} = {pct(dt + ut, n)}"],
        ["ABORTED", ab],
        ["Backtrack trung binh", f"{sum(bt) / len(bt):.2f}" if bt else "-"],
        ["Pattern truoc nen", len(pats)],
        ["Pattern sau nen", f"{len(kept)} (phu {cov['detected']}/{n} loi dang chay)"],
        [f"Tap sau nen phu toan bo loi goc ({len(universe)} loi)",
         f"{cov_all['detected']}/{len(universe)} = {pct(cov_all['detected'], len(universe))}"],
        ["Pattern bi kiem chung SAI", sai],
        ["Pattern co X ma co cach dien X khong phat hien", x_bad],
        [f"Pattern chua kiem chung het moi cach dien X (>{args.max_x} bit X)", x_unp],
    ]) + "\n")
    text.append(f"## Tap test sau nen (X da dien 0; thu tu PI: {', '.join(c.inputs)})\n")
    text.append(md_table(["#", "Pattern"], [[i + 1, "".join(str(p[pi]) for pi in c.inputs)]
                                             for i, p in enumerate(kept)]))
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
    t0 = time.perf_counter()
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
                     r.algo, r.backtracks, scope])
    elapsed = time.perf_counter() - t0
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
            meta_lines(args, base, [
                f"- Pham vi loi: {n} loi stem vat ly, moi loi cay vao ca {k} khung",
                f"- Nguon pattern theo hang (cot Thuat toan): {', '.join(sorted({r.algo for r in results}))}",
                f"- Tong thoi gian (sinh + kiem chung bao dam): {elapsed:.4f} s (time.perf_counter). "
                "So do phu thuoc may chay."]),
            scope_line(base, k, n) + "\n",
            *([podem_error_note() + "\n"] if podem_error_note() else []),
            md_table(["PI moi khung", "PO moi khung", "cong moi khung", "DFF"],
                     [[len(base.inputs), len(base.outputs), len(base.topo_order), len(base.dffs)]]) + "\n",
            f"Pattern: moi nhom ky tu la cac PI ({', '.join(base.inputs)}) cua mot khung, theo thoi gian.\n",
            md_table(["Loi", "Trang thai", "Chuoi (PI moi khung)", "Thuat toan", "Backtrack", "Pham vi dam bao"],
                     rows) + "\n",
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
    return run_all(c, faults, n, f"Dang chay {n} loi stem vat ly, khong gop (moi loi cay vao ca {k} khung).",
                   args, podem_fn, notes, universe=faults, base=base)


def _int_at_least(lo, what):
    def conv(text):
        try:
            v = int(text)
        except ValueError:
            raise argparse.ArgumentTypeError(f"{what} phai la so nguyen, nhan {text!r}")
        if v < lo:
            raise argparse.ArgumentTypeError(f"{what} phai >= {lo}, nhan {v}")
        return v
    return conv


def _safe_console():
    """Console Windows cu (cp1252) khong in duoc tieng Viet trong trace PODEM: thay ky tu loi
    bang '?' thay vi dung chuong trinh. Muon luu ket qua day du hay dung --md (ghi UTF-8)."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(errors="replace")
            except Exception:
                pass


def main(argv=None):
    _safe_console()
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(prog="atpg.run", description="ATPG PODEM: sinh pattern, kiem chung, coverage")
    ap.add_argument("bench")
    ap.add_argument("--fault", nargs=2, metavar=("NET", "SV"), help="mot loi, vd: --fault 11 0 (SV la 0 hoac 1)")
    ap.add_argument("--branch", metavar="GATE", help="loi tren nhanh cua NET di vao cong GATE (chi mach to hop)")
    ap.add_argument("--all", action="store_true", help="chay moi loi, tinh coverage")
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--unroll", type=_int_at_least(1, "So khung K"), metavar="K",
                    help="trai K khung thoi gian (unroll.py cua P4), K >= 1")
    ap.add_argument("--init", choices=["unknown", "controllable"], default="unknown",
                    help="chi dung voi --unroll: trang thai dau chua biet (mac dinh) hoac dieu khien duoc")
    ap.add_argument("--no-collapse", action="store_true", help="khong gop loi tuong duong (mach to hop)")
    ap.add_argument("--pattern", help="chuoi 0/1/X theo thu tu INPUT: kiem tra pattern co phat hien loi")
    ap.add_argument("--max-backtracks", type=_int_at_least(0, "--max-backtracks"), default=1000)
    ap.add_argument("--max-x", type=_int_at_least(0, "--max-x"), default=16, metavar="N",
                    help="vet can moi cach dien X neu pattern co toi da N bit X (mac dinh 16)")
    ap.add_argument("--md", metavar="FILE", help="ghi bao cao Markdown UTF-8 (vd results/c17_all_faults.md)")
    args = ap.parse_args(argv)
    args.argv_used = argv

    if args.fault and args.fault[1] not in ("0", "1"):
        ap.error(f"SV phai la 0 hoac 1 (stuck-at-0/stuck-at-1), nhan {args.fault[1]!r}")
    if args.branch and not args.fault:
        ap.error("--branch can di kem --fault NET SV")
    if args.init != "unknown" and args.unroll is None:
        ap.error("--init chi dung cung --unroll")

    base = Circuit.from_bench(args.bench)
    if args.fault:
        net = args.fault[0]
        if net not in base.gates and net not in base.inputs:
            ap.error(f"Khong co net {net!r} trong mach {base.name}")
        if args.branch:
            g = base.gates.get(args.branch)
            if g is None or net not in g.inputs:
                ap.error(f"Nhanh {net}->{args.branch} khong ton tai: "
                         + (f"khong co cong {args.branch!r}" if g is None
                            else f"cong {args.branch} khong nhan net {net}"))
    if base.dffs and args.unroll is None:
        ap.error(f"Mach {base.name} co {len(base.dffs)} DFF: can --unroll K (hoac full_scan cua P4)")

    c = base
    expand = None
    if args.unroll is not None:
        if args.branch:
            ap.error("--branch chua ho tro khi --unroll: fault_in_frames cua P4 chi nhan loi stem "
                     "(loi nhanh can anh xa dung canh, dac biet canh vao DFF).")
        try:
            from atpg.unroll import fault_in_frames, unroll   # P4
        except ImportError:
            sys.exit("Chua co atpg/unroll.py cua P4 (can ham unroll va fault_in_frames).")
        c = unroll(base, args.unroll)
        expand = lambda f: tuple(fault_in_frames(f, args.unroll))   # tuple de lam khoa dict
        if args.no_collapse:
            print("(--no-collapse: che do tran khung luon khong gop loi)")

    s = c.stats()
    print(f"Mach {c.name}: {s['PI']} PI, {s['PO']} PO, {s['gates']} cong, {s['DFF']} DFF")
    podem_fn = _load_podem()
    if podem_fn is None:
        print("(Chua co atpg/podem.py cua P5 - dung vet can tham chieu thay PODEM)")
    state_nets = [f"{g.output}@0" for g in base.dffs]

    if args.fault:
        net, sv = args.fault[0], int(args.fault[1])
        if args.unroll is not None:
            fault = expand(Fault(net, sv))
            if args.init == "controllable":
                return run_single(c, fault, args, podem_fn)
            return run_seq_single(c, base, fault, args, podem_fn, state_nets)
        return run_single(c, Fault(net, sv, args.branch), args, podem_fn)
    if args.all:
        if args.unroll is not None:
            if args.init == "controllable":
                return run_seq_controllable(c, base, args.unroll, expand, args, podem_fn)
            return run_seq_all(c, base, args.unroll, expand, args, podem_fn, state_nets)
        base_faults = all_faults(base)
        used = base_faults if args.no_collapse else collapse(base, base_faults)
        return run_all(c, used, len(base_faults), len(collapse(base, base_faults)), args, podem_fn,
                       universe=base_faults, base=base)
    ap.error("can --fault NET SV hoac --all")


if __name__ == "__main__":
    sys.exit(main())
