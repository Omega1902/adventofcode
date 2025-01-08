import re
from typing import Final, NamedTuple

from tqdm import trange


class FutureStones(NamedTuple):
    stones: list[int]
    blinkings: int

    @classmethod
    def generate(cls, stone: int, blinkings: int) -> "FutureStones":
        return cls(blink([stone], blinkings), blinkings)


class BlinkFutures:
    def __init__(self, size: int = 5) -> None:
        self.blink_future: list[list[int]] = [self.gen_blink_future_element() for _ in range(size)]

    @staticmethod
    def gen_blink_future_element() -> list[int]:
        return [0 for _ in range(10)]

    def add(self, blinks: int, stone: int, amount: int = 1) -> None:
        self.blink_future[blinks][stone] += amount

    def apply_first(self) -> None:
        current = self.pop_first()
        for stone, count in enumerate(current):
            self.add_cached(stone, count)

    def pop_first(self) -> list[int]:
        current = self.blink_future.pop(0)
        self.blink_future.append(self.gen_blink_future_element())
        return current

    def add_cached(self, stone: int, amount: int = 1) -> None:
        if amount < 1:
            return
        for future_stone in CACHE[stone]:
            for stones in future_stone.stones:
                self.add(future_stone.blinkings - 1, stones, amount)

    def get_extrapolaited_stones(self) -> int:
        result = 0
        for i, blink_future_element in enumerate(self.blink_future):
            for stone, count in enumerate(blink_future_element):
                if count:
                    result += len(blink([stone], 5 - i)) * count
        return result


def blink(stones: list[int], times: int = 25) -> list[int]:
    for _ in trange(times, delay=0.1):
        new_stones: list[int] = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif (stone_str := str(stone)) and len(stone_str) % 2 == 0:
                middle = len(stone_str) // 2
                new_stones.append(int(stone_str[:middle]))
                new_stones.append(int(stone_str[middle:]))
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
    return stones


# CACHE[0] holds the FutureStones for the stone "0"
# 0 -> 2 0 2 4 in 4 blinks
# 1 -> 2 0 2 4 in 3 blinks
# 2 -> 4 0 4 8 in 3 blinks
# 3 -> 6 0 7 2 in 3 blinks
# 4 -> 8 0 9 6 in 3 blinks
# 5 -> 2, 0, 4, 8, 2, 8, 8, 0 in 5 blinks
# 6 -> 2 4 5 7 9 4 5 6 in 5 blinks
# 7 -> [2, 0, 4, 8, 2, 8, 8, 0] in 5 blinks
# 8 -> [32, 77, 26, 8] in 4 blinks, [3, 2, 7, 7, 2, 6, 16192] in 5 blinks
# 9 -> [3, 6, 8, 6, 9, 1, 8, 4] in 5 blinks
CACHE: Final[tuple[tuple[FutureStones] | tuple[FutureStones, FutureStones], ...]] = (
    (FutureStones.generate(0, 4),),
    (FutureStones.generate(1, 3),),
    (FutureStones.generate(2, 3),),
    (FutureStones.generate(3, 3),),
    (FutureStones.generate(4, 3),),
    (FutureStones.generate(5, 5),),
    (FutureStones.generate(6, 5),),
    (FutureStones.generate(7, 5),),
    (FutureStones([8], 4), FutureStones([3, 2, 7, 7, 2, 6], 5)),
    (FutureStones.generate(9, 5),),
)

# Validate CACHE
for c in CACHE:
    for final_stone in c:
        if final_stone.blinkings > 5:
            raise ValueError(f"Invalid blinkings {final_stone.blinkings} in CACHE")
        for stone in final_stone.stones:
            if stone >= 10:
                raise ValueError(f"Invalid stone {stone} in CACHE")


def blink_cached(stones: list[int], times: int = 25) -> int:
    blink_future = BlinkFutures()

    for _ in trange(times - 5, delay=0.1):
        blink_future.apply_first()
        new_stones: list[int] = []
        for stone in stones:
            if stone < 10:
                blink_future.add_cached(stone)
            elif (stone_str := str(stone)) and len(stone_str) % 2 == 0:
                middle = len(stone_str) // 2
                new_stones.append(int(stone_str[:middle]))
                new_stones.append(int(stone_str[middle:]))
            else:
                new_stones.append(stone * 2024)
        stones = new_stones

    result: int = len(blink(stones, 5))  # Calc remaining stones
    result += blink_future.get_extrapolaited_stones()  # Add stones from the future
    return result


def challenge1(data: str, blinkings: int = 25) -> int:
    stones: list[int] = list(map(int, re.findall(r"\d+", data)))
    return len(blink(stones, blinkings))


def challenge2(data: str, blinkings: int = 75) -> int:
    stones: list[int] = list(map(int, re.findall(r"\d+", data)))
    return blink_cached(stones, blinkings)
