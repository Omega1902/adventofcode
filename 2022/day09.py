def move(direction: str, current_position: tuple[int, int]) -> tuple[int, int]:
    if direction == "R":
        return (current_position[0] + 1, current_position[1])
    if direction == "L":
        return (current_position[0] - 1, current_position[1])
    if direction == "U":
        return (current_position[0], current_position[1] + 1)
    if direction == "D":
        return (current_position[0], current_position[1] - 1)
    raise ValueError


def tail_need_to_move(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    return abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1


def tail_new_position(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    x = head[0] - tail[0]
    if x != 0:
        x //= abs(x)
    y = head[1] - tail[1]
    if y != 0:
        y //= abs(y)
    return (tail[0] + x, tail[1] + y)


def challenge1(data: str) -> int:
    head = (0, 0)
    tail = (0, 0)
    positions: set[tuple[int, int]] = {tail}

    for line in data.splitlines():
        direction, amount = line.split(" ")
        for _ in range(int(amount)):
            head_new = move(direction, head)
            if tail_need_to_move(head_new, tail):
                tail = head
                positions.add(tail)
            head = head_new
    return len(positions)


def challenge2(data: str) -> int:
    start = (0, 0)
    head = start
    tails: list[tuple[int, int]] = [start, start, start, start, start, start, start, start, start]
    positions: set[tuple[int, int]] = {start}

    for line in data.splitlines():
        direction, amount = line.split(" ")
        for _ in range(int(amount)):
            head_new = move(direction, head)
            new = [head_new]
            for tail in tails:
                if tail_need_to_move(new[-1], tail):
                    new.append(tail_new_position(new[-1], tail))
                else:
                    break
            head = head_new
            for i, new_pos in enumerate(new[1:]):
                tails[i] = new_pos
            positions.add(tails[-1])
    return len(positions)
