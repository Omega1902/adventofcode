from collections.abc import Collection, Iterable
from functools import reduce
from itertools import tee

from utils import get_data

test_data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

Coord = tuple[int, int]
StonePath = tuple[Coord, ...]


def convert_to_coord(coord: str) -> Coord:
    return tuple(map(int, coord.split(",")))  # type: ignore


def parse_line(line: str) -> StonePath:
    return tuple(map(convert_to_coord, line.split(" -> ")))


def parse_data(data: str) -> tuple[StonePath, ...]:
    return tuple(map(parse_line, data.splitlines()))


def find_smallest_x(paths: Iterable[StonePath]):
    return min(coord[0] for path in paths for coord in path)


def find_highest_x(paths: Iterable[StonePath]):
    return max(coord[0] for path in paths for coord in path)


def find_smallest_y(paths: Iterable[StonePath]):
    return min(coord[1] for path in paths for coord in path)


def find_highest_y(paths: Iterable[StonePath]):
    return max(coord[1] for path in paths for coord in path)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


downward = lambda point: (point[0], point[1] + 1)
left_down = lambda point: (point[0] - 1, point[1] + 1)
right_down = lambda point: (point[0] + 1, point[1] + 1)
movements = (downward, left_down, right_down)


class Canvas:
    def __init__(self, paths: Collection[StonePath], floor=False):
        self.x_min = find_smallest_x(paths)
        self.x_max = find_highest_x(paths) + 1
        print(f"X axis from {self.x_min} to {self.x_max}")
        self.y_min = min(find_smallest_y(paths), 0)
        self.y_max = find_highest_y(paths)
        self.floor = self.y_max + 2 if floor else False
        if self.floor:
            self.y_max += 2
        print(f"Y axis from {self.y_min} to {self.y_max}")
        self.sand_counter = 0
        self.sand = (500, 0)
        self.canvas = reduce(
            lambda x, y: x + y, ([["."] * (self.x_max - self.x_min)] for _ in range(self.y_max - self.y_min + 1))
        )
        self.draw_point(self.sand, "+")
        self.draw_paths(paths)
        self.draw_floor()

    def draw_point(self, point: Coord, char: str):
        # print(f"Draw {char} on {point}")
        self.canvas[point[1] - self.y_min][point[0] - self.x_min] = char

    def draw_line(self, point_start: Coord, point_stop: Coord, char: str):
        if point_start[0] == point_stop[0]:
            start = min(point_start[1], point_stop[1])
            stop = max(point_start[1], point_stop[1]) + 1
            for y in range(start, stop):
                self.draw_point((point_start[0], y), char)
        else:
            start = min(point_start[0], point_stop[0])
            stop = max(point_start[0], point_stop[0]) + 1
            for x in range(start, stop):
                self.draw_point((x, point_start[1]), char)

    def draw_path(self, paths: StonePath):
        for point1, point2 in pairwise(paths):
            # print(f"Draw {point1} to {point2}")
            self.draw_line(point1, point2, "#")

    def draw_paths(self, paths: Collection[StonePath]):
        tuple(map(self.draw_path, paths))

    def draw_floor(self):
        if not self.floor:
            return
        for x in range(self.x_min, self.x_max):
            self.draw_point((x, self.floor), "#")

    def __str__(self):
        return "\n".join(("".join(line) for line in self.canvas))

    def add_column_left(self):
        for row in self.canvas:
            row.insert(0, ".")
        self.canvas[-1][0] = "#"
        self.x_min -= 1

    def add_column_right(self):
        for row in self.canvas:
            row.append(".")
        self.canvas[-1][-1] = "#"
        self.x_max += 1

    def point_is_empty(self, point: Coord) -> bool:
        if self.floor:
            if point[0] >= self.x_max:
                self.add_column_right()
            elif point[0] < self.x_min:
                self.add_column_left()
        elif point[0] > self.x_max or point[0] < self.x_min or point[1] > self.y_max:
            # point[1] < self.y_min not necessary
            raise ValueError
        return self.canvas[point[1] - self.y_min][point[0] - self.x_min] == "."

    def find_next_sand_point(self):
        cur_pos = self.sand
        while True:
            moved = False
            for move in movements:
                next_pos = move(cur_pos)
                if self.point_is_empty(next_pos):
                    cur_pos = next_pos
                    moved = True
                    break
            if not moved:  # no move is possible, return current position
                return cur_pos

    def draw_sand_cycle(self) -> bool:
        try:
            point = self.find_next_sand_point()
        except ValueError:
            return False
        self.draw_point(point, "o")
        self.sand_counter += 1
        return point != self.sand

    def draw_sand_complete(self):
        while self.draw_sand_cycle():
            pass


def task1(paths):
    canvas = Canvas(paths)
    canvas.draw_sand_complete()
    print(canvas)
    return canvas.sand_counter


def task2(paths):
    canvas = Canvas(paths, True)
    canvas.draw_sand_complete()
    # print(canvas)
    return canvas.sand_counter


test_paths = parse_data(test_data)
paths = parse_data(get_data("input_day14.txt"))

assert task1(test_paths) == 24  # noqa: PLR2004
print(task1(paths))

assert task2(test_paths) == 93  # noqa: PLR2004
print(task2(paths))
