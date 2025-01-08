import operator
import re
from collections.abc import Callable, Iterable


def find_solutions(
    resolution: int, *numbers: int, operators: tuple[Callable[[int, int], int], ...] = (operator.add, operator.mul)
) -> int:
    def inner_find_solutions(res: int, *numbers: int) -> bool:
        if not numbers:
            return resolution == res
        for op in operators:
            res1 = op(res, numbers[0])
            if res1 <= resolution and (result := inner_find_solutions(res1, *numbers[1:])):
                return result
        return False

    solution = inner_find_solutions(0, *numbers)
    return resolution if solution else 0


def problem_to_str(resolution: int, *numbers: int) -> str:
    return f"{resolution}: {' '.join(map(str, numbers))}"


def parse_input(data: str) -> Iterable[Iterable[int]]:
    lines = data.splitlines()
    return (map(int, re.findall(r"\d+", line)) for line in lines)


def concat(n1: int, n2: int) -> int:
    return int(str(n1) + str(n2))


def challenge1(data: str) -> int:
    math_problems = parse_input(data)
    return sum(find_solutions(*math_problem, operators=(operator.add, operator.mul)) for math_problem in math_problems)


def challenge2(data: str) -> int:
    math_problems = parse_input(data)
    return sum(
        find_solutions(*math_problem, operators=(operator.add, operator.mul, concat)) for math_problem in math_problems
    )
