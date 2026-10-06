"""Mo phong mach, mo phong loi stuck-at, coverage, fault dropping va nen tap test (P6).
Chi dung thu vien chuan. Giao dien theo muc 8 cua prompt.md.
Quy uoc: pattern co "X" thi thay X bang 0 truoc khi mo phong (ghi ro trong bao cao)."""
from __future__ import annotations

from itertools import product


def _bit(v):
    if isinstance(v, str):
        v = v.strip()
        if v in ("X", "x"):
            return 0                      # quy uoc nhom: X -> 0
        return int(v)
    return int(v)


def _as_list(fault):
    if fault is None:
        return []
    return list(fault) if isinstance(fault, (list, tuple, set)) else [fault]


def _eval(typ, v):
    if typ == "AND":
        return int(all(v))
    if typ == "NAND":
        return 1 - int(all(v))
    if typ == "OR":
        return int(any(v))
    if typ == "NOR":
        return 1 - int(any(v))
    if typ == "XOR":
        return sum(v) % 2
    if typ == "XNOR":
        return 1 - sum(v) % 2
    if typ == "NOT":
        return 1 - v[0]
    if typ == "BUFF":
        return v[0]
    raise ValueError(f"Khong mo phong duoc cong {typ} (can full_scan/unroll truoc)")


def _split(fault):
    fl = _as_list(fault)
    stem = {f.net: f.stuck_at for f in fl if f.branch_to is None}
    branch = {(f.net, f.branch_to): f.stuck_at for f in fl if f.branch_to is not None}
    return stem, branch


def simulate(c, pattern, fault=None):
    """Tinh gia tri 0/1 cua moi net. fault co the la None, 1 Fault hoac danh sach Fault."""
    stem, branch = _split(fault)
    val = {}
    for pi in c.inputs:
        if pi not in pattern:
            raise ValueError(f"Pattern thieu dau vao {pi}")
        val[pi] = stem.get(pi, _bit(pattern[pi]))
    for g in c.dffs:                       # Q cua DFF coi nhu dau vao gia (mac dinh 0)
        val[g.output] = stem.get(g.output, _bit(pattern.get(g.output, 0)))
    for net in c.topo_order:
        g = c.gates[net]
        ins = [branch.get((i, net), val[i]) for i in g.inputs]
        val[net] = stem.get(net, _eval(g.type, ins))
    return val


def detects(c, pattern, fault):
    good = simulate(c, pattern)
    bad = simulate(c, pattern, fault)
    return any(good[o] != bad[o] for o in c.outputs)


def detects_cube(c, cube, fault, max_x=12):
    """True neu MOI cach dien X deu phat hien duoc loi (neu qua nhieu X thi thu dien het 0 va het 1)."""
    xs = [k for k, v in cube.items() if isinstance(v, str) and v in ("X", "x")]
    base = {k: (0 if k in xs else _bit(v)) for k, v in cube.items()}
    fills = (product((0, 1), repeat=len(xs)) if len(xs) <= max_x
             else [(0,) * len(xs), (1,) * len(xs)])
    for bits in fills:
        p = dict(base)
        p.update(zip(xs, bits))
        if not detects(c, p, fault):
            return False
    return True


def d_value(g, b):
    return {(0, 0): "0", (1, 1): "1", (1, 0): "D", (0, 1): "D'"}[(g, b)]


def trace_rows(c, pattern, fault):
    """Bang (net, tot, loi, gia tri 5) theo thu tu topo, de doi chieu voi trace chay tay."""
    good, bad = simulate(c, pattern), simulate(c, pattern, fault)
    return [(n, good[n], bad[n], d_value(good[n], bad[n])) for n in c.nets]


