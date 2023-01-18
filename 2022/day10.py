from utils import get_lines

lines = get_lines("input_day10.txt")

cur_val = 1
signals = [cur_val]
for line in lines:
    signals.append(cur_val)
    if line.startswith("addx"):
        value = int(line[5:])
        signals.append(cur_val)
        cur_val += value

indexes = list(range(20, 221, 40))

mysum = 0
for index in indexes:
    print(f"Index {index} times value x {signals[index]} is {index * signals[index]}")
    mysum += index * signals[index]
# print(signals)
print(mysum)

bright = "#"
low = "."
CRC = 0
result_screen = ["", "", "", "", "", ""]
screen_index = -1

for signal in signals[1:]:
    if CRC == 0:
        screen_index += 1
    if CRC in (signal, signal + 1, signal - 1):
        result_screen[screen_index] += bright
    else:
        result_screen[screen_index] += low
    CRC += 1
    CRC %= 40

for line in result_screen:
    print(line)
