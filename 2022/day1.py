with open("input_day1.txt") as myfile:
    data = myfile.read()

elves = [[]]
lines = data.split("\n")
for line in lines:
    if line:
        elves[-1].append(int(line))
    else:
        elves.append([])

print(max(map(sum, elves)))
