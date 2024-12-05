import contextlib
import re
from typing import Any


class MonkeyYell:
    def __init__(self, name: str, number: int) -> None:
        self.name = name
        self.number = number

    def yell(self, *args) -> int:  # noqa: ARG002
        return self.number

    def yell2(self, *args) -> int:
        if self.name == "humn":
            raise ValueError("HUMAN CANNOT YELL YET")
        return self.yell(*args)

    def to_yell(self, _, expected: float) -> float:
        if self.name != "humn":
            raise TypeError("I AM NO HUMAN")
        return expected


class MonkeyMath:
    def __init__(self, name: str, operation: str, monkey1: str, monkey2: str) -> None:
        self.name = name
        self.monkey1 = monkey1
        self.monkey2 = monkey2
        self.operation = operation

    def calc(self, number1: float, number2: float) -> float:
        if self.operation == "+":
            return number1 + number2
        if self.operation == "-":
            return number1 - number2
        if self.operation == "*":
            return number1 * number2
        if self.operation == "/":
            return number1 / number2
        raise ValueError(f"Operation {self.operation} does not exist")

    def yell(self, monkeys: dict[str, Any]) -> float:
        return self.calc(monkeys[self.monkey1].yell(monkeys), monkeys[self.monkey2].yell(monkeys))

    def yell2(self, monkeys: dict[str, Any]) -> float:
        return self.calc(monkeys[self.monkey1].yell2(monkeys), monkeys[self.monkey2].yell2(monkeys))

    def to_yell(self, monkeys: dict[str, Any], expected: float | None = None) -> float:
        result1 = None
        result2 = None
        with contextlib.suppress(ValueError):
            result1 = monkeys[self.monkey1].yell2(monkeys)
        with contextlib.suppress(ValueError):
            result2 = monkeys[self.monkey2].yell2(monkeys)
        if self.name == "root":
            expected = result1 if result2 is None else result2
            if result1 is None:
                return monkeys[self.monkey1].to_yell(monkeys, expected)
            return monkeys[self.monkey2].to_yell(monkeys, expected)

        if self.operation == "+":
            operation = lambda other, expected: expected - other
        elif self.operation == "*":
            operation = lambda other, expected: expected / other
        elif self.operation == "-" and result1 is None:
            operation = lambda res2, expected: res2 + expected
        elif self.operation == "-" and result2 is None:
            operation = lambda res1, expected: res1 - expected
        elif self.operation == "/" and result1 is None:
            operation = lambda res2, expected: res2 * expected
        elif self.operation == "/" and result2 is None:
            operation = lambda res1, expected: res1 / expected
        else:
            raise ValueError(f"Operation {self.operation} does not exist")
        if result1 is None:
            expected = operation(result2, expected)
            return monkeys[self.monkey1].to_yell(monkeys, expected)
        expected = operation(result1, expected)
        return monkeys[self.monkey2].to_yell(monkeys, expected)


Monkey = MonkeyMath | MonkeyYell


def parse_data(data: str) -> dict[str, Monkey]:
    result: dict[str, Monkey] = {}
    regex_results = re.findall(r"([a-zA-Z]+): (\d+)|([a-zA-Z]+): ([a-zA-Z]+) (.) ([a-zA-Z]+)", data)
    for regex_result in regex_results:
        if regex_result[0]:
            monkey = MonkeyYell(regex_result[0], int(regex_result[1]))
        else:
            monkey = MonkeyMath(regex_result[2], regex_result[4], regex_result[3], regex_result[5])
        result[monkey.name] = monkey

    return result


def get_root_number(monkeys: dict[str, Monkey]) -> float:
    return monkeys["root"].yell(monkeys)


def get_humn_number(monkeys: dict[str, Monkey]) -> float:
    monkey = monkeys["root"]
    if isinstance(monkey, MonkeyYell):
        raise TypeError("Root monkey does yell")
    root: MonkeyMath = monkey
    return root.to_yell(monkeys)


def challenge1(data: str) -> int:
    monkeys = parse_data(data)
    return int(get_root_number(monkeys))


def challenge2(data: str) -> int:
    monkeys = parse_data(data)
    return int(get_humn_number(monkeys))
