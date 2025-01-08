import re
from collections.abc import Callable
from dataclasses import dataclass
from math import prod

from utils import GridBounds, Point


@dataclass(slots=True)
class Roboter:
    position: Point
    movement: Point
    grid_bounds: GridBounds

    @classmethod
    def from_string(cls, data: str, grid_bounds: GridBounds) -> "Roboter":
        px, py, mx, my = map(int, re.findall(r"-?\d+", data))
        return cls(Point(px, py), Point(mx, my), grid_bounds)

    def move(self) -> None:
        self.position = Point(
            (self.position.x + self.movement.x) % (self.grid_bounds.xmax + 1),
            (self.position.y + self.movement.y) % (self.grid_bounds.ymax + 1),
        )


@dataclass(slots=True)
class Quadrant:
    grid_bounds: GridBounds

    def count_robots(self, robots: tuple[Roboter, ...]) -> int:
        return sum(1 for robot in robots if self.grid_bounds.is_inside(robot.position.x, robot.position.y))


def print_grid(
    robots: tuple[Roboter, ...], grid_bounds: GridBounds, filter_fun: Callable[[int, int], bool] | None = None
) -> None:
    print()
    for y in range(grid_bounds.ymax + 1):
        for x in range(grid_bounds.xmax + 1):
            if filter_fun is not None and filter_fun(x, y):
                print(" ", end="")
            else:
                count = 0
                for robot in robots:
                    if robot.position == Point(x, y):
                        count += 1
                if count == 0:
                    print(".", end="")
                else:
                    print(count, end="")
        print()

    print()


def challenge1(data: str, grid_bounds: GridBounds | None = None) -> int:
    grid_bounds = grid_bounds or GridBounds(100, 102)
    robots = tuple(Roboter.from_string(robot, grid_bounds) for robot in data.splitlines())
    # print_grid(robots, grid_bounds)
    for _ in range(100):
        for robot in robots:
            robot.move()
    # print_grid(robots, grid_bounds)
    xmid = grid_bounds.xmax // 2
    ymid = grid_bounds.ymax // 2
    # print_grid(robots, grid_bounds, lambda x, y: x == xmid or y == ymid)
    quadrants = [
        Quadrant(GridBounds(xmid - 1, ymid - 1)),
        Quadrant(GridBounds(grid_bounds.xmax, ymid - 1, xmid + 1, 0)),
        Quadrant(GridBounds(xmid - 1, grid_bounds.ymax, 0, ymid + 1)),
        Quadrant(GridBounds(grid_bounds.xmax, grid_bounds.ymax, xmid + 1, ymid + 1)),
    ]
    return prod(q.count_robots(robots) for q in quadrants)


def challenge2_do_not_know_output(data: str, grid_bounds: GridBounds | None = None) -> int:
    grid_bounds = grid_bounds or GridBounds(100, 102)
    robots = tuple(Roboter.from_string(robot, grid_bounds) for robot in data.splitlines())
    print_grid(robots, grid_bounds)
    for i in range(2024):
        for robot in robots:
            robot.move()
        if i > 2020:
            print(i)
            print_grid(robots, grid_bounds)
    return 0
