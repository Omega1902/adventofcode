from typing import NamedTuple

from tqdm import tqdm

Map = list[list[str]]


class Point(NamedTuple):
    x: int
    y: int


def get_next_point(grid: Map, point: Point) -> Point:
    match grid[point.y][point.x]:
        case "^":
            return Point(point.x, point.y - 1)
        case "v":
            return Point(point.x, point.y + 1)
        case "<":
            return Point(point.x - 1, point.y)
        case ">":
            return Point(point.x + 1, point.y)
        case _:
            raise ValueError(f"Invalid point at {point}: " + grid[point.y][point.x])


def turn_right(grid: Map, point: Point) -> None:
    match grid[point.y][point.x]:
        case "^":
            grid[point.y][point.x] = ">"
        case ">":
            grid[point.y][point.x] = "v"
        case "v":
            grid[point.y][point.x] = "<"
        case "<":
            grid[point.y][point.x] = "^"
        case _:
            raise ValueError(f"Invalid point at {point}: " + grid[point.y][point.x])


def find_distinct_visits(grid: Map) -> int:
    guard = find_guard(grid)
    max_point = Point(len(grid[0]) - 1, len(grid) - 1)
    while guard.y > 0 and guard.x > 0 and guard.y < max_point.y and guard.x < max_point.x:
        new_position = get_next_point(grid, guard)
        while grid[new_position.y][new_position.x] == "#":
            turn_right(grid, guard)
            new_position = get_next_point(grid, guard)
        grid[new_position.y][new_position.x] = grid[guard.y][guard.x]
        grid[guard.y][guard.x] = "X"
        guard = new_position
    grid[guard.y][guard.x] = "X"
    return sum(row.count("X") for row in grid)


def find_guard(mal: Map) -> Point:
    for y in range(len(mal)):
        for x, item in enumerate(mal[y]):
            if item in "^<>v":
                return Point(x, y)
    raise ValueError("No guard found")


def loops(grid: Map, guard: Point, max_point: Point) -> bool:
    visited: dict[Point, tuple[str, ...]] = {}
    visited[guard] = (grid[guard.y][guard.x],)
    while guard.y > 0 and guard.x > 0 and guard.y < max_point.y and guard.x < max_point.x:
        new_position = get_next_point(grid, guard)
        while grid[new_position.y][new_position.x] == "#":
            turn_right(grid, guard)
            new_position = get_next_point(grid, guard)
        grid[new_position.y][new_position.x] = grid[guard.y][guard.x]
        grid[guard.y][guard.x] = "X"
        guard = new_position
        if grid[guard.y][guard.x] in visited.get(guard, ()):
            return True
        visited[guard] = (*visited.get(guard, ()), grid[guard.y][guard.x])
    return False


def find_obstruction_places(grid) -> int:
    guard = find_guard(grid)
    max_point = Point(len(grid[0]) - 1, len(grid) - 1)
    result = 0
    possible_obstruction_points = [
        Point(x, y) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] not in "#^v<>"
    ]
    for p in tqdm(possible_obstruction_points, delay=0.1):
        grid_copy = [row.copy() for row in grid]
        grid_copy[p.y][p.x] = "#"
        if loops(grid_copy, guard, max_point):
            result += 1
    return result


def challenge1(data: str) -> int:
    grid = [list(line) for line in data.splitlines()]
    return find_distinct_visits(grid)


def challenge2(data: str) -> int:
    grid = [list(line) for line in data.splitlines()]
    return find_obstruction_places(grid)
