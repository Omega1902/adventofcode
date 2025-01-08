from typing import Final, Literal

import tqdm

from utils import Grid, GridList, GridTuple, Point

_ROCKS = ["####", ".#.\n###\n.#.", "..#\n..#\n###", "#\n#\n#\n#", "##\n##"]


ROCKS: Final[tuple[GridTuple[str], ...]] = tuple(
    tuple(tuple(rock_line) for rock_line in rocks) for rocks in (rocks.splitlines() for rocks in _ROCKS)
)


Movement = Literal["<", ">"]


class Cave:
    def __init__(self, width: int) -> None:
        self.width: Final = width
        self.empty_line: Final = ["."] * width
        self.grid: GridList[str] = [self.empty_line.copy(), self.empty_line.copy(), self.empty_line.copy()]
        self.rocks_in_motion: list[Point] = []

    def get_height(self) -> int:
        for i in range(len(self.grid) - 1, -1, -1):
            if self.grid[i] != self.empty_line:
                return i + 1
        return 0

    def _ensure_empty_lines(self) -> None:
        while not (
            self.grid[-1] == self.empty_line and self.grid[-2] == self.empty_line and self.grid[-3] == self.empty_line
        ):
            self.grid.append(self.empty_line.copy())
        if len(self.grid) < 4:
            return
        while self.grid[-4] == self.empty_line:
            self.grid.pop()

    def add_rock(self, rock: Grid[str]) -> None:
        self._ensure_empty_lines()
        for rock_line in reversed(rock):
            line_to_add = [".", "."]
            for i, rock_item in enumerate(rock_line):
                if rock_item == "#":
                    self.rocks_in_motion.append(Point(i + 2, len(self.grid)))
                    line_to_add.append("@")
                else:
                    line_to_add.append(rock_item)
            # fill line with "."
            while len(line_to_add) < self.width:
                line_to_add.append(".")
            self.grid.append(line_to_add)

    def rock_in_motion(self) -> bool:
        # return any("@" in self.grid[i] for i in range(len(self.grid), 0, -1))
        return bool(self.rocks_in_motion)

    def _mark_mul(self, points: list[Point], char: str) -> None:
        for point in points:
            self.grid[point.y][point.x] = char

    def _move_if_possible(self, try_points: list[Point]) -> bool:
        can_move = all(
            try_Point.x >= 0
            and try_Point.x < self.width
            and try_Point.y >= 0
            and self.grid[try_Point.y][try_Point.x] != "#"
            for try_Point in try_points
        )
        if can_move:
            self._mark_mul(self.rocks_in_motion, ".")
            self._mark_mul(try_points, "@")

            self.rocks_in_motion = try_points
        return can_move

    def fixate_rocks_in_motion(self) -> None:
        self._mark_mul(self.rocks_in_motion, "#")
        self.rocks_in_motion = []

    def rock_down(self) -> None:
        try_points = [Point(rock.x, rock.y - 1) for rock in self.rocks_in_motion]
        can_fall = self._move_if_possible(try_points)
        if not can_fall:
            self.fixate_rocks_in_motion()

    def move(self, movement: Movement) -> None:
        to_add = 1 if movement == ">" else -1
        try_points = [Point(rock.x + to_add, rock.y) for rock in self.rocks_in_motion]
        self._move_if_possible(try_points)

    def __str__(self) -> str:
        return (
            "\n".join("|" + "".join(self.grid[i]) + "|" for i in range(len(self.grid) - 1, -1, -1))
            + "\n+"
            + ("-" * self.width)
            + "+"
        )

    def debug(self) -> None:
        print(self.rocks_in_motion)
        print(self.grid)
        print(str(self))
        print()


def get_cave_height(movements: str, rocks_count: int = 2022, cave_width: int = 7) -> int:
    movements_index = 0
    cave = Cave(cave_width)
    for i in tqdm.trange(rocks_count, delay=0.1):
        cave.add_rock(ROCKS[i % len(ROCKS)])
        while cave.rock_in_motion():
            movement: Movement = movements[movements_index % len(movements)]  # type: ignore
            movements_index += 1
            cave.move(movement)
            cave.rock_down()

    return cave.get_height()


def challenge1(data: str) -> int:
    return get_cave_height(data)


def challenge2_takes_too_long(data: str) -> int:
    return get_cave_height(data, 1_000_000_000_000)  # takes to long
