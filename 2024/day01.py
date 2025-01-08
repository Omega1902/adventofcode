import re
from pathlib import Path


def get_abs_path(filename: str) -> Path:
    return Path(__file__).parent / filename


def get_data(filename: str) -> str:
    return get_abs_path(filename).read_text()


def get_lines(filename: str) -> list[str]:
    return get_data(filename).splitlines()


def read_lists(filename: str) -> tuple[list[int], list[int]]:
    lines = get_lines(filename)
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


def challenge1(filename: str) -> int:
    l1, l2 = read_lists(filename)
    return calc_lists_diff(l1, l2)


def challenge2(filename: str) -> int:
    l1, l2 = read_lists(filename)
    result = 0
    for e1 in l1:
        result += e1 * l2.count(e1)
    return result


assert challenge1("data/test_day01.txt") == 11
print(challenge1("data/input_day01.txt"))


assert challenge2("data/test_day01.txt") == 31
print(challenge2("data/input_day01.txt"))
