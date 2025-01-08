import re
from collections.abc import Iterable
from typing import NamedTuple

from tqdm import trange

from utils import Point


class ClawMachine(NamedTuple):
    button_a: Point
    button_b: Point
    win: Point

    @classmethod
    def from_string(cls, data: str, offset: int = 0) -> "ClawMachine":
        a, b, w = data.splitlines()

        match = next(re.finditer(r"Button A: X\+(\d+), Y\+(\d+)", a))
        ax, ay = map(int, match.groups())

        match = next(re.finditer(r"Button B: X\+(\d+), Y\+(\d+)", b))
        bx, by = map(int, match.groups())

        match = next(re.finditer(r"Prize: X=(\d+), Y=(\d+)", w))
        wx, wy = map(int, match.groups())

        return cls(Point(ax, ay), Point(bx, by), Point(wx + offset, wy + offset))

    def cheapest_win(self, max_all: int | None = None) -> int:
        cheapest = None
        max_a = min(self.win.x // self.button_a.x, self.win.y // self.button_a.y)
        if max_all is not None:
            max_a = min(max_a, max_all)
        for i in trange(max_a + 1, delay=0.1):
            j = (self.win.x - (self.button_a.x * i)) // self.button_b.x
            if (
                i * self.button_a.x + j * self.button_b.x == self.win.x
                and i * self.button_a.y + j * self.button_b.y == self.win.y
            ):
                result = i * 3 + j
                if cheapest is None or result < cheapest:
                    cheapest = result

        return cheapest if cheapest is not None else 0


def challenge1(data: str) -> int:
    claw_machines: Iterable[ClawMachine] = map(ClawMachine.from_string, data.split("\n\n"))
    return sum(m.cheapest_win(100) for m in claw_machines)


def challenge2_takes_too_long(data: str) -> int:
    claw_machines: Iterable[ClawMachine] = (
        ClawMachine.from_string(machine, 10_000_000_000_000) for machine in data.split("\n\n")
    )
    return sum(m.cheapest_win() for m in claw_machines)
