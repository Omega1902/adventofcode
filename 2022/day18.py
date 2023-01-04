def get_data()->str:
    with open("input_day18.txt") as myfile:
        return myfile.read()


data = get_data()
test_data = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def parse_line(line):
    x, y, z = line.split(",")
    return (int(x), int(y), int(z))


def parse_data(data):
    return set(map(parse_line, data.splitlines()))


def is_lava(cube, cubes):
    return cube in cubes


def is_not_lava(cube, cubes, *args):
    return not is_lava(cube, cubes)


def is_in_dim(cube, dims):
    # print(type(cube), type(dims))
    return (
        cube[0] >= dims[0]
        and cube[0] <= dims[1]
        and cube[1] >= dims[2]
        and cube[1] <= dims[3]
        and cube[2] >= dims[4]
        and cube[2] <= dims[5]
    )


def is_air(cube, cubes, dims, air_bubble=None):
    global air
    if cube in air:
        return True
    is_root = False
    if air_bubble is None:
        air_bubble = set()
        is_root = True
        air_bubble.add(cube)
    if not is_in_dim(cube, dims):
        return False
    neighbours = tuple(
        n for n in get_neighbours(cube) if not is_lava(n, cubes) and n not in air_bubble
    )
    air_bubble.update(neighbours)
    try:
        result = all(
            is_air(neighbour, cubes, dims, air_bubble) for neighbour in neighbours
        )
    except:
        print(cube)
    if result and is_root:
        air.update(air_bubble)
        # print(f"bubble size {len(air_bubble)}")
    return result


def is_water(cube, cubes, dims):
    if is_lava(cube, cubes):
        return False
    return not is_air(cube, cubes, dims)


def get_neighbours(cube):
    x, y, z = cube
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


def parts(cubes, strategy, dims):
    exposed_surfaces = (
        1 if strategy(neighbour, cubes, dims) else 0
        for cube in cubes
        for neighbour in get_neighbours(cube)
    )
    print(sum(exposed_surfaces))


def get_dims(cubes) -> tuple[int, int, int, int, int, int]:
    x_min = min(cube[0] for cube in cubes)
    x_max = max(cube[0] for cube in cubes)
    y_min = min(cube[1] for cube in cubes)
    y_max = max(cube[1] for cube in cubes)
    z_min = min(cube[2] for cube in cubes)
    z_max = max(cube[2] for cube in cubes)
    return x_min, x_max, y_min, y_max, z_min, z_max


cubes = parse_data(data)
dims = get_dims(cubes)
print(dims)
air = set()

# part1
parts(cubes, is_not_lava, dims)

# part2
parts(cubes, is_water, dims)
# 3246 is to high for part2
# 3236 is to high for part2
# 2005 is to low for part2
