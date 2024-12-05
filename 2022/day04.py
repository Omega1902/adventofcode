from collections.abc import Callable


def contained(elf1_start: int, elf1_stop: int, elf2_start: int, elf2_stop: int) -> bool:
    return elf1_start >= elf2_start and elf1_stop <= elf2_stop


def overlapps(elf1_start: int, elf1_stop: int, elf2_start: int, elf2_stop: int) -> bool:
    if elf1_start == elf2_start or elf1_stop == elf2_stop:
        return True
    if elf1_start < elf2_start:
        return elf1_stop >= elf2_start
    return elf1_start <= elf2_stop


def run(data: str, condition: Callable[[int, int, int, int], bool]) -> int:
    result = 0
    for line in data.splitlines():
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
        if condition(elf1_start, elf1_stop, elf2_start, elf2_stop) or condition(
            elf2_start, elf2_stop, elf1_start, elf1_stop
        ):
            result += 1
    return result


def challenge1(data: str) -> int:
    return run(data, contained)


def challenge2(data: str) -> int:
    return run(data, overlapps)
