def get_lines():
    with open("input_day4.txt") as myfile:
        data = myfile.read()

    return data.split("\n")


lines = get_lines()


def contained(elf1_start: int, elf1_stop: int, elf2_start: int, elf2_stop: int) -> bool:
    return elf1_start >= elf2_start and elf1_stop <= elf2_stop


def overlapps(elf1_start: int, elf1_stop: int, elf2_start: int, elf2_stop: int) -> bool:
    if elf1_start == elf2_start or elf1_stop == elf2_stop:
        return True
    if elf1_start < elf2_start:
        return elf1_stop >= elf2_start
    return elf1_start <= elf2_stop


contained_sum = 0
overlapps_sum = 0
for line in lines:
    if line == "":
        continue
    try:
        elf1, elf2 = line.split(",")
    except ValueError:
        print(line)
        raise
    elf1_start, elf1_stop = elf1.split("-")
    elf2_start, elf2_stop = elf2.split("-")
    elf1_start = int(elf1_start)
    elf1_stop = int(elf1_stop)
    elf2_start = int(elf2_start)
    elf2_stop = int(elf2_stop)
    if contained(elf1_start, elf1_stop, elf2_start, elf2_stop):
        contained_sum += 1
    elif contained(elf2_start, elf2_stop, elf1_start, elf1_stop):
        contained_sum += 1
    if overlapps(elf1_start, elf1_stop, elf2_start, elf2_stop):
        overlapps_sum += 1
    elif overlapps(elf2_start, elf2_stop, elf1_start, elf1_stop):
        overlapps_sum += 1
print(contained_sum)
print(overlapps_sum)  # 958 is to high
