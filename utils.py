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
