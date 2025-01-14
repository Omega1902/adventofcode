import operator
from collections.abc import Iterable
from functools import cmp_to_key, reduce


def find_matching_bracket(line: str, start: int = 0) -> int:
    bracket_depth = 0
    for i, char in enumerate(line[start:], start=start):
        if char == "[":
            bracket_depth += 1
        elif char == "]":
            bracket_depth -= 1
            if bracket_depth == 0:
                return i
    raise ValueError("No matching bracket")


def parse_array_string(line: str) -> list:
    content = line[1:-1]
    result = []
    while content:
        if content.startswith("["):
            rindex = find_matching_bracket(content)
            item = parse_array_string(content[: rindex + 1])
            result.append(item)
            content = content[rindex + 1 :]
            content = content.removeprefix(",")
        elif "," in content:
            item, content = content.split(",", maxsplit=1)
            try:
                result.append(int(item))
            except ValueError:
                print(item)
                print(content)
                raise
        else:
            try:
                result.append(int(content))
            except ValueError:
                print(content)
                raise
            content = ""
    return result


assert parse_array_string("[[1,[]],[2,3,4]]") == [[1, []], [2, 3, 4]]


def parse_pairs(pair: str) -> tuple[list, ...]:
    return tuple(map(parse_array_string, pair.splitlines()))


def parse_data(data: str) -> Iterable[tuple[list, ...]]:
    pairs = data.split("\n\n")
    return map(parse_pairs, pairs)


def right_order(left: list, right: list) -> int:
    for left_item, right_item in zip(left, right, strict=False):
        if isinstance(left_item, int) and isinstance(right_item, int):
            if left_item > right_item:
                return -1
            if right_item > left_item:
                return 1
        elif isinstance(left_item, list) and isinstance(right_item, list):
            if (result := right_order(left_item, right_item)) != 0:
                return result
        elif isinstance(left_item, int):
            if (result := right_order([left_item], right_item)) != 0:
                return result
        elif (result := right_order(left_item, [right_item])) != 0:
            return result
    return len(right) - len(left)


def compare_pairs(pairs: Iterable[tuple[list, ...]]) -> int:
    return sum(i for i, pair in enumerate(pairs, 1) if right_order(*pair) > 0)


def challenge1(data: str) -> int:
    pairs = tuple(parse_data(data))
    return compare_pairs(pairs)


def sort_packages(pairs: Iterable[tuple[list, ...]]) -> list[list]:
    # first flatten packages
    packages = (package for pair in pairs for package in pair)
    # sort packages
    return sorted(packages, key=cmp_to_key(right_order), reverse=True)


def find_divider_packets(package: list) -> bool:
    return package in ([[2]], [[6]])


def decoder_key(pairs: tuple[tuple[list, ...], ...]) -> int:
    pairs = (*pairs, ([[2]], [[6]]))
    packages = sort_packages(pairs)
    # pprint(packages)
    indexes = (i for i, package in enumerate(packages, 1) if find_divider_packets(package))
    return reduce(operator.mul, indexes)


def challenge2(data: str) -> int:
    pairs = tuple(parse_data(data))
    return decoder_key(pairs)
