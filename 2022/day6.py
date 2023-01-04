test1 = "bvwbjplbgvbhsrlpgdmjqwftvncz"  # 5
test2 = "nppdvjthqldpwncqszvftbrmjlhg"  # 6
test3 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"  # 10
test4 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"  # 11
test5 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"  # 19
test6 = "bvwbjplbgvbhsrlpgdmjqwftvncz"  # 23
test7 = "nppdvjthqldpwncqszvftbrmjlhg"  # 23
test8 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"  # 29
test9 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"  # 26


def get_data() -> str:
    with open("input_day6.txt") as myfile:
        return myfile.read()


real_data = get_data()


def all_unique(buffer: str) -> bool:
    return len(buffer) == len(set(buffer))


def get_index(data: str) -> int:
    buffer = data[0:4]
    for i, character in enumerate(data[4:], start=5):
        buffer += character
        buffer = buffer[1:]
        if all_unique(buffer):
            return i


def get_index2(data: str) -> int:
    buffer = data[0:14]
    for i, character in enumerate(data[14:], start=15):
        buffer += character
        buffer = buffer[1:]
        if all_unique(buffer):
            return i


print(get_index(test1))
print(get_index(test2))
print(get_index(test3))
print(get_index(test4))
print(get_index(real_data))


print(get_index2(test5))
print(get_index2(test6))
print(get_index2(test7))
print(get_index2(test8))
print(get_index2(test9))
print(get_index2(real_data))
