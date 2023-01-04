from functools import reduce
from typing import Callable

from tqdm import tqdm, trange

data = """Monkey 0:
  Starting items: 63, 57
  Operation: new = old * 11
  Test: divisible by 7
    If true: throw to monkey 6
    If false: throw to monkey 2

Monkey 1:
  Starting items: 82, 66, 87, 78, 77, 92, 83
  Operation: new = old + 1
  Test: divisible by 11
    If true: throw to monkey 5
    If false: throw to monkey 0

Monkey 2:
  Starting items: 97, 53, 53, 85, 58, 54
  Operation: new = old * 7
  Test: divisible by 13
    If true: throw to monkey 4
    If false: throw to monkey 3

Monkey 3:
  Starting items: 50
  Operation: new = old + 3
  Test: divisible by 3
    If true: throw to monkey 1
    If false: throw to monkey 7

Monkey 4:
  Starting items: 64, 69, 52, 65, 73
  Operation: new = old + 6
  Test: divisible by 17
    If true: throw to monkey 3
    If false: throw to monkey 7

Monkey 5:
  Starting items: 57, 91, 65
  Operation: new = old + 5
  Test: divisible by 2
    If true: throw to monkey 0
    If false: throw to monkey 6

Monkey 6:
  Starting items: 67, 91, 84, 78, 60, 69, 99, 83
  Operation: new = old * old
  Test: divisible by 5
    If true: throw to monkey 2
    If false: throw to monkey 4

Monkey 7:
  Starting items: 58, 78, 69, 65
  Operation: new = old + 7
  Test: divisible by 19
    If true: throw to monkey 5
    If false: throw to monkey 1"""

test_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


class Monkey:
    monkeys = []
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
            item = self.operation(item)
            # item = item // 3
            item = item % self.get_kgv()
            if item % self.test_param == 0:
                index = self.monkey_true
            else:
                index = self.monkey_false
            Monkey.monkeys[index].items.append(item)
        self.items_inspected += len(self.items)
        self.items = []

    @classmethod
    def from_string(cls, monkey_description: str):
        for line in monkey_description.split("\n"):
            if line.startswith("  Starting items: "):
                items = line.removeprefix("  Starting items: ").split(", ")
                items = [int(item) for item in items]
            elif line.startswith("  Operation: new = old "):
                operation, operator = line.removeprefix("  Operation: new = old ").split(" ")
                if operation == "+":
                    try:
                        operator = int(operator)
                        operation = lambda x: x + operator
                    except ValueError:
                        operation = lambda x: x + x
                elif operation == "*":
                    try:
                        operator = int(operator)
                        operation = lambda x: x * operator
                    except ValueError:
                        operation = lambda x: x * x
                else:
                    raise ValueError()
            elif line.startswith("  Test: divisible by "):
                test_param = int(line.removeprefix("  Test: divisible by "))
            elif line.startswith("    If true: throw to monkey "):
                monkey_true = int(line.removeprefix("    If true: throw to monkey "))
            elif line.startswith("    If false: throw to monkey "):
                monkey_false = int(line.removeprefix("    If false: throw to monkey "))
        return Monkey(items, operation, test_param, monkey_true, monkey_false)

    @classmethod
    def get_kgv(cls):
        if cls._kgv is None:
            primes = set(x.test_param for x in cls.monkeys)
            cls._kgv = reduce(lambda x, y: x * y, primes)
            tqdm.write(f"Set kgv to {cls._kgv}")
        return cls._kgv


monkey_descriptions = data.split("\n\n")
for monkey_description in monkey_descriptions:
    Monkey.from_string(monkey_description)


def calc_monkey_business(monkeys):
    for _ in trange(10_000):
        for monkey in Monkey.monkeys:
            monkey.turn()

    for i, monkey in enumerate(monkeys):
        print(f"Monkey{i} inspected {monkey.items_inspected} items")

    monkeys = sorted(monkeys, key=lambda x: x.items_inspected, reverse=True)
    return monkeys[0].items_inspected * monkeys[1].items_inspected


print(calc_monkey_business(Monkey.monkeys))
