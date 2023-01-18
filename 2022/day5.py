from utils import get_lines

stacks = {
    1: [["Z"], ["P"], ["B"], ["Q"], ["M"], ["D"], ["N"]],
    2: [["V"], ["H"], ["D"], ["M"], ["Q"], ["Z"], ["L"], ["C"]],
    3: [["G"], ["Z"], ["F"], ["V"], ["D"], ["R"], ["H"], ["Q"]],
    4: [["N"], ["F"], ["D"], ["G"], ["H"]],
    5: [["Q"], ["F"], ["N"]],
    6: [["T"], ["B"], ["F"], ["Z"], ["V"], ["Q"], ["D"]],
    7: [["H"], ["S"], ["V"], ["D"], ["Z"], ["T"], ["M"], ["Q"]],
    8: [["Q"], ["N"], ["P"], ["F"], ["G"], ["M"]],
    9: [["M"], ["R"], ["W"], ["B"]],
}

stacks_test = {1: [["N"], ["Z"]], 2: [["D"], ["C"], ["M"]], 3: [["P"]]}


def move_stack(stacks: dict[int, list[list[str]]], amount: int, index_from: int, index_to: int):
    moving = stacks[index_from][:amount]
    stacks[index_from] = stacks[index_from][amount:]
    for item in moving:
        stacks[index_to].insert(0, item)


def parse_line(line: str) -> tuple[int, int, int]:
    amount, line = line.split(" from ")
    index_from, index_to = line.split(" to ")
    amount = int(amount.strip("move "))
    index_from = int(index_from)
    index_to = int(index_to)
    return amount, index_from, index_to


test_data = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""".splitlines()

for line in get_lines("input_day5.txt"):
    amount, index_from, index_to = parse_line(line)
    move_stack(stacks, amount, index_from, index_to)
result = "".join(stacks[i][0][0] for i in range(1, 10))
print(result)  # MGDMPSZTM wrong
