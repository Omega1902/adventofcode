import os
import re
from collections.abc import Collection

from tqdm import trange

test_data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


def get_abs_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), filename))


def get_data() -> str:
    with open(get_abs_path("input_day15.txt")) as myfile:
        return myfile.read()


def parse_line(data: str):
    pattern = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    sx, sy, bx, by = re.findall(pattern, data)[0]
    beacon = Beacon(int(bx), int(by))
    sensor = Sensor(int(sx), int(sy), beacon)
    return sensor


def parse_data(data: str):
    return map(parse_line, data.splitlines())


class GridItem:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"GridItem at ({self.x}, {self.y})"


class Beacon(GridItem):
    def __str__(self) -> str:
        return f"Beacon at ({self.x}, {self.y})"


class Sensor(GridItem):
    def __init__(self, x: int, y: int, beacon: Beacon):
        super().__init__(x, y)
        self.beacon = beacon
        self.range_to_next_beacon = self.range_to_grid_item(self.beacon)

    def _range_to_coords(self, x: int, y: int):
        return abs(self.x - x) + abs(self.y - y)

    def range_to_grid_item(self, other: GridItem):
        return self._range_to_coords(other.x, other.y)

    def closer_than_next_beacon(self, x: int, y: int) -> bool:
        return self._range_to_coords(x, y) <= self.range_to_next_beacon

    def __str__(self) -> str:
        return f"Sensor at ({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)


class Grid:
    def __init__(self, sensors: Collection[Sensor]):
        self.sensors = sensors
        self.beacons = set(sensor.beacon for sensor in sensors)
        self.grid_items = self.beacons.union(sensors)
        self.x_min = min(grid_item.x for grid_item in self.grid_items)
        self.x_max = max(grid_item.x for grid_item in self.grid_items)
        self.y_min = min(grid_item.y for grid_item in self.grid_items)
        self.y_max = max(grid_item.y for grid_item in self.grid_items)
        print(f"Matrix x {self.x_min} to {self.x_max} and y {self.y_min} to {self.y_max}")
        self.sort_step = 100
        self.sort_sensors()

    def get_sorted_sensors(self, x: int) -> Collection[Sensor]:
        return self.sorted_sensors[x // self.sort_step]

    def add_sorted_sensor(self, sensor: Sensor, x_min: int, x_max: int) -> None:
        for index in range(x_min // self.sort_step, x_max // self.sort_step + 1):
            if index not in self.sorted_sensors.keys():
                self.sorted_sensors[index] = set()
            self.sorted_sensors[index].add(sensor)

    def sort_sensors(self) -> None:
        self.sorted_sensors = dict()  # [set()] * (self.x_max - self.x_min + 1)
        for sensor in self.sensors:
            self.add_sorted_sensor(
                sensor, sensor.x - sensor.range_to_next_beacon, sensor.x + sensor.range_to_next_beacon
            )

    def cannot_be_beacon(self, x: int, y: int) -> bool:
        beacons = tuple(beacon for beacon in self.beacons if beacon.x == x and beacon.y == y)
        if beacons:
            return False
        return any(sensor.closer_than_next_beacon(x, y) for sensor in self.sensors)

    def can_be_distress_beacon(self, x: int, y: int, sensors: Collection[Sensor]) -> bool:
        return not any(sensor.closer_than_next_beacon(x, y) for sensor in sensors)

    def get_no_beacon(self, row: int) -> int:
        counter = 0
        for x in range(self.x_min, self.x_max + 1):
            if self.cannot_be_beacon(x, row):
                counter += 1
        x = self.x_min - 1
        while self.cannot_be_beacon(x, row):
            counter += 1
            x -= 1
        x = self.x_max + 1
        while self.cannot_be_beacon(x, row):
            counter += 1
            x += 1
        return counter

    def find_tuning_frequency(self, range_min: int, range_max: int) -> int:
        for x in trange(range_min, range_max + 1):
            sensors = self.get_sorted_sensors(x)
            # print(len(sensors))
            for y in range(range_min, range_max + 1):
                if self.can_be_distress_beacon(x, y, sensors):
                    return x * 4000000 + y


test_sensors = tuple(parse_data(test_data))
sensors = tuple(parse_data(get_data()))

test_grid = Grid(test_sensors)
grid = Grid(sensors)

assert test_grid.get_no_beacon(10) == 26
print(grid.get_no_beacon(2000000))  # 4033885 is to low

assert test_grid.find_tuning_frequency(0, 20) == 56000011  # works
print(grid.find_tuning_frequency(0, 4000000))  # might take days to complete
