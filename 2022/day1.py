from utils import get_lines

elves = [[]]
lines = get_lines("input_day1.txt")
for line in lines:
    if line:
        elves[-1].append(int(line))
    else:
        elves.append([])

print(max(map(sum, elves)))
