"""D-algorithm (Roth 1966) cho mot loi stuck-at tren mach to hop (P6).

Muc dich: chay CUNG mot loi bang D-algorithm va PODEM de so sanh (xem compare.py).
Thuat toan bam theo cach nhom chay tay o Chuong 3 (P2):
  1. Chon PDCF de kich hoat loi (D/D' tai vi tri loi).
  2. Implication tien/lui.
  3. Neu sai khac chua toi PO: chon mot cong trong D-frontier va mot PDC de lan truyen.
  4. Neu sai khac da toi PO: justify cac net trong J-frontier bang singular cover.
  5. Xung dot: khoi phuc trang thai va thu lua chon khac (quay lui).
Thanh cong khi sai khac toi PO VA J-frontier rong.

Quyet dinh duoc dat tren NET NOI BO (cube cua tung cong), khac PODEM chi gan PI.

Bieu dien: moi net la cap (good, faulty), moi thanh phan 0/1/None (None = chua biet).
  0=(0,0), 1=(1,1), D=(1,0), D'=(0,1), X=(None,None).

Heuristic mac dinh (chon de trung bang chay tay cua P2 cho c17 11/SA0):
  - D-frontier: uu tien cong gan PO nhat (level lon nhat), hoa thi theo thu tu trong file.
  - Thu tu thu cube (PDCF, singular cover): dau vao SAU truoc (order="last");
    order="first" thu dau vao dau truoc. Thu tu chi doi cach tim, khong doi tinh dung.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from itertools import product

from atpg.faults import Fault, validate_fault

CONTROLLING = {"AND": 0, "NAND": 0, "OR": 1, "NOR": 1}
INVERTING = {"NAND", "NOR", "NOT", "XNOR"}
SUPPORTED = {"AND", "NAND", "OR", "NOR", "NOT", "BUFF", "XOR", "XNOR"}


PAIR = {"0": (0, 0), "1": (1, 1), "D": (1, 0), "D'": (0, 1), "X": (None, None)}


def five(pair):
    """Cap (g, f) -> ky hieu 5 gia tri; con thanh phan chua biet thi la X."""
    return {(0, 0): "0", (1, 1): "1", (1, 0): "D", (0, 1): "D'"}.get(tuple(pair), "X")


def _eval_bit(typ, bits):
    """Danh gia mot thanh phan (logic 3 gia tri 0/1/None)."""
    if typ in ("AND", "NAND", "OR", "NOR"):
        c = CONTROLLING[typ]
        if any(b == c for b in bits):
            out = c
        elif all(b == 1 - c for b in bits):
            out = 1 - c
        else:
            return None
    elif typ in ("XOR", "XNOR"):
        if any(b is None for b in bits):
            return None
        out = sum(bits) % 2
    elif typ in ("NOT", "BUFF"):
        out = bits[0]
        if out is None:
            return None
    else:
        raise ValueError(f"D-algorithm chua ho tro loai cong {typ}")
    return 1 - out if typ in INVERTING else out


@dataclass
class DalgResult:
    fault: object
    status: str                       # DETECTED | UNTESTABLE | ABORTED
    pattern: dict                     # PI -> "0"/"1"/"X"
    decisions: int = 0                # so lan chon cube (PDCF + PDC + cover)
    backtracks: int = 0
    implications: int = 0             # so lan goi implication
    gate_evals: int = 0               # so lan danh gia cong (ca hai thanh phan)
    internal_assigned: list = field(default_factory=list)   # net noi bo bi gan boi quyet dinh
    justifications: int = 0           # so lan chon singular cover de justify
    steps: list = field(default_factory=list)


class _Abort(Exception):
    pass


class DAlgorithm:
    def __init__(self, c, fault, max_backtracks=1000, order="last", trace=False):
        if isinstance(fault, (list, tuple)):
            raise ValueError("D-algorithm o day chi nhan MOT loi (khong nhan danh sach loi da trai khung)")
        validate_fault(c, fault)
        if c.dffs:
            raise ValueError("D-algorithm chi chay tren mach to hop (can unroll/full_scan truoc)")
        for g in c.gates.values():
            if g.type not in SUPPORTED:
                raise ValueError(f"D-algorithm chua ho tro loai cong {g.type}")
        if order not in ("last", "first"):
            raise ValueError("order phai la 'last' hoac 'first'")
        if max_backtracks < 0:
            raise ValueError("max_backtracks phai >= 0")
        self.c, self.f = c, fault
        self.max_bt = max_backtracks
        self.order = order
        self.trace = trace
        self.res = DalgResult(fault, "UNTESTABLE", {})
        self.cone = self._cone()

    # ---------------- tien ich ----------------
    def _cone(self):
        """Cac net nam trong vung anh huong cua loi (o ngoai vung, mach tot = mach loi)."""
        start = self.f.branch_to if self.f.branch_to is not None else self.f.net
        seen, todo = {start}, [start]
        while todo:
            n = todo.pop()
            for g in self.c.fanout.get(n, []):
                if g not in seen:
                    seen.add(g)
                    todo.append(g)
        return seen

    def _ordered(self, items):
        return list(reversed(items)) if self.order == "last" else list(items)

    def _seen(self, val, net, gate):
        """Gia tri ma cong `gate` nhin thay tren ngo vao `net` (tinh ca loi nhanh)."""
        g, f = val[net]
        if self.f.branch_to == gate and self.f.net == net:
            f = self.f.stuck_at
        return [g, f]

    def _is_stem_fault_net(self, net):
        return self.f.branch_to is None and self.f.net == net

    def _set(self, val, net, comp, v):
        """Gan mot thanh phan cho net; tra False neu xung dot. Ngoai vung loi: g va f luon bang nhau."""
        if comp == 1 and self._is_stem_fault_net(net):
            return v == self.f.stuck_at
        cur = val[net][comp]
        if cur is not None:
            return cur == v
        val[net][comp] = v
        if net not in self.cone:
            other = 1 - comp
            if val[net][other] is None:
                val[net][other] = v
            elif val[net][other] != v:
                return False
        return True

    def _set_input(self, val, net, gate, comp, v):
        """Gan thanh phan cho ngo vao `net` cua `gate` (bo qua thanh phan bi ep boi loi nhanh)."""
        if comp == 1 and self.f.branch_to == gate and self.f.net == net:
            return v == self.f.stuck_at
        return self._set(val, net, comp, v)

    # ---------------- implication ----------------
    def _seen5(self, val, net, gate):
        """Gia tri 5 nguyen thuy (0/1/X/D/D') cong `gate` nhin thay; thong tin mot nua bi bo (= X)."""
        return five(self._seen(val, net, gate))

    def _eval5(self, val, out):
        """Gia tri 5 cua cong `out` tinh tu ngo vao hien tai (khong doc gia tri da gan cua `out`)."""
        gate = self.c.gates[out]
        ins = [PAIR[self._seen5(val, i, out)] for i in gate.inputs]
        g = _eval_bit(gate.type, [x[0] for x in ins])
        f = _eval_bit(gate.type, [x[1] for x in ins])
        if self._is_stem_fault_net(out):
            f = self.f.stuck_at
        return five((g, f))

    def imply(self, val):
        """Implication tien va lui den diem bat dong, theo logic 5 gia tri (D-calculus).
        Tra False neu co xung dot."""
        self.res.implications += 1
        c = self.c
        changed = True
        while changed:
            changed = False
            for out in c.topo_order:                       # tien
                gate = c.gates[out]
                ins = [PAIR[self._seen5(val, i, out)] for i in gate.inputs]
                self.res.gate_evals += 1
                g = _eval_bit(gate.type, [x[0] for x in ins])
                f = _eval_bit(gate.type, [x[1] for x in ins])
                if self._is_stem_fault_net(out):
                    f = self.f.stuck_at
                if g is None or f is None:                 # 5 gia tri: chua du ca hai thanh phan = X
                    continue
                before = five(val[out])
                if not (self._set(val, out, 0, g) and self._set(val, out, 1, f)):
                    return False
                changed |= five(val[out]) != before
            for out in reversed(c.topo_order):             # lui: chi tu gia tri 0/1 chua duoc ngo vao suy ra
                v = five(val[out])
                if v not in ("0", "1") or self._eval5(val, out) != "X":
                    continue
                gate = c.gates[out]
                req = self._backward(gate.type, int(v), [self._seen5(val, i, out) for i in gate.inputs])
                if req is False:
                    return False
                for i, rv in zip(gate.inputs, req):
                    if rv is None:
                        continue
                    before = five(val[i])
                    if not (self._set_input(val, i, out, 0, rv) and self._set_input(val, i, out, 1, rv)):
                        return False
                    changed |= five(val[i]) != before
        return True

    @staticmethod
    def _backward(typ, v, ins):
        """Gia tri (0/1) bat buoc o ngo vao khi ngo ra la v (0/1); ins la gia tri 5 cua ngo vao.
        None = khong suy ra duoc; False = mau thuan."""
        raw = 1 - v if typ in INVERTING else v
        if typ in ("NOT", "BUFF"):
            return [raw]
        if typ in ("AND", "NAND", "OR", "NOR"):
            c = CONTROLLING[typ]
            if raw == 1 - c:                               # khong bi dieu khien: moi ngo vao = 1-c
                if any(x in ("D", "D'") for x in ins):
                    return False
                return [1 - c] * len(ins)
            if any(x == str(c) for x in ins):              # da co ngo vao dieu khien
                return [None] * len(ins)
            unknown = [k for k, x in enumerate(ins) if x == "X"]
            if not unknown:
                return False
            if len(unknown) == 1:                          # chi con mot cach: ngo vao do = c
                req = [None] * len(ins)
                req[unknown[0]] = c
                return req
            return [None] * len(ins)
        if typ in ("XOR", "XNOR"):
            unknown = [k for k, x in enumerate(ins) if x == "X"]
            if len(unknown) == 1 and all(x in ("0", "1", "X") for x in ins):
                req = [None] * len(ins)
                req[unknown[0]] = (raw - sum(int(x) for x in ins if x != "X")) % 2
                return req
            return [None] * len(ins)
        return [None] * len(ins)

    # ---------------- frontier ----------------
    def d_frontier(self, val):
        out = []
        for name in self.c.topo_order:
            if five(val[name]) != "X":
                continue
            gate = self.c.gates[name]
            if any(five(self._seen(val, i, name)) in ("D", "D'") for i in gate.inputs):
                out.append(name)
        lvl = self.c.level
        idx = {n: k for k, n in enumerate(self.c.topo_order)}
        return sorted(out, key=lambda n: (-lvl[n], idx[n]))      # gan PO nhat truoc

    def j_frontier(self, val):
        """Cong co ngo ra da gan 0/1 nhung ngo vao chua du de suy ra gia tri do (can justify)."""
        return [n for n in self.c.topo_order
                if five(val[n]) in ("0", "1") and self._eval5(val, n) == "X"]

    def error_at_po(self, val):
        return [o for o in self.c.outputs if five(val[o]) in ("D", "D'")]

    # ---------------- cube ----------------
    def _cover_inputs(self, typ, n_in, out_value):
        """Singular cover: cac cach gan ngo vao (list gia tri, None = X) cho ngo ra out_value."""
        raw = 1 - out_value if typ in INVERTING else out_value
        if typ in ("NOT", "BUFF"):
            return [[raw]]
        if typ in ("AND", "NAND", "OR", "NOR"):
            c = CONTROLLING[typ]
            if raw == c:                                       # mot ngo vao dieu khien la du
                cubes = []
                for k in range(n_in):
                    cube = [None] * n_in
                    cube[k] = c
                    cubes.append(cube)
                return self._ordered(cubes)
            return [[1 - c] * n_in]
        cubes = [list(bits) for bits in product((0, 1), repeat=n_in) if sum(bits) % 2 == raw]
        return self._ordered(cubes)

    def _apply_inputs(self, val, gate_name, values):
        gate = self.c.gates[gate_name]
        for net, v in zip(gate.inputs, values):
            if v is None:
                continue
            for comp in (0, 1):
                if not self._set_input(val, net, gate_name, comp, v):
                    return False
        return True

    def _decide(self, kind, gate, assigned, val):
        """Ghi nhan mot quyet dinh (chon cube)."""
        self.res.decisions += 1
        for n in assigned:
            if n not in self.c.inputs and n not in self.res.internal_assigned:
                self.res.internal_assigned.append(n)
        if kind == "Cover":
            self.res.justifications += 1

    def _record(self, kind, gate, cube_text, val, action):
        if not self.trace:
            return
        self.res.steps.append({
            "Bước": len(self.res.steps) + 1,
            "Loại": kind,
            "Cổng": gate,
            "Cube": cube_text,
            "Giá trị các net": {n: five(val[n]) for n in self.c.nets},
            "D-frontier": self.d_frontier(val),
            "J-frontier": self.j_frontier(val),
            "Hành động": action,
        })

    def _fail(self):
        self.res.backtracks += 1
        if self.res.backtracks > self.max_bt:
            raise _Abort()

    # ---------------- tim kiem ----------------
    def _activation_options(self, val):
        """Cac PDCF: (mo ta, ham ap dung) de dat sai khac tai vi tri loi."""
        f, c = self.f, self.c
        want = 1 - f.stuck_at
        opts = []
        if f.branch_to is not None or f.net in c.inputs:
            def act(v, net=f.net):
                return self._set(v, net, 0, want) and (net in self.cone or self._set(v, net, 1, want))
            label = f"{f.net}={want}"
            opts.append((label, [f.net], act, f.branch_to or f.net))
            return opts
        gate = c.gates[f.net]
        for cube in self._cover_inputs(gate.type, len(gate.inputs), want):
            def act(v, cube=cube, gate=gate):
                if not self._apply_inputs(v, gate.output, cube):
                    return False
                return self._set(v, gate.output, 0, want)
            text = ", ".join(f"{n}={'X' if b is None else b}" for n, b in zip(gate.inputs, cube))
            label = f"({text}) -> {gate.output}={'D' if want == 1 else "D'"}"
            assigned = [n for n, b in zip(gate.inputs, cube) if b is not None] + [gate.output]
            opts.append((label, assigned, act, gate.output))
        return opts

    def _propagation_options(self, val, gate_name):
        gate = self.c.gates[gate_name]
        ins = [self._seen(val, i, gate_name) for i in gate.inputs]
        side = [k for k, x in enumerate(ins) if five(x) not in ("D", "D'")]
        if gate.type in CONTROLLING:
            choices = [[1 - CONTROLLING[gate.type]] * len(side)]
        elif gate.type in ("XOR", "XNOR"):
            choices = self._ordered([list(b) for b in product((0, 1), repeat=len(side))])
        else:
            choices = [[]]
        opts = []
        for ch in choices:
            values = [None] * len(gate.inputs)
            for k, v in zip(side, ch):
                values[k] = v
            text = ", ".join(f"{gate.inputs[k]}={v}" for k, v in zip(side, ch)) or "-"
            assigned = [gate.inputs[k] for k in side] + [gate_name]
            opts.append((f"PDC qua {gate_name}: {text}", assigned, values))
        return opts

    def _search(self, val, pending=None):
        """pending = (loai, cong, mo ta cube): ghi vao trace SAU khi implication."""
        ok = self.imply(val)
        if pending is not None:
            self._record(*pending, val, {"PDCF": "kích hoạt", "PDC": "lan truyền", "Cover": "justify"}
                         [pending[0]] if ok else "xung đột")
        if not ok:
            return None
        if self.error_at_po(val):
            jf = self.j_frontier(val)
            if not jf:
                return val
            gname = jf[0]
            gate = self.c.gates[gname]
            want = int(five(val[gname]))
            for cube in self._cover_inputs(gate.type, len(gate.inputs), want):
                v2 = copy.deepcopy(val)
                assigned = [n for n, b in zip(gate.inputs, cube) if b is not None]
                text = ", ".join(f"{n}={'X' if b is None else b}" for n, b in zip(gate.inputs, cube))
                self._decide("Cover", gname, assigned, v2)
                if self._apply_inputs(v2, gname, cube):
                    r = self._search(v2, ("Cover", gname, f"({text}) -> {gname}={want}"))
                    if r is not None:
                        return r
                self._fail()
                self._record("Backtrack", gname, f"bo cover ({text})", val, "backtrack")
            return None
        df = self.d_frontier(val)
        if not df:
            return None
        for gname in df:
            for text, assigned, values in self._propagation_options(val, gname):
                v2 = copy.deepcopy(val)
                self._decide("PDC", gname, assigned, v2)
                if self._apply_inputs(v2, gname, values):
                    r = self._search(v2, ("PDC", gname, text))
                    if r is not None:
                        return r
                self._fail()
                self._record("Backtrack", gname, f"bo {text}", val, "backtrack")
        return None

    def run(self):
        c = self.c
        start = {n: [None, None] for n in c.nets}
        if self._is_stem_fault_net(self.f.net):
            start[self.f.net][1] = self.f.stuck_at
        found = None
        try:
            for text, assigned, act, site in self._activation_options(start):
                v = copy.deepcopy(start)
                self._decide("PDCF", site, assigned, v)
                if act(v):
                    found = self._search(v, ("PDCF", site, text))
                    if found is not None:
                        break
                self._fail()
                self._record("Backtrack", site, f"bo PDCF {text}", start, "backtrack")
        except _Abort:
            self.res.status = "ABORTED"
            self.res.backtracks = min(self.res.backtracks, self.max_bt)
            if self.trace:
                self.res.steps.append({"Bước": len(self.res.steps) + 1, "Loại": "-", "Cổng": "-",
                                       "Cube": "-", "Giá trị các net": {}, "D-frontier": [],
                                       "J-frontier": [], "Hành động": "thất bại (vượt giới hạn backtrack)"})
            return self.res
        if found is None:
            self.res.status = "UNTESTABLE"
            return self.res
        self.res.status = "DETECTED"
        self.res.pattern = {pi: ("X" if found[pi][0] is None else str(found[pi][0])) for pi in c.inputs}
        if self.trace and self.res.steps:
            self.res.steps[-1]["Hành động"] = "thành công"
        return self.res


def d_algorithm(c, fault, max_backtracks=1000, order="last", trace=False) -> DalgResult:
    """Chay D-algorithm cho mot loi stuck-at tren mach to hop `c`."""
    return DAlgorithm(c, fault, max_backtracks=max_backtracks, order=order, trace=trace).run()
