from dataclasses import dataclass, field

from utils import Direction, GridBounds, GridTuple, Point, parse_to_grid_tuple_str


@dataclass(slots=True)
class Region:
    plants_type: str
    grid_bounds: GridBounds
    area: list[Point] = field(default_factory=list)
    perimeter: list[Point] = field(default_factory=list)

    def contains(self, point: Point) -> bool:
        return point in self.area

    @classmethod
    def from_point(cls, point: Point, grid: GridTuple, grid_bounds: GridBounds) -> "Region":
        region = cls(grid[point.y][point.x], grid_bounds, [point])

        points = [point]
        while points:
            new_points = []
            for p in points:
                for new_point in p.neighbours_straight():
                    if not grid_bounds.is_inside(new_point.x, new_point.y):
                        region.perimeter.append(new_point)
                        continue
                    if new_point in region.area or new_point in points or new_point in new_points:
                        continue
                    if grid[new_point.y][new_point.x] == region.plants_type:
                        region.area.append(new_point)
                        new_points.append(new_point)
                    else:
                        region.perimeter.append(new_point)
            points = new_points

        return region

    def get_price_by_perimeter(self) -> int:
        return len(self.perimeter) * len(self.area)

    def get_sides(self) -> int:
        result = 0
        marked_points: set[tuple[Point, Direction]] = set()
        for point in self.area:
            for direction in Direction.straight():
                if point.get_neighbour(direction) in self.perimeter:
                    marker = (point, direction)
                    if marker not in marked_points:
                        result += 1
                        marked_points.add((point, direction))
                        walking_directions: tuple[Direction, Direction] = (
                            (Direction.TOP, Direction.BOTTOM)
                            if direction in (Direction.RIGHT, Direction.LEFT)
                            else (Direction.RIGHT, Direction.LEFT)
                        )
                        for walking_direction in walking_directions:
                            for walk_point in self.grid_bounds.walk(point, walking_direction):
                                if walk_point in self.area and walk_point.get_neighbour(direction) in self.perimeter:
                                    marked_points.add((walk_point, direction))
                                else:
                                    break

        return result

    def get_price_by_sides(self) -> int:
        return self.get_sides() * len(self.area)


def price_fencing(grid: GridTuple[str], discount: bool) -> int:
    bounds = GridBounds.from_grid(grid)
    regions: list[Region] = []
    for point in bounds.iterate():
        if any(region.contains(point) for region in regions):
            continue
        regions.append(Region.from_point(point, grid, bounds))
    if discount:
        return sum(region.get_price_by_sides() for region in regions)
    return sum(region.get_price_by_perimeter() for region in regions)


def challenge1(data: str) -> int:
    grid = parse_to_grid_tuple_str(data)
    return price_fencing(grid, discount=False)


def challenge2(data: str) -> int:
    grid = parse_to_grid_tuple_str(data)
    return price_fencing(grid, discount=True)
