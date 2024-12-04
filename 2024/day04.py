def xmas_bottom_to_top(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:  # noqa: ARG001
    return x >= 3 and input_lines[x - 1][y] == "M" and input_lines[x - 2][y] == "A" and input_lines[x - 3][y] == "S"


def xmas_top_to_bottom(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:  # noqa: ARG001
    return (
        x <= X_MAX - 3
        and input_lines[x + 1][y] == "M"
        and input_lines[x + 2][y] == "A"
        and input_lines[x + 3][y] == "S"
    )


def xmas_right_to_left(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:  # noqa: ARG001
    return y >= 3 and input_lines[x][y - 1] == "M" and input_lines[x][y - 2] == "A" and input_lines[x][y - 3] == "S"


def xmas_left_to_right(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:  # noqa: ARG001
    return (
        y <= Y_MAX - 3
        and input_lines[x][y + 1] == "M"
        and input_lines[x][y + 2] == "A"
        and input_lines[x][y + 3] == "S"
    )


def xmas_to_top_left(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:  # noqa: ARG001
    return (
        x >= 3
        and y >= 3
        and input_lines[x - 1][y - 1] == "M"
        and input_lines[x - 2][y - 2] == "A"
        and input_lines[x - 3][y - 3] == "S"
    )


def xmas_to_top_right(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:  # noqa: ARG001
    return (
        x >= 3
        and y <= Y_MAX - 3
        and input_lines[x - 1][y + 1] == "M"
        and input_lines[x - 2][y + 2] == "A"
        and input_lines[x - 3][y + 3] == "S"
    )


def xmas_to_bottom_left(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:  # noqa: ARG001
    return (
        x <= X_MAX - 3
        and y >= 3
        and input_lines[x + 1][y - 1] == "M"
        and input_lines[x + 2][y - 2] == "A"
        and input_lines[x + 3][y - 3] == "S"
    )


def xmas_to_bottom_right(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:
    return (
        x <= X_MAX - 3
        and y <= Y_MAX - 3
        and input_lines[x + 1][y + 1] == "M"
        and input_lines[x + 2][y + 2] == "A"
        and input_lines[x + 3][y + 3] == "S"
    )


def challenge1(data: str) -> int:
    input_lines = data.strip().splitlines()
    X_MAX = len(input_lines) - 1
    Y_MAX = len(input_lines[0]) - 1
    result = 0
    for x, row in enumerate(input_lines):
        for y, char in enumerate(row):
            if char == "X":
                result += (
                    xmas_to_bottom_left(input_lines, x, y, X_MAX, Y_MAX)
                    + xmas_to_bottom_right(input_lines, x, y, X_MAX, Y_MAX)
                    + xmas_to_top_left(input_lines, x, y, X_MAX, Y_MAX)
                    + xmas_to_top_right(input_lines, x, y, X_MAX, Y_MAX)
                    + xmas_bottom_to_top(input_lines, x, y, X_MAX, Y_MAX)
                    + xmas_top_to_bottom(input_lines, x, y, X_MAX, Y_MAX)
                    + xmas_right_to_left(input_lines, x, y, X_MAX, Y_MAX)
                    + xmas_left_to_right(input_lines, x, y, X_MAX, Y_MAX)
                )

    return result


def mas_right_right(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:
    return (
        x >= 1
        and y >= 1
        and x <= X_MAX - 1
        and y <= Y_MAX - 1
        and input_lines[x - 1][y - 1] == "M"
        and input_lines[x + 1][y - 1] == "M"
        and input_lines[x + 1][y + 1] == "S"
        and input_lines[x - 1][y + 1] == "S"
    )


def mas_right_left(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:
    return (
        x >= 1
        and y >= 1
        and x <= X_MAX - 1
        and y <= Y_MAX - 1
        and input_lines[x - 1][y - 1] == "M"
        and input_lines[x + 1][y - 1] == "S"
        and input_lines[x + 1][y + 1] == "S"
        and input_lines[x - 1][y + 1] == "M"
    )


def mas_left_right(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:
    return (
        x >= 1
        and y >= 1
        and x <= X_MAX - 1
        and y <= Y_MAX - 1
        and input_lines[x - 1][y - 1] == "S"
        and input_lines[x + 1][y - 1] == "M"
        and input_lines[x + 1][y + 1] == "M"
        and input_lines[x - 1][y + 1] == "S"
    )


def mas_left_left(input_lines: list[str], x: int, y: int, X_MAX: int, Y_MAX: int) -> bool:
    return (
        x >= 1
        and y >= 1
        and x <= X_MAX - 1
        and y <= Y_MAX - 1
        and input_lines[x - 1][y - 1] == "S"
        and input_lines[x + 1][y - 1] == "S"
        and input_lines[x + 1][y + 1] == "M"
        and input_lines[x - 1][y + 1] == "M"
    )


def challenge2(data: str) -> int:
    input_lines = data.strip().split("\n")
    X_MAX = len(input_lines) - 1
    Y_MAX = len(input_lines[0]) - 1
    result = 0
    for x, row in enumerate(input_lines):
        for y, char in enumerate(row):
            if char == "A":
                result += (
                    mas_right_right(input_lines, x, y, X_MAX, Y_MAX)
                    + mas_right_left(input_lines, x, y, X_MAX, Y_MAX)
                    + mas_left_right(input_lines, x, y, X_MAX, Y_MAX)
                    + mas_left_left(input_lines, x, y, X_MAX, Y_MAX)
                )

    return result
