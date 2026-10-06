"""Sinh danh sach loi stuck-at va gop loi tuong duong (P6). Giao dien theo muc 8 cua prompt.md."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fault:
    net: str
    stuck_at: int                    # 0 hoac 1
    branch_to: str | None = None     # None = loi tren stem; "16" = loi tren nhanh cua net di vao cong 16

    def __str__(self):
        where = self.net if self.branch_to is None else f"{self.net}->{self.branch_to}"
        return f"{where}/SA{self.stuck_at}"


def has_branches(c, net):
    """Net co nhanh rieng khi no re nhieu huong (nhieu cong, hoac vua la PO vua vao cong).
    Han che: nhanh di toi PO khong bieu dien duoc bang branch_to nen khong sinh loi rieng cho no."""
    n_dest = len(c.fanout.get(net, [])) + (1 if net in c.outputs else 0)
    return len(c.fanout.get(net, [])) >= 1 and n_dest > 1


def all_faults(c) -> list:
    """Toan bo loi: moi net co SA0/SA1 tren stem; net re nhanh co them SA0/SA1 tren tung nhanh."""
    out = []
    for net in c.nets:
        for sv in (0, 1):
            out.append(Fault(net, sv))
        if has_branches(c, net):
            for g in c.fanout[net]:
                for sv in (0, 1):
                    out.append(Fault(net, sv, g))
    return out


# loai cong -> danh sach (gia tri ket o ngo vao, gia tri ket tuong duong o ngo ra)
_EQUIV = {
    "AND": [(0, 0)],
    "NAND": [(0, 1)],
    "OR": [(1, 1)],
    "NOR": [(1, 0)],
    "NOT": [(0, 1), (1, 0)],
    "BUFF": [(0, 0), (1, 1)],
}


def _input_line_fault(c, net, gate_out, sv):
    """Loi tren duong dua net vao cong: la loi nhanh neu net re nhanh, nguoc lai la loi stem."""
    return Fault(net, sv, gate_out) if has_branches(c, net) else Fault(net, sv)


def equivalence_classes(c, faults: list) -> list:
    """Chia danh sach loi thanh cac lop tuong duong (dung union-find)."""
    present = set(faults)
    parent = {f: f for f in faults}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for g in c.gates.values():
        for in_sv, out_sv in _EQUIV.get(g.type, []):
            out_f = Fault(g.output, out_sv)
            for net in g.inputs:
                a = _input_line_fault(c, net, g.output, in_sv)
                if a in present and out_f in present:
                    parent[find(a)] = find(out_f)
    groups = {}
    for f in faults:
        groups.setdefault(find(f), []).append(f)
    return list(groups.values())


def collapse(c, faults: list) -> list:
    """Gop loi tuong duong (equivalence). Moi lop giu 1 dai dien: loi gan ngo ra nhat."""
    index = {f: k for k, f in enumerate(faults)}

    def loc_level(f):
        return c.level[f.net] if f.branch_to is None else c.level[f.branch_to]

    reps = [max(m, key=lambda f: (loc_level(f), f.branch_to is None, -index[f]))
            for m in equivalence_classes(c, faults)]
    reps.sort(key=lambda f: index[f])
    return reps
