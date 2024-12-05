from collections.abc import Callable
from functools import reduce
from typing import ClassVar


class Monkey:
    monkeys: ClassVar[list["Monkey"]] = []
    _kgv = None

    def __init__(
        self, items: list[int], operation: Callable[[int], int], test_param: int, monkey_true: int, monkey_false: int
    ):
        self.items = items
        self.operation = operation
        self.test_param = test_param
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.items_inspected = 0
        Monkey.monkeys.append(self)

    def turn(self):
        for item in self.items:
            cur_item = self.operation(item)
            # cur_item = cur_item // 3
            cur_item = cur_item % self.get_kgv()
            index = self.monkey_true if cur_item % self.test_param == 0 else self.monkey_false
            Monkey.monkeys[index].items.append(cur_item)
        self.items_inspected += len(self.items)
        self.items = []

    @classmethod
    def from_string(cls, monkey_description: str):
        items = None
        operation = None
        test_param = None
        monkey_true = None
        monkey_false = None
        for line in monkey_description.split("\n"):
            if line.startswith("  Starting items: "):
                items = line.removeprefix("  Starting items: ").split(", ")
                items = [int(item) for item in items]
            elif line.startswith("  Operation: new = old "):
                operation, operator = line.removeprefix("  Operation: new = old ").split(" ")
                if operation == "+":
                    try:
                        operator = int(operator)
                        operation = lambda x: x + operator  # noqa: B023
                    except ValueError:
                        operation = lambda x: x + x
                elif operation == "*":
                    try:
                        operator = int(operator)
                        operation = lambda x: x * operator  # noqa: B023
                    except ValueError:
                        operation = lambda x: x * x
                else:
                    raise ValueError
            elif line.startswith("  Test: divisible by "):
                test_param = int(line.removeprefix("  Test: divisible by "))
            elif line.startswith("    If true: throw to monkey "):
                monkey_true = int(line.removeprefix("    If true: throw to monkey "))
            elif line.startswith("    If false: throw to monkey "):
                monkey_false = int(line.removeprefix("    If false: throw to monkey "))
        if items is None or operation is None or test_param is None or monkey_true is None or monkey_false is None:
            raise ValueError("monkey_description does not describe a monkey")
        return Monkey(items, operation, test_param, monkey_true, monkey_false)

    @classmethod
    def get_kgv(cls):
        if cls._kgv is None:
            primes = {x.test_param for x in cls.monkeys}
            cls._kgv = reduce(lambda x, y: x * y, primes)
        return cls._kgv


def calc_monkey_business(monkeys):
    for _ in range(10_000):
        for monkey in Monkey.monkeys:
            monkey.turn()

    monkeys = sorted(monkeys, key=lambda x: x.items_inspected, reverse=True)
    return monkeys[0].items_inspected * monkeys[1].items_inspected


def challenge2(data: str) -> int:
    monkey_descriptions = data.split("\n\n")
    for monkey_description in monkey_descriptions:
        Monkey.from_string(monkey_description)
    return calc_monkey_business(Monkey.monkeys)
