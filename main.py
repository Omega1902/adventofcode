#! /usr/bin/env python3
import argparse
import importlib
from pathlib import Path
from typing import Literal

SUPPORTED_YEARS = (2024,)


def get_abs_path(filename: str) -> Path:
    return Path(__file__).parent / filename


def get_data(filename: str) -> str:
    return get_abs_path(filename).read_text()


def print_day_result(day: int, challenge: Literal[1] | Literal[2], result: int | float) -> None:
    print(f"Day {day} challenge {challenge}: {result}")


def run_day(year: int, day: int) -> None:
    try:
        day_script = importlib.import_module(f"{year}.day{day:02d}")
    except ModuleNotFoundError:
        print(f"Day {day} not implemented yet")
        return
    try:
        data = get_data(f"data/{year}/input_day{day:02d}.txt")
    except FileNotFoundError:
        print(f"Day {day} input file not found")
        return
    try:
        print_day_result(day, 1, day_script.challenge1(data))
    except (AttributeError, NotImplementedError):
        print(f"Day {day} challenge 1 not implemented yet")

    try:
        print_day_result(day, 2, day_script.challenge2(data))
    except (AttributeError, NotImplementedError):
        print(f"Day {day} challenge 2 not implemented yet")


def main(year: int | None = None, day: int | None = None) -> None:
    if year is None:
        year = SUPPORTED_YEARS[-1]
    if year not in SUPPORTED_YEARS:
        print(f"Invalid year: {year}")
        return

    print(f"Running year {year}:")
    if day is None:
        for i in range(1, 26):
            run_day(year, i)
    elif 1 <= day <= 25:
        run_day(year, day)
    else:
        print(f"Invalid day: {day}")


def wrapped_main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "year", type=int, nargs="?", help=f"Year to run. Choose from: 2024. Default: {SUPPORTED_YEARS[-1]}"
    )
    parser.add_argument("day", type=int, nargs="?", help="Day to run")
    args = parser.parse_args()
    year = args.year
    day = args.day
    if year is not None and year < 100:
        day = year
        year = None
    main(year, day)


if __name__ == "__main__":
    wrapped_main()
