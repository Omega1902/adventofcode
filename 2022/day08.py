from utils import Grid, parse_to_grid_tuple_int


def calc_visible(grid: Grid[int]) -> int:
    counter = len(grid[0]) + len(grid[-1]) + 2 * len(grid) - 4
    for i, row in enumerate(grid[1:-1], 1):
        for k, value in enumerate(row[1:-1], 1):
            if (
                max(row[:k]) < value  # left
                or max(row[k + 1 :]) < value  # right
                or max(temp_row[k] for temp_row in grid[:i]) < value  # top
                or max(temp_row[k] for temp_row in grid[i + 1 :]) < value  # bottom
            ):
                counter += 1
    return counter


def _calc_scenic_score(my_list: list[int] | tuple[int, ...], value: int) -> int:
    return next((i for i, item in enumerate(my_list, 1) if value <= item), len(my_list))


def calc_scenic_score(grid: Grid[int]) -> int:
    highscore = 0
    for i, row in enumerate(grid[1:-1], 1):
        for k, value in enumerate(row[1:-1], 1):
            left = list(reversed(row[:k]))
            right = row[k + 1 :]
            top = list(reversed([temp_row[k] for temp_row in grid[:i]]))
            bottom = [temp_row[k] for temp_row in grid[i + 1 :]]
            score = (
                _calc_scenic_score(left, value)
                * _calc_scenic_score(right, value)
                * _calc_scenic_score(top, value)
                * _calc_scenic_score(bottom, value)
            )
            highscore = max(score, highscore)

    return highscore


def challenge1(data: str) -> int:
    grid = parse_to_grid_tuple_int(data)
    return calc_visible(grid)


def challenge2(data: str) -> int:
    grid = parse_to_grid_tuple_int(data)
    return calc_scenic_score(grid)
