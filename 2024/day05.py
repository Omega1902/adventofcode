import re
from collections.abc import Collection


class Orders:
    def __init__(self, first: int, second: int):
        self.first = first
        self.second = second

    def order_violated(self, updates: Collection[int]) -> bool:
        second_first_index = min((i for i, x in enumerate(updates) if x == self.second), default=None)
        if second_first_index is None:
            return False
        first_last_index = max((i for i, x in enumerate(updates) if x == self.first), default=None)
        if first_last_index is None:
            return False
        return second_first_index < first_last_index

    def correct_update(self, updates: list[int]) -> bool:
        second_first_index = min((i for i, x in enumerate(updates) if x == self.second), default=None)
        if second_first_index is None:
            return False
        first_last_index = max((i for i, x in enumerate(updates) if x == self.first), default=None)
        if first_last_index is None:
            return False
        if second_first_index < first_last_index:
            updates[first_last_index], updates[second_first_index] = (
                updates[second_first_index],
                updates[first_last_index],
            )
            return True
        return False


def check_update_invalid(orders: Collection[Orders], update: Collection[int]) -> bool:
    return any(order.order_violated(update) for order in orders)


def parse(data: str) -> tuple[Collection[Orders], list[list[int]]]:
    orders_input, update_input = data.split("\n\n")
    orders: tuple[Orders, ...] = tuple(Orders(int(x[0]), int(x[1])) for x in re.findall(r"(\d+)\|(\d+)", orders_input))
    updates: list[list[int]] = [[int(x) for x in re.findall(r"\d+", update)] for update in update_input.splitlines()]
    return orders, updates


def get_middle_element(update: list[int] | tuple[int, ...]) -> int:
    middle_index = len(update) // 2
    return update[middle_index]


def challenge1(data: str) -> int:
    orders, updates = parse(data)
    return sum(get_middle_element(update) for update in updates if not check_update_invalid(orders, update))


def challenge2(data: str) -> int:
    orders, updates = parse(data)
    invalid_updates = [update for update in updates if check_update_invalid(orders, update)]
    for invalid_update in invalid_updates:
        while any(order.correct_update(invalid_update) for order in orders):
            pass
    return sum(get_middle_element(update) for update in invalid_updates)
