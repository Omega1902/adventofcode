from typing import NamedTuple

Grid = list[list[str]]

NEXT: dict[str, str] = {
    "0": "1",
    "1": "2",
    "2": "3",
    "3": "4",
    "4": "5",
    "5": "6",
    "6": "7",
    "7": "8",
    "8": "9",
}


class Point(NamedTuple):
    x: int
    y: int


def parse_input(data: str) -> Grid:
    return [list(x) for x in data.splitlines()]


def get_start_points(grid: Grid) -> list[Point]:
    return [Point(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == "0"]


def get_path_solutions(grid: Grid, start: Point, distinct: bool) -> int:
    MAX_X = len(grid[0]) - 1
    MAX_Y = len(grid) - 1

    def inner(point: Point) -> list[Point]:
        if grid[point.y][point.x] == "9":
            return [point]
        count = []
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            new_x, new_y = point.x + dx, point.y + dy
            if 0 <= new_x <= MAX_X and 0 <= new_y <= MAX_Y and grid[new_y][new_x] == NEXT[grid[point.y][point.x]]:
                count.extend(inner(Point(new_x, new_y)))
        return count

    result = inner(start)
    if distinct:
        result = set(result)
    return len(result)


def get_paths_solutions(grid: Grid, distinct: bool) -> int:
    starts = get_start_points(grid)
    return sum(get_path_solutions(grid, start, distinct) for start in starts)


def challenge1(data: str) -> int:
    grid = parse_input(data)
    return get_paths_solutions(grid, True)


def challenge2(data: str) -> int:
    grid = parse_input(data)
    return get_paths_solutions(grid, False)
