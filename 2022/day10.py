def create_signals(data: str) -> list[int]:
    cur_val = 1
    signals = [cur_val]
    for line in data.splitlines():
        signals.append(cur_val)
        if line.startswith("addx"):
            value = int(line[5:])
            signals.append(cur_val)
            cur_val += value
    return signals


def challenge1(data: str) -> int:
    signals = create_signals(data)

    indexes = list(range(20, 221, 40))

    mysum = 0
    for index in indexes:
        mysum += index * signals[index]
    return mysum


def challenge2(data: str) -> str:
    signals = create_signals(data)
    bright = "#"
    low = "."
    CRC = 0
    result_screen = ["", "", "", "", "", ""]
    screen_index = -1

    for signal in signals[1:]:
        if CRC == 0:
            screen_index += 1
        if CRC in {signal, signal + 1, signal - 1}:
            result_screen[screen_index] += bright
        else:
            result_screen[screen_index] += low
        CRC += 1
        CRC %= 40

    return "\n" + "\n".join(result_screen)
