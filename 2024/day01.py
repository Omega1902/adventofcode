import re


def read_lists(data: str) -> tuple[list[int], list[int]]:
    lines = data.strip().splitlines()
    l1, l2 = [], []
    for line in lines:
        res = re.findall(r"(\d+) +(\d+)", line)
        l1.append(int(res[0][0]))
        l2.append(int(res[0][1]))
    return l1, l2


def calc_lists_diff(list1: list[int], list2: list[int]) -> int:
    l1 = sorted(list1)
    l2 = sorted(list2)
    result = 0
    for e1, e2 in zip(l1, l2, strict=True):
        result += abs(e1 - e2)
    return result


def challenge1(data: str) -> int:
    l1, l2 = read_lists(data)
    return calc_lists_diff(l1, l2)


def challenge2(data: str) -> int:
    l1, l2 = read_lists(data)
    result = 0
    for e1 in l1:
        result += e1 * l2.count(e1)
    return result
