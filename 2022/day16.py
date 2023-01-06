import os
import time
from functools import partial
from itertools import combinations
from typing import Any, Iterable

from tqdm import tqdm

test_data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


def timeit(func):
    def inner(*args, **kwargs):
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        stop = time.perf_counter_ns()
        print(f"Process time {(stop-start)/1_000_000_000:.2f} s")
        return result

    return inner


def remove_save_from_list(my_list: list, value: Any):
    try:
        my_list.remove(value)
    except ValueError:
        pass


class Valve:
    def __init__(
        self, name: str, flow_rate: int, tunnel_names: tuple[str, ...], opened: bool = False, my_map: dict = None
    ):
        self.name = name
        self.flow_rate = flow_rate
        self.tunnel_names = tunnel_names
        self.open = opened
        self.my_map = my_map

    @classmethod
    def from_string(cls, description: str):
        description = description.removeprefix("Valve ")
        name, description = description.split(" has flow rate=")
        flow_rate, desription = description.split("; tunnel")
        tunnel_names = desription.removeprefix("s lead to valves ").removeprefix(" leads to valve ")
        return cls(name, int(flow_rate), list(tunnel_names.split(", ")))

    def open_valve(self, minutes: int = None) -> int:
        """If minutes if given, returns the amount of pressure released during that time"""
        if self.open:
            return None if minutes is None else 0
        self.open = True
        return None if minutes is None else minutes * self.flow_rate

    def to_open(self):
        return self.flow_rate > 0 and not self.open

    def copy(self):
        return Valve(self.name, self.flow_rate, self.tunnel_names, self.open, self.my_map)

    def setup_map(self, cave: dict):
        def get_next_tunnels(my_map, counter):
            next_tunnels = (tunnel.tunnel_names for tunnel, value in my_map.items() if value + 1 == counter)
            for tunnels in next_tunnels:
                for tunnel in tunnels:
                    yield tunnel

        my_map = {cave[valve_name]: 1 for valve_name in self.tunnel_names}
        my_map[self] = 0
        counter = 2
        target = list(get_valves_to_open(cave.values()))
        for tunnel in my_map.keys():
            remove_save_from_list(target, tunnel)
        while target:
            next_tunnels = tuple(
                valve for valve_name in get_next_tunnels(my_map, counter) if (valve := cave[valve_name]) not in my_map
            )
            for tunnel in next_tunnels:
                remove_save_from_list(target, tunnel)
                my_map[tunnel] = counter
            if not next_tunnels:
                raise ValueError()
            counter += 1
        self.my_map = {valve.name: value for valve, value in my_map.items()}


def get_abs_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), filename))


def get_data() -> str:
    with open(get_abs_path("input_day16.txt")) as myfile:
        return myfile.read()


def parse_data(data: str) -> tuple[Valve]:
    valves = tuple(map(Valve.from_string, data.splitlines()))
    cave = {valve.name: valve for valve in valves}
    for valve in valves:
        valve.setup_map(cave)
    return cave


def get_valves_to_open(valves: Iterable[Valve]) -> Iterable[Valve]:
    return (valve for valve in valves if valve.to_open())


def copy_cave(cave: dict[str, Valve]) -> dict[str, Valve]:
    return {name: valve.copy() for name, valve in cave.items()}


def current_flow_rate(cave: dict[str, Valve]) -> int:
    return sum(valve.flow_rate for valve in cave.values() if valve.open)


def gen_future(cave: dict[str, Valve], current_valve_name: str, released_pressure: int, minutes: int) -> Iterable[int]:
    return (
        _get_most_pressure_released(copy_cave(cave), current_valve_name, next_target.name, released_pressure, minutes)
        for next_target in get_valves_to_open(cave.values())
    )


def _get_most_pressure_released(
    cave: dict[str, Valve], current_valve_name: str, next_valve: str, released_pressure: int, minutes: int
) -> int:
    travel_and_work_time = cave[current_valve_name].my_map[next_valve] + 1
    travel_and_work_time = min(travel_and_work_time, minutes)
    minutes -= travel_and_work_time
    released_pressure += cave[next_valve].open_valve(minutes)
    # open_valves = tuple(get_valves_to_open(cave.values()))
    # print(
    #     f"{minutes} m left, Opened Valve {next_valve}, already released {released_pressure} pressure"
    #     f", closed valves {len(open_valves)}"
    # )
    if minutes == 0:
        return released_pressure
    # future are all future possible solutions. Might be empty (if get_valves_to_open returns no elements)
    future = gen_future(cave, next_valve, released_pressure, minutes)
    return max(future, default=released_pressure)


@timeit
def get_most_pressure_released(cave: dict[str, Valve]) -> int:
    open_valves = len(tuple(get_valves_to_open(cave.values())))
    print("Valves that should be open:", open_valves)
    return max(tqdm(gen_future(cave, "AA", 0, 30), total=open_valves))


