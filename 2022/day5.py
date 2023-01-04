from pprint import pprint
from collections.abc import Collection

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


def move_stack(stacks: dict[list[list[str]]], amount: int, index_from: int, index_to: int):
    moving = stacks[index_from][0:amount]
    stacks[index_from] = stacks[index_from][amount:]
    for item in moving:
        stacks[index_to].insert(0, item)


def get_lines() -> Collection[str]:
    with open("input_day5.txt") as myfile:
        data = myfile.read()
#     data = """move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2"""
    return data.split("\n")


def parse_line(line: str) -> tuple[int, int, int]:
    amount, line = line.split(" from ")
    index_from, index_to = line.split(" to ")
    amount = int(amount.strip("move "))
    index_from = int(index_from)
    index_to = int(index_to)
    return amount, index_from, index_to


for line in get_lines():
    amount, index_from, index_to = parse_line(line)
    move_stack(stacks, amount, index_from, index_to)
result = ""
for i in range(1, 10):
    result += stacks[i][0][0]
print(result)  # MGDMPSZTM wrong
