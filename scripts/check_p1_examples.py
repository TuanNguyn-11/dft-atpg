"""Kiểm chứng độc lập ví dụ P1; không thay lõi ATPG của P4/P5/P6."""

from itertools import product


INPUTS = ("1", "2", "3", "6", "7")
GATES = {
    "10": ("1", "3"), "11": ("3", "6"), "16": ("2", "11"),
    "19": ("11", "7"), "22": ("10", "16"), "23": ("16", "19"),
}


def simulate(bits, fault=None):
    values = dict(zip(INPUTS, bits))
    if fault and fault[0] in values:
        values[fault[0]] = fault[1]
    for net, inputs in GATES.items():
        values[net] = 1 - (values[inputs[0]] & values[inputs[1]])
        if fault and fault[0] == net:
            values[net] = fault[1]
    return values["22"], values["23"]


def main():
    # Duyệt đầy đủ miền PI, độc lập với PODEM và fault_sim của nhóm.
    vectors = list(product((0, 1), repeat=5))
    assert all(simulate(v, ("1", 0)) == simulate(v, ("10", 1)) for v in vectors)
    cube = [v for v in vectors if v[1] == 1 and v[2] == 0]
    assert len(cube) == 8
    assert all(simulate(v)[0] != simulate(v, ("11", 0))[0] for v in cube)

    cc = {net: (1, 1) for net in INPUTS}
    for net, (a, b) in GATES.items():
        cc[net] = (cc[a][1] + cc[b][1] + 1, min(cc[a][0], cc[b][0]) + 1)
    co = {net: float("inf") for net in cc}
    co.update({"22": 0, "23": 0})
    for net, (a, b) in reversed(list(GATES.items())):
        co[a] = min(co[a], co[net] + cc[b][1] + 1)
        co[b] = min(co[b], co[net] + cc[a][1] + 1)
    expected = {
        "1": (1, 1, 5), "2": (1, 1, 6), "3": (1, 1, 5),
        "6": (1, 1, 7), "7": (1, 1, 6), "10": (3, 2, 3),
        "11": (3, 2, 5), "16": (4, 2, 3), "19": (4, 2, 3),
        "22": (5, 4, 0), "23": (5, 5, 0),
    }
    actual = {net: (*cc[net], co[net]) for net in cc}
    assert actual == expected, actual

    # Hình 4.5: lỗi stem y/SA0 tác động cả hai nhánh của y.
    detected = []
    for x, y, z in product((0, 1), repeat=3):
        good = (x & y) | ((1 - y) & z)
        faulty = z
        if good != faulty:
            detected.append((x, y, z))
    assert detected == [(0, 1, 1), (1, 1, 0)], detected
    print("PASS: collapsing (32 vectors); c17 cube (8 completions); SCOAP (11 nets)")
    print("PASS: Figure 4.5 (8 vectors), detects y/SA0: 011, 110")
    print("SCOAP: net CC0 CC1 CO")
    for net, values in actual.items():
        print(net, *values)


if __name__ == "__main__":
    main()
