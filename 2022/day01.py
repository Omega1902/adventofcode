def challenge2(data: str) -> int:
    lines = data.splitlines()
    elves = [[]]
    for line in lines:
        if line:
            elves[-1].append(int(line))
        else:
            elves.append([])

    return max(map(sum, elves))