def my_permutations(
    cave: dict[str, Valve], valve_name1: str, valve_name2: str, open_valves: Iterable[Valve]
) -> Iterable[tuple[Valve, Valve]]:
    for target_valve1, target_valve2 in combinations(open_valves, 2):
        if (
            cave[valve_name1].my_map[target_valve1.name] <= cave[valve_name2].my_map[target_valve1.name]
            and cave[valve_name2].my_map[target_valve2.name] <= cave[valve_name1].my_map[target_valve2.name]
        ):
            yield target_valve1, target_valve2
        elif (
            cave[valve_name2].my_map[target_valve1.name] <= cave[valve_name1].my_map[target_valve1.name]
            and cave[valve_name1].my_map[target_valve2.name] <= cave[valve_name2].my_map[target_valve2.name]
        ):
            yield target_valve2, target_valve1
        else:
            yield target_valve1, target_valve2
            yield target_valve2, target_valve1


def gen_future2(
    cave: dict[str, Valve],
    current_valve1: str,
    current_valve2: str,
    next_valve1: str,
    next_valve2: str,
    released_pressure: int,
    minutes: int,
) -> Iterable[int]:
    worker1 = current_valve1 is None
    worker2 = current_valve2 is None
    my_pressure_released = partial(_get_most_pressure_released2, released_pressure=released_pressure, minutes=minutes)
    if worker1 and not worker2:
        return (
            my_pressure_released(copy_cave(cave), next_valve1, current_valve2, next_target.name, next_valve2)
            for next_target in get_valves_to_open(cave.values())
            if next_target.name != next_valve2
        )
    elif worker2 and not worker1:
        return (
            my_pressure_released(copy_cave(cave), current_valve1, next_valve2, next_valve1, next_target.name)
            for next_target in get_valves_to_open(cave.values())
            if next_target.name != next_valve1
        )
    elif worker1 and worker2:
        open_valves = tuple(get_valves_to_open(cave.values()))
        if len(open_valves) <= 1:
            # only one valve left, just send both for that one
            # or nothing to do
            return (
                my_pressure_released(copy_cave(cave), next_valve1, next_valve2, new_valve.name, new_valve.name)
                for new_valve in open_valves
            )
        # if both worker are at the same valve, we do not need to have permutations both way
        select_valves = (
            partial(combinations, r=2)
            if next_valve1 == next_valve2
            else partial(my_permutations, cave, next_valve1, next_valve2)
        )
        return (
            my_pressure_released(copy_cave(cave), next_valve1, next_valve2, new_valve1.name, new_valve2.name)
            for new_valve1, new_valve2 in select_valves(open_valves)
        )
    raise ValueError()  # should not be called without one workers opened a valve


def find_in_between_step(cave: dict[str, Valve], next_valve: str, open_steps: int) -> str:
    for valve, steps in cave[next_valve].my_map.items():
        if steps == open_steps:
            return valve


def get_current_valve_name(
    cave: dict[str, Valve], minutes: int, time_passed: int, time_required: int, target_valve_name: str
):
    """If target is reached, valve gets opened and a new target needs to be find (-> Returns None)
    If not, the worker reached a step inbetween. (-> Return string value)
    """
    if time_required == time_passed:
        return None, cave[target_valve_name].open_valve(minutes)
    return find_in_between_step(cave, target_valve_name, time_required - time_passed - 1), 0


def _get_most_pressure_released2(
    cave: dict[str, Valve],
    current_valve1: str,
    current_valve2: str,
    next_valve1: str,
    next_valve2: str,
    released_pressure: int,
    minutes: int,
) -> int:
    travel_and_work_time1 = cave[current_valve1].my_map[next_valve1] + 1
    travel_and_work_time2 = cave[current_valve2].my_map[next_valve2] + 1
    travel_and_work_time = min(travel_and_work_time1, travel_and_work_time2, minutes)
    minutes -= travel_and_work_time
    if minutes == 0:
        return released_pressure

    process_time_passed = partial(get_current_valve_name, cave, minutes, travel_and_work_time)
    current_valve1, released_pressure_temp1 = process_time_passed(travel_and_work_time1, next_valve1)
    current_valve2, released_pressure_temp2 = process_time_passed(travel_and_work_time2, next_valve2)
    released_pressure += released_pressure_temp1 + released_pressure_temp2
    # open_valves = tuple(get_valves_to_open(cave.values()))
    # print(
    #     f"{minutes} m left, goto Valve {next_valve1}, elephant goes to Valve {next_valve2}, already released "
    #     f"{released_pressure} pressure, closed valves {len(open_valves)}"
    # )
    future = gen_future2(cave, current_valve1, current_valve2, next_valve1, next_valve2, released_pressure, minutes)
    return max(future, default=released_pressure)


@timeit
def get_most_pressure_released2(cave: dict[str, Valve]) -> int:
    open_valves = len(tuple(get_valves_to_open(cave.values())))
    print("Valves that should be open:", open_valves)
    return max(tqdm(gen_future2(cave, None, None, "AA", "AA", 0, 26), total=(open_valves * (open_valves - 1)) // 2))


test_cave = parse_data(test_data)
cave = parse_data(get_data())

assert get_most_pressure_released(test_cave) == 1651
print(get_most_pressure_released(cave))  # takes a couple of minutes

# print(get_most_pressure_released2(test_cave))
assert get_most_pressure_released2(test_cave) == 1707  # currently broken
print(get_most_pressure_released2(cave))  # takes to long to compute
