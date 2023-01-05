import os
from itertools import combinations, permutations
from typing import Iterable

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


class Valve:
    def __init__(self, name: str, flow_rate: int, tunnel_names: tuple[str, ...], opened: bool = False, my_map=None):
        self.name = name
        self.flow_rate = flow_rate
        self.tunnel_names = tunnel_names
        self.tunnels = None
        self.open = opened
        self.my_map = my_map

    @classmethod
    def from_string(cls, description: str):
        description = description.removeprefix("Valve ")
        name, description = description.split(" has flow rate=")
        flow_rate, desription = description.split("; tunnel")
        tunnel_names = desription.removeprefix("s lead to valves ").removeprefix(" leads to valve ")
        return cls(name, int(flow_rate), list(tunnel_names.split(", ")))

    def use_tunnel(self, valve_name: str):
        for tunnel in self.tunnels:
            if valve_name == tunnel.name:
                return tunnel
        raise ValueError()

    def open_valve(self):
        self.open = True

    def to_open(self):
        return self.flow_rate > 0 and not self.open

    def set_tunnels(self, cave: dict):
        self.tunnels = tuple(cave[name] for name in self.tunnel_names)

    def copy(self):
        return Valve(self.name, self.flow_rate, self.tunnel_names, self.open, self.my_map)

    def setup_map(self, cave: dict):
        def get_next_tunnels(my_map, counter):
            next_tunnels = (tunnel.tunnels for tunnel, value in my_map.items() if value + 1 == counter)
            for tunnels in next_tunnels:
                for tunnel in tunnels:
                    yield tunnel

        my_map = {valve: 1 for valve in self.tunnels}
        my_map[self] = 0
        counter = 2
        target = list(get_valves_to_open(cave.values()))
        for tunnel in my_map.keys():
            try:
                target.remove(tunnel)
            except ValueError:
                pass
        while target:
            next_tunnels = tuple(tunnel for tunnel in get_next_tunnels(my_map, counter) if tunnel not in my_map)
            for tunnel in next_tunnels:
                try:
                    target.remove(tunnel)
                except ValueError:
                    pass
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
        valve.set_tunnels(cave)
    for valve in valves:
        valve.setup_map(cave)
    return cave


def get_valves_to_open(valves: Iterable[Valve]) -> Iterable[Valve]:
    return (valve for valve in valves if valve.to_open())


def copy_cave(cave: dict[str, Valve]) -> dict[str, Valve]:
    new_cave = {name: valve.copy() for name, valve in cave.items()}
    for valve in new_cave.values():
        valve.set_tunnels(new_cave)
    return new_cave


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
    released_pressure += current_flow_rate(cave) * travel_and_work_time
    cave[next_valve].open_valve()
    # closed_valves = tuple(get_valves_to_open(cave.values()))
    # print(
    #     f"{minutes} m left, Opened Valve {next_valve}, already released {released_pressure} pressure"
    #     f", closed valves {len(closed_valves)}"
    # )
    if minutes == 0:
        return released_pressure
    # future are all future possible solutions. Might be empty (if get_valves_to_open returns no elements)
    future = gen_future(cave, next_valve, released_pressure, minutes)
    return max(future, default=released_pressure + current_flow_rate(cave) * minutes)


def get_most_pressure_released(cave: dict[str, Valve]) -> int:
    print("Valves that should be open:", len(tuple(get_valves_to_open(cave.values()))))
    return max(tqdm(gen_future(cave, "AA", 0, 30), total=len(tuple(get_valves_to_open(cave.values())))))


