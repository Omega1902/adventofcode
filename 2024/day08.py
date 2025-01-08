from itertools import combinations

from utils import GridBounds, GridTuple, Point, parse_to_grid_tuple_str


def get_antennas(grid: GridTuple[str]) -> set[str]:
    antennas = set()
    for row in grid:
        antennas.update(row)
    antennas.remove(".")
    return antennas


def find_antenna_positions(grid: GridTuple[str], antenna: str) -> set[Point]:
    antenna_positions = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == antenna:
                antenna_positions.add(Point(x, y))
    return antenna_positions


def _find_antinodes(grid: GridTuple[str], antenna: str, grid_bounds: GridBounds) -> set[Point]:
    antinodes = set()

    def add_antinode(x: int, y: int):
        if new_point := grid_bounds.create_point(x, y):
            antinodes.add(new_point)

    antenna_positions = find_antenna_positions(grid, antenna)
    for antenna1, antenna2 in combinations(antenna_positions, 2):
        diff_x = antenna1.x - antenna2.x
        diff_y = antenna1.y - antenna2.y
        add_antinode(antenna1.x + diff_x, antenna1.y + diff_y)
        add_antinode(antenna2.x - diff_x, antenna2.y - diff_y)
    return antinodes


def find_antinodes(grid: GridTuple[str], antennas: set[str]) -> set[Point]:
    antinodes = set()
    grid_bounds = GridBounds.from_grid(grid)
    for antenna in antennas:
        antinodes.update(_find_antinodes(grid, antenna, grid_bounds))
    return antinodes


def _find_antinodes2(grid: GridTuple[str], antenna: str, grid_bounds: GridBounds) -> set[Point]:
    antinodes = set()

    antenna_positions = find_antenna_positions(grid, antenna)
    if len(antenna_positions) > 1:
        antinodes.update(antenna_positions)
    antinodes.update(antenna_positions)
    for antenna1, antenna2 in combinations(antenna_positions, 2):
        diff_x = antenna1.x - antenna2.x
        diff_y = antenna1.y - antenna2.y
        x = antenna1.x + diff_x
        y = antenna1.y + diff_y
        while grid_bounds.is_inside(x, y):
            antinodes.add(Point(x, y))
            x += diff_x
            y += diff_y
        x = antenna2.x - diff_x
        y = antenna2.y - diff_y
        while grid_bounds.is_inside(x, y):
            antinodes.add(Point(x, y))
            x -= diff_x
            y -= diff_y
    return antinodes


def find_antinodes2(grid: GridTuple[str], antennas: set[str]) -> set[Point]:
    antinodes = set()
    grid_bounds = GridBounds.from_grid(grid)
    for antenna in antennas:
        antinodes.update(_find_antinodes2(grid, antenna, grid_bounds))
    return antinodes


def challenge1(data: str) -> int:
    grid = parse_to_grid_tuple_str(data)
    antennas = get_antennas(grid)
    return len(find_antinodes(grid, antennas))


def challenge2(data: str) -> int:
    grid = parse_to_grid_tuple_str(data)
    antennas = get_antennas(grid)
    return len(find_antinodes2(grid, antennas))
