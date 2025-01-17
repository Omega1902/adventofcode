import re
from collections.abc import Collection

from tqdm import trange


def parse_line(data: str):
    pattern = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    sx, sy, bx, by = re.findall(pattern, data)[0]
    beacon = Beacon(int(bx), int(by))
    return Sensor(int(sx), int(sy), beacon)


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

    def range_on_row(self, x: int) -> tuple[int, int] | None:
        radius_on_row = self.range_to_next_beacon - self._range_to_coords(x, self.y)
        if radius_on_row < 0:
            return None
        return self.y - radius_on_row, self.y + radius_on_row

    def closer_than_next_beacon(self, x: int, y: int) -> bool:
        return self._range_to_coords(x, y) <= self.range_to_next_beacon

    def __str__(self) -> str:
        return f"Sensor at ({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)


class Grid:
    def __init__(self, sensors: Collection[Sensor]):
        self.sensors = sensors
        self.beacons = {sensor.beacon for sensor in sensors}
        self.grid_items = self.beacons.union(sensors)
        self.x_min = min(grid_item.x for grid_item in self.grid_items)
        self.x_max = max(grid_item.x for grid_item in self.grid_items)
        self.y_min = min(grid_item.y for grid_item in self.grid_items)
        self.y_max = max(grid_item.y for grid_item in self.grid_items)
        self.sort_step = 100
        self.sort_sensors()

    def get_sorted_sensors(self, x: int) -> Collection[Sensor]:
        return self.sorted_sensors[x // self.sort_step]

    def add_sorted_sensor(self, sensor: Sensor, x_min: int, x_max: int) -> None:
        for index in range(x_min // self.sort_step, x_max // self.sort_step + 1):
            if index not in self.sorted_sensors:
                self.sorted_sensors[index] = set()
            self.sorted_sensors[index].add(sensor)

    def sort_sensors(self) -> None:
        self.sorted_sensors = {}  # [set()] * (self.x_max - self.x_min + 1)
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

    def find_distress_beacon(
        self, x: int, sensors: Collection[Sensor], range_min: int, range_max: int
    ) -> tuple[int, int] | None:
        ranges = [sensor_range for sensor in sensors if (sensor_range := sensor.range_on_row(x)) is not None]
        ranges.sort()
        index = range_min
        for sensor_range in ranges:
            if sensor_range[0] > index:
                return x, index
            index = max(sensor_range[1] + 1, index)
        return (x, index) if index < range_max else None

    def find_tuning_frequency(self, range_min: int, range_max: int) -> int:
        for x in trange(range_min, range_max + 1, delay=0.1):
            sensors = self.get_sorted_sensors(x)
            if (distress_beacon := self.find_distress_beacon(x, sensors, range_min, range_max)) is not None:
                return distress_beacon[0] * 4_000_000 + distress_beacon[1]
        raise ValueError("No distress beacon!")


def challenge1(data: str, param: int = 2_000_000) -> int:
    sensors = tuple(parse_data(data))
    grid = Grid(sensors)
    return grid.get_no_beacon(param)


def challenge2(data: str, param: int = 4_000_000) -> int:
    sensors = tuple(parse_data(data))
    grid = Grid(sensors)
    return grid.find_tuning_frequency(0, param)
