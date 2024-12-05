priority = [
    0,
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]


def challenge1(data: str) -> int:
    prio_sum = 0
    for line in data.splitlines():
        if line == "":
            continue
        length = len(line)
        compartment1 = set(line[slice(0, length // 2)])
        compartment2 = set(line[slice(length // 2, length)])
        leftover = compartment1.intersection(compartment2)
        assert len(leftover) == 1
        item = leftover.pop()
        prio_sum += priority.index(item)
    return prio_sum


def challenge2(data: str) -> int:
    prio_sum = 0
    backpacks = [set(line) for line in data.splitlines() if line]
    length = len(backpacks)
    for b1, b2, b3 in zip(
        backpacks[slice(0, length, 3)], backpacks[slice(1, length, 3)], backpacks[slice(2, length, 3)], strict=False
    ):
        common_item = b1.intersection(b2).intersection(b3)
        assert len(common_item) == 1
        item = common_item.pop()
        prio_sum += priority.index(item)
    return prio_sum
