from typing import NamedTuple, TypeVar

T = TypeVar("T")

GridList = list[list[T]]
GridTuple = tuple[tuple[T, ...], ...]
Grid = GridList[T] | GridTuple[T]


def parse_to_grid_tuple_str(data: str) -> GridTuple[str]:
    """Parse a string to a tuple of tuples containing a character as element"""
    return tuple(tuple(line) for line in data.splitlines())


def parse_to_grid_list_str(data: str) -> GridList[str]:
    """Parse a string to a list of lists containing a character as element"""
    return [list(line) for line in data.splitlines()]


def parse_to_grid_tuple_int(data: str) -> GridTuple[int]:
    """Parse a string to a tuple of tuples containing an integer (0-9) as element"""
    return tuple(tuple(int(char) for char in line) for line in data.splitlines())


def parse_to_grid_list_int(data: str) -> GridList[int]:
    """Parse a string to a list of lists containing an integer (0-9) as element"""
    return [[int(char) for char in line] for line in data.splitlines()]


class Point(NamedTuple):
    x: int
    y: int


class GridBounds(NamedTuple):
    xmax: int
    ymax: int
    xmin: int = 0
    ymin: int = 0

    @classmethod
    def from_grid(cls, grid: Grid) -> "GridBounds":
        return cls(len(grid[0]) - 1, len(grid) - 1, 0, 0)

    def create_point(self, x: int, y: int) -> Point | None:
        """Creates Point and returs it if it is inside of the GridBounds. Otherwise returns None"""
        if self.is_inside(x, y):
            return Point(x, y)
        return None

    def is_inside(self, x: int, y: int) -> bool:
        """Returns True if the given coordinates are inside the GridBounds"""
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax
