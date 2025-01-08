from collections.abc import Iterable
from enum import Enum, auto
from typing import NamedTuple, TypeVar


class Direction(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_RIGHT = auto()
    TOP_LEFT = auto()
    BOTTOM_LEFT = auto()

    @staticmethod
    def straight() -> Iterable["Direction"]:
        yield Direction.TOP
        yield Direction.RIGHT
        yield Direction.BOTTOM
        yield Direction.LEFT

    @staticmethod
    def crossed() -> Iterable["Direction"]:
        yield Direction.TOP_LEFT
        yield Direction.TOP_RIGHT
        yield Direction.BOTTOM_LEFT
        yield Direction.BOTTOM_RIGHT


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

    def neighbours_straight(self) -> Iterable["Point"]:
        """Returns the four straight neighbours of the point"""
        for direction in Direction.straight():
            yield self.get_neighbour(direction)

    def neighbours_crossed(self) -> Iterable["Point"]:
        """Returns the four crossed neighbours of the point"""
        for direction in Direction.crossed():
            yield self.get_neighbour(direction)

    def neighbours_all(self) -> Iterable["Point"]:
        """Returns the all neighbours (straight + crossed) of the point"""
        for direction in Direction:
            yield self.get_neighbour(direction)

    def get_neighbour(self, direction: Direction) -> "Point":  # noqa: PLR0911
        """Returns the neighbour of the point in the given direction"""
        match direction:
            case Direction.TOP:
                return Point(self.x, self.y + 1)
            case Direction.RIGHT:
                return Point(self.x + 1, self.y)
            case Direction.BOTTOM:
                return Point(self.x, self.y - 1)
            case Direction.LEFT:
                return Point(self.x - 1, self.y)
            case Direction.TOP_RIGHT:
                return Point(self.x + 1, self.y + 1)
            case Direction.BOTTOM_RIGHT:
                return Point(self.x + 1, self.y - 1)
            case Direction.TOP_LEFT:
                return Point(self.x - 1, self.y + 1)
            case Direction.BOTTOM_LEFT:
                return Point(self.x - 1, self.y - 1)
        raise ValueError(f"Unknown direction {direction}")


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

    def iterate(self) -> Iterable[Point]:
        """Iterate over the GridBounds"""
        for y in range(self.ymin, self.ymax + 1):
            for x in range(self.xmin, self.xmax + 1):
                yield Point(x, y)

    def walk(self, point: Point, direction: Direction) -> Iterable[Point]:
        """Walk in the given direction from the given point. Stops at the border of the GridBounds"""
        while (point := point.get_neighbour(direction)) and self.is_inside(point.x, point.y):
            yield point
