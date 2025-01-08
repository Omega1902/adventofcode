import re
from collections.abc import Iterable
from enum import Enum, auto
from itertools import pairwise

from utils import get_lines


def get_numbers(line: str) -> Iterable[int]:
    return map(int, re.findall(r"\d+", line))


def level_is_safe(level: Iterable[int]) -> bool:
    direction = None
    for item1, item2 in pairwise(level):
        sub = item1 - item2
        if abs(sub) < 1 or abs(sub) > 3:
            return False
        if direction is None:
            direction = sub
        elif (sub > 0 and direction < 0) or (sub < 0 and direction > 0):
            return False
    return True


class LevelRemover(Enum):
    CanRemove = auto()
    IsRemoving = auto()
    HasRemoved = auto()


def _level_try_direction(level: list, direction: int) -> bool:
    item = LevelRemover.CanRemove
    previous_value: int | None = None
    for item1, item2 in pairwise(level):
        if item is LevelRemover.IsRemoving:
            item1 = previous_value  # noqa: PLW2901
            item = LevelRemover.HasRemoved
        sub = item1 - item2
        if abs(sub) < 1 or abs(sub) > 3:
            if item is LevelRemover.HasRemoved:
                print(str(level) + " is unsafe")
                return False
            item = LevelRemover.IsRemoving
            previous_value = item1
        if (sub > 0 and direction < 0) or (sub < 0 and direction > 0):
            if item is LevelRemover.HasRemoved:
                print(str(level) + " is unsafe")
                return False
            item = LevelRemover.IsRemoving
            previous_value = item1
    print(str(level) + " is safe")
    return True


def level_is_safe2(level: Iterable[int]) -> bool:
    level = list(level)
    return any(_level_try_direction(level, direction) for direction in (-1, 1)) or level_is_safe(level[1:])


def challenge1(filename: str) -> int:
    lines = get_lines(filename)
    levels: Iterable[Iterable[int]] = map(get_numbers, lines)

    return sum(1 for level in levels if level_is_safe(level))


def challenge2(filename: str) -> int:
    lines = get_lines(filename)
    levels: Iterable[Iterable[int]] = map(get_numbers, lines)

    return sum(1 for level in levels if level_is_safe2(level))


assert challenge1("data/test_day02.txt") == 2
print(challenge1("data/input_day02.txt"))


assert challenge2("data/test_day02.txt") == 4
print(challenge2("data/input_day02.txt"))
