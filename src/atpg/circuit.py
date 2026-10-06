"""Doc netlist .bench va cau truc mach dung chung (P6). Giao dien theo muc 8 cua prompt.md."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass

_IO = re.compile(r"^(INPUT|OUTPUT)\s*\(\s*([^)\s]+)\s*\)$", re.I)
_GATE = re.compile(r"^(\S+)\s*=\s*([A-Za-z]+)\s*\(\s*([^)]*)\)$")
VALID_TYPES = {"AND", "NAND", "OR", "NOR", "NOT", "BUFF", "XOR", "XNOR", "DFF"}


@dataclass
class Gate:
    output: str          # ten net ngo ra cua cong, vd "10"
    type: str            # "AND","NAND","OR","NOR","NOT","BUFF","XOR","XNOR","DFF"
    inputs: list         # ten cac net ngo vao


class Circuit:
    """Quy uoc DFF: ngo ra Q cua DFF duoc xem la nguon (level 0, nhu pseudo-PI);
    cong DFF khong nam trong topo_order. Dung unroll.py (P4) de bien thanh mach to hop."""

    def __init__(self, name, inputs, outputs, gates):
        self.name = name
        self.inputs = list(inputs)
        self.outputs = list(outputs)
        self.gates = dict(gates)       # key = net ngo ra
        self._build()

    # ---- dung cac bang phu: fanout, topo_order, level ----
    def _build(self):
        defined = set(self.inputs) | set(self.gates)
        for pi in self.inputs:
            if pi in self.gates:
                raise ValueError(f"Net {pi} vua la INPUT vua la ngo ra cong")
        missing = sorted({i for g in self.gates.values() for i in g.inputs if i not in defined}
                         | {o for o in self.outputs if o not in defined})
        if missing:
            raise ValueError("Net chua duoc dinh nghia: " + ", ".join(missing))

        self.fanout = {n: [] for n in list(self.inputs) + list(self.gates)}
        for g in self.gates.values():
            seen = []
            for i in g.inputs:
                if i not in seen:                  # cong dung cung mot net hai lan chi tinh mot nhanh
                    seen.append(i)
                    self.fanout[i].append(g.output)

        self.level = {n: 0 for n in self.inputs}
        for g in self.gates.values():
            if g.type == "DFF":
                self.level[g.output] = 0
        pending = [g for g in self.gates.values() if g.type != "DFF"]
        self.topo_order = []
        while pending:
            ready = [g for g in pending if all(i in self.level for i in g.inputs)]
            if not ready:
                raise ValueError("Vong lap to hop trong mach: " + ", ".join(g.output for g in pending))
            for g in ready:
                self.level[g.output] = 1 + max(self.level[i] for i in g.inputs)
                self.topo_order.append(g.output)
            pending = [g for g in pending if g.output not in self.level]
        # sap xep on dinh theo (level, thu tu trong file)
        idx = {n: k for k, n in enumerate(self.gates)}
        self.topo_order.sort(key=lambda n: (self.level[n], idx[n]))

    @property
    def dffs(self):
        return [g for g in self.gates.values() if g.type == "DFF"]

    @property
    def nets(self):
        """Moi net: PI, ngo ra DFF, roi cac cong theo topo."""
        return list(self.inputs) + [g.output for g in self.dffs] + list(self.topo_order)

    def stats(self):
        return {"name": self.name, "PI": len(self.inputs), "PO": len(self.outputs),
                "gates": len(self.topo_order), "DFF": len(self.dffs), "nets": len(self.nets)}

    @staticmethod
    def from_gates(name, inputs, outputs, gates):
        """Tien ich cho P4: dung Circuit tu danh sach Gate (vd khi trai khung thoi gian)."""
        return Circuit(name, inputs, outputs, {g.output: g for g in gates})

    @staticmethod
    def from_bench(path: str) -> "Circuit":
        inputs, outputs, gates = [], [], {}
        with open(path, encoding="utf-8") as f:
            for n, raw in enumerate(f, 1):
                line = raw.split("#", 1)[0].strip()
                if not line:
                    continue
                m = _IO.match(line)
                if m:
                    (inputs if m.group(1).upper() == "INPUT" else outputs).append(m.group(2))
                    continue
                m = _GATE.match(line)
                if not m:
                    raise ValueError(f"{path}:{n}: dong khong hop le: {raw.strip()}")
                out, typ = m.group(1), m.group(2).upper()
                typ = "BUFF" if typ == "BUF" else typ
                if typ not in VALID_TYPES:
                    raise ValueError(f"{path}:{n}: loai cong chua ho tro: {typ}")
                ins = [s.strip() for s in m.group(3).split(",") if s.strip()]
                if out in gates:
                    raise ValueError(f"{path}:{n}: net {out} bi dinh nghia hai lan")
                gates[out] = Gate(out, typ, ins)
        name = os.path.splitext(os.path.basename(path))[0]
        return Circuit(name, inputs, outputs, gates)
