def get_lines():
    with open("input_day9.txt") as myfile:
        data = myfile.read()

    return data.split("\n")


lines = get_lines()


def move(direction: str, current_position: tuple[int, int]) -> tuple[int, int]:
    if direction == "R":
        return (current_position[0] + 1, current_position[1])
    if direction == "L":
        return (current_position[0] - 1, current_position[1])
    if direction == "U":
        return (current_position[0], current_position[1] + 1)
    if direction == "D":
        return (current_position[0], current_position[1] - 1)
    raise ValueError()


def tail_need_to_move(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    return abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1


def tail_new_position(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    x = head[0] - tail[0]
    if x != 0:
        x = x / abs(x)
    y = head[1] - tail[1]
    if y != 0:
        y = y / abs(y)
    return (tail[0] + x, tail[1] + y)


def day9_part1():
    head = (0, 0)
    tail = (0, 0)
    positions = set()
    positions.add(tail)

    for line in lines:
        direction, amount = line.split(" ")
        for _ in range(int(amount)):
            head_new = move(direction, head)
            if tail_need_to_move(head_new, tail):
                tail = head
                positions.add(tail)
            head = head_new
    # print(positions)
    print(len(positions))


def day9_part2():
    start = (0, 0)
    head = start
    tails = [start, start, start, start, start, start, start, start, start]
    positions = set()
    positions.add(start)

    for line in lines:
        direction, amount = line.split(" ")
        for _ in range(int(amount)):
            head_new = move(direction, head)
            new = [head_new]
            prev_old = head
            for tail in tails:
                if tail_need_to_move(new[-1], tail):
                    new.append(tail_new_position(new[-1], tail))
                    prev_old = tail
                else:
                    break
            head = head_new
            for i, new_pos in enumerate(new[1:]):
                tails[i] = new_pos
            positions.add(tails[-1])
    # print(positions)
    print(len(positions))


day9_part2()