# ---------- coverage, fault dropping ----------
def coverage(c, patterns, faults, drop=True):
    """Mo phong noi tiep. drop=True: loi da phat hien thi khong mo phong them (fault dropping)."""
    detected_by = {}
    for f in faults:
        detected_by[f] = None
        for idx, p in enumerate(patterns):
            if detects(c, p, f):
                detected_by[f] = idx
                if drop:
                    break
    det = [f for f in faults if detected_by[f] is not None]
    total = len(faults)
    return {"total": total, "detected": len(det),
            "undetected": [f for f in faults if detected_by[f] is None],
            "coverage": 100.0 * len(det) / total if total else 100.0,
            "detected_by": detected_by}


def compact(c, patterns, faults):
    """Nen tap test: bo pattern khong phat hien them loi moi (luot xuoi, roi luot nguoc)."""
    target = {f for f in faults if any(detects(c, p, f) for p in patterns)}

    def one_pass(pats):
        remaining, kept = set(target), []
        for p in pats:
            new = {f for f in remaining if detects(c, p, f)}
            if new:
                kept.append(p)
                remaining -= new
        return kept

    kept = one_pass(patterns)
    return list(reversed(one_pass(list(reversed(kept)))))


# ---------- mo phong song song theo pattern (phep toan bit) ----------
def simulate_parallel(c, patterns, fault=None):
    """Moi net la mot so nguyen: bit k = gia tri cua pattern thu k. Tinh het pattern mot luot."""
    n = len(patterns)
    mask = (1 << n) - 1
    stem, branch = _split(fault)

    def force(net, word):
        return (mask if stem[net] else 0) if net in stem else word

    val = {}
    for pi in c.inputs:
        word = sum(_bit(p[pi]) << k for k, p in enumerate(patterns))
        val[pi] = force(pi, word)
    for g in c.dffs:
        word = sum(_bit(p.get(g.output, 0)) << k for k, p in enumerate(patterns))
        val[g.output] = force(g.output, word)
    for net in c.topo_order:
        g = c.gates[net]
        ins = [(mask if branch[(i, net)] else 0) if (i, net) in branch else val[i] for i in g.inputs]
        t = g.type
        if t in ("AND", "NAND"):
            w = mask
            for x in ins:
                w &= x
        elif t in ("OR", "NOR"):
            w = 0
            for x in ins:
                w |= x
        elif t in ("XOR", "XNOR"):
            w = 0
            for x in ins:
                w ^= x
        elif t in ("NOT", "BUFF"):
            w = ins[0]
        else:
            raise ValueError(f"Khong mo phong duoc cong {t}")
        if t in ("NAND", "NOR", "XNOR", "NOT"):
            w = ~w & mask
        val[net] = force(net, w)
    return val


def coverage_parallel(c, patterns, faults):
    """Giong coverage nhung moi loi chi mo phong mot lan cho toan bo tap pattern."""
    good = simulate_parallel(c, patterns)
    detected_by = {}
    for f in faults:
        bad = simulate_parallel(c, patterns, f)
        diff = 0
        for o in c.outputs:
            diff |= good[o] ^ bad[o]
        detected_by[f] = ((diff & -diff).bit_length() - 1) if diff else None
    det = [f for f in faults if detected_by[f] is not None]
    total = len(faults)
    return {"total": total, "detected": len(det),
            "undetected": [f for f in faults if detected_by[f] is None],
            "coverage": 100.0 * len(det) / total if total else 100.0,
            "detected_by": detected_by}


# ---------- doi chieu voi PODEM (chi hop cho mach it dau vao) ----------
def exhaustive_test(c, fault, max_pi=16):
    """Tim mot pattern bang vet can roi noi long thanh cube co X.
    Tra ve (cube | None, da_vet_can). Neu qua nhieu PI thi tra (None, False)."""
    if len(c.inputs) > max_pi:
        return None, False
    for bits in product((0, 1), repeat=len(c.inputs)):
        vec = dict(zip(c.inputs, bits))
        if detects(c, vec, fault):
            cube = dict(vec)
            for i in c.inputs:
                trial = dict(cube)
                trial[i] = "X"
                if detects_cube(c, trial, fault):
                    cube = trial
            return {k: str(v) for k, v in cube.items()}, True
    return None, True
