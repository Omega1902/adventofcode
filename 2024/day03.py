import re
from collections.abc import Iterable


def get_multipliers(data: str) -> Iterable[tuple[int, int]]:
    # python regex to get 1 to 3 digit numbers in mul(2,3)
    regex = r"mul\((\d{1,3}),(\d{1,3})\)"
    return ((int(n1), int(n2)) for n1, n2 in re.findall(regex, data))


def get_multipliers2(data: str) -> Iterable[tuple[int, int]]:
    # python regex to get 1 to 3 digit numbers in mul(2,3) or do() or don't()
    regex = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"
    mode = "do()"
    for match in re.findall(regex, data):
        if match[0] == "do()":
            mode = "do()"
        elif match[0] == "don't()":
            mode = "don't()"
        elif mode == "do()":
            yield (int(match[1]), int(match[2]))


def challenge1(data: str) -> int:
    multi = get_multipliers(data)
    return sum(x * y for x, y in multi)


def challenge2(data: str) -> int:
    multi = get_multipliers2(data)
    return sum(x * y for x, y in multi)
