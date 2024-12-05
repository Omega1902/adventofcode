def calc_visible(my_map):
    counter = len(my_map[0]) + len(my_map[-1]) + 2 * len(my_map) - 4
    for i, row in enumerate(my_map[1:-1], 1):
        for k, value in enumerate(row[1:-1], 1):
            if (
                max(row[:k]) < value  # left
                or max(row[k + 1 :]) < value  # right
                or max(temp_row[k] for temp_row in my_map[:i]) < value  # top
                or max(temp_row[k] for temp_row in my_map[i + 1 :]) < value  # bottom
            ):
                counter += 1
    return counter


def _calc_scenic_score(my_list: list[int], value: int) -> int:
    return next((i for i, item in enumerate(my_list, 1) if value <= item), len(my_list))


def calc_scenic_score(my_map):
    highscore = 0
    for i, row in enumerate(my_map[1:-1], 1):
        for k, value in enumerate(row[1:-1], 1):
            left = list(reversed(row[:k]))
            right = row[k + 1 :]
            top = list(reversed([temp_row[k] for temp_row in my_map[:i]]))
            bottom = [temp_row[k] for temp_row in my_map[i + 1 :]]
            score = (
                _calc_scenic_score(left, value)
                * _calc_scenic_score(right, value)
                * _calc_scenic_score(top, value)
                * _calc_scenic_score(bottom, value)
            )
            highscore = max(score, highscore)

    return highscore


def challenge1(data: str) -> int:
    my_map = [[int(char) for char in line] for line in data.splitlines()]
    return calc_visible(my_map)


def challenge2(data: str) -> int:
    my_map = [[int(char) for char in line] for line in data.splitlines()]
    return calc_scenic_score(my_map)