def gen_future_two_workers(
    cave: dict[str, Valve],
    current_valve_name1: str,
    current_valve_name2: str,
    next_valve1: str,
    next_valve2: str,
    released_pressure: int,
    minutes: int,
) -> Iterable[int]:
    # worker1 = not cave[next_valve1].open
    # worker2 = not cave[next_valve2].open
    worker1 = current_valve_name1 is None
    worker2 = current_valve_name2 is None
    if worker1 and not worker2:
        return (
            _get_most_pressure_released_two_worker(
                copy_cave(cave),
                next_valve1,
                current_valve_name2,
                next_target.name,
                next_valve2,
                released_pressure,
                minutes,
            )
            for next_target in get_valves_to_open(cave.values())
        )
    elif worker2 and not worker1:
        return (
            _get_most_pressure_released_two_worker(
                copy_cave(cave),
                current_valve_name1,
                next_valve2,
                next_valve1,
                next_target.name,
                released_pressure,
                minutes,
            )
            for next_target in get_valves_to_open(cave.values())
        )
    elif worker1 and worker2:
        valves_to_open = tuple(get_valves_to_open(cave.values()))
        if len(valves_to_open) <= 1:
            # only one valve left, just send both for that one
            # or nothing to do
            return (
                _get_most_pressure_released_two_worker(
                    copy_cave(cave),
                    next_valve1,
                    next_valve2,
                    new_valve.name,
                    new_valve.name,
                    released_pressure,
                    minutes,
                )
                for new_valve in valves_to_open
            )
        # if both worker are at the same valve, we do not need to have permutations both way
        select_valves = combinations if next_valve1 == next_valve2 else permutations
        return (
            _get_most_pressure_released_two_worker(
                copy_cave(cave),
                next_valve1,
                next_valve2,
                new_valve1.name,
                new_valve2.name,
                released_pressure,
                minutes,
            )
            for new_valve1, new_valve2 in select_valves(valves_to_open, 2)
        )
    raise ValueError()  # should not be called without one workers opened a valve


def find_in_between_step(cave: dict[str, Valve], next_valve: str, open_steps: int) -> str:
    for valve in cave.values():
        if valve.my_map[next_valve] == open_steps:
            return valve.name


def _get_most_pressure_released_two_worker(
    cave: dict[str, Valve],
    current_valve_name1: str,
    current_valve_name2: str,
    next_valve1: str,
    next_valve2: str,
    released_pressure: int,
    minutes: int,
) -> int:
    travel_and_work_time1 = cave[current_valve_name1].my_map[next_valve1] + 1
    travel_and_work_time2 = cave[current_valve_name2].my_map[next_valve2] + 1
    travel_and_work_time = min(travel_and_work_time1, travel_and_work_time2, minutes)
    minutes -= travel_and_work_time
    released_pressure += current_flow_rate(cave) * travel_and_work_time
    if minutes == 0:
        return released_pressure

    # one or both workers got their target.
    # If target is reached, valve should be opened and a new target needs to be find.
    # If not, the worker reached a step inbetween. Find out which one
    if travel_and_work_time1 == travel_and_work_time:
        cave[next_valve1].open_valve()
        current_valve_name1 = None
    else:
        current_valve_name1 = find_in_between_step(cave, next_valve1, travel_and_work_time1 - travel_and_work_time - 1)
    if travel_and_work_time2 == travel_and_work_time:
        cave[next_valve2].open_valve()
        current_valve_name2 = None
    else:
        current_valve_name2 = find_in_between_step(cave, next_valve2, travel_and_work_time2 - travel_and_work_time - 1)

    future = gen_future_two_workers(
        cave, current_valve_name1, current_valve_name2, next_valve1, next_valve2, released_pressure, minutes
    )
    return max(future, default=released_pressure + current_flow_rate(cave) * minutes)


def get_most_pressure_released_two_worker(cave: dict[str, Valve]) -> int:
    valves_to_open = len(tuple(get_valves_to_open(cave.values())))
    print("Valves that should be open:", valves_to_open)

    return max(
        tqdm(
            gen_future_two_workers(cave, None, None, "AA", "AA", 0, 26),
            total=(valves_to_open * (valves_to_open - 1)) // 2,
        )
    )


test_cave = parse_data(test_data)
cave = parse_data(get_data())

assert get_most_pressure_released(test_cave) == 1651
print(get_most_pressure_released(cave))  # takes a couple of minutes

assert get_most_pressure_released_two_worker(test_cave) == 1707
print(get_most_pressure_released_two_worker(cave))  # takes to long to compute
