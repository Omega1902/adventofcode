def all_unique(buffer: str) -> bool:
    return len(buffer) == len(set(buffer))


def challenge1(data: str) -> int:
    buffer = data[:4]
    for i, character in enumerate(data[4:], start=5):
        buffer += character
        buffer = buffer[1:]
        if all_unique(buffer):
            return i
    raise ValueError


def challenge2(data: str) -> int:
    buffer = data[:14]
    for i, character in enumerate(data[14:], start=15):
        buffer += character
        buffer = buffer[1:]
        if all_unique(buffer):
            return i
    raise ValueError
