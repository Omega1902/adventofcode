from collections.abc import Iterable
from functools import partial

from utils import get_data

test_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

Coord = tuple[int, int]
Matrix = list[list[int]]
weights = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
    "n": 13,
    "o": 14,
    "p": 15,
    "q": 16,
    "r": 17,
    "s": 18,
    "t": 19,
    "u": 20,
    "v": 21,
    "w": 22,
    "x": 23,
    "y": 24,
    "z": 25,
}


def parse_row(row: str) -> tuple[int | None, int | None, list[int]]:
    result = []
    start = None
    stop = None
    for i, char in enumerate(row):
        if char in weights:
            result.append(weights[char])
        elif char == "S":
            result.append(0)
            start = i
        elif char == "E":
            result.append(25)
            stop = i
        else:
            raise ValueError
    return start, stop, result


def parse_data(data: str) -> tuple[Coord, Coord, Matrix]:
    result = []
    start = None
    stop = None
    for i, row_str in enumerate(data.splitlines()):
        start_column, stop_column, row = parse_row(row_str)
        result.append(row)
        if start_column is not None:
            start = (i, start_column)
        if stop_column is not None:
            stop = (i, stop_column)
    if start is None or stop is None:
        raise ValueError("data cannot be parsed")
    return start, stop, result


def get_possible_nodes_for_node(node: Coord) -> Iterable[Coord]:
    yield (node[0] - 1, node[1])
    yield (node[0], node[1] - 1)
    yield (node[0], node[1] + 1)
    yield (node[0] + 1, node[1])


# def get_possible_nodes(visited_nodes: dict):
#     return (node for gen in map(get_possible_nodes, visited_nodes) for node in gen)


def can_go(start: Coord, stop: Coord, matrix: Matrix) -> bool:
    try:
        return matrix[start[0]][start[1]] + 1 >= matrix[stop[0]][stop[1]]
    except IndexError:
        return False


def node_is_valid(node: Coord, width: int, length: int) -> bool:
    return node[0] >= 0 and node[0] < length and node[1] >= 0 and node[1] < width


def heuristic(start: Coord, stop: Coord, matrix: Matrix) -> int:
    return matrix[stop[0]][stop[1]] - matrix[start[0]][start[1]]


def dijkstra(start: Coord, stop: Coord, matrix: Matrix) -> int:
    visited_nodes_open = {start: 0}
    visited_nodes = {start: 0}
    width = len(matrix[0])
    length = len(matrix)
    while stop not in visited_nodes:
        nodes_to_add = {}
        to_remove = set()
        for visited_node, steps in visited_nodes_open.items():
            new_nodes = [
                node
                for node in get_possible_nodes_for_node(visited_node)
                if node not in visited_nodes and node_is_valid(node, width, length)
            ]
            if not new_nodes:
                # node is not open since all valid neighbours are already visited
                to_remove.add(visited_node)
                continue
            for new_node in new_nodes:
                if can_go(visited_node, new_node, matrix) and nodes_to_add.get(new_node, 1_000_000_000) > steps + 1:
                    nodes_to_add[new_node] = steps + 1
        for node in to_remove:
            visited_nodes_open.pop(node)
        nodes_to_add_heuristic = {key: value + heuristic(key, stop, matrix) for key, value in nodes_to_add.items()}
        try:
            min_steps = min(nodes_to_add_heuristic.values())
        except ValueError:
            # seems like we cannot add any node - it is not possible to reach the target
            return 1_000_000_000
        nodes_to_add = {
            key: nodes_to_add[key] for key in nodes_to_add_heuristic if nodes_to_add_heuristic[key] == min_steps
        }
        visited_nodes |= nodes_to_add
        visited_nodes_open |= nodes_to_add
    return visited_nodes[stop]


def find_shortest(stop: Coord, matrix: Matrix) -> int:
    start_weight = 0
    possible_starting_points = (
        (row_id, column_id)
        for row_id, row in enumerate(matrix)
        for column_id, weight in enumerate(row)
        if weight == start_weight
    )
    my_dijkstra = partial(dijkstra, stop=stop, matrix=matrix)
    return min(map(my_dijkstra, possible_starting_points))


test_start, test_stop, test_matrix = parse_data(test_data)
start, stop, matrix = parse_data(get_data("input_day12.txt"))

assert dijkstra(test_start, test_stop, test_matrix) == 31  # noqa: PLR2004
print(dijkstra(start, stop, matrix))

assert find_shortest(test_stop, test_matrix) == 29  # noqa: PLR2004
print(find_shortest(stop, matrix))
