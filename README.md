# adventofcode

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## How to use

1. Check out code
2. `pipenv install`
3. `pipenv shell`
4. Run:
    1. `./main.py 2022 2` for day 2 of 2022
    2. `./main.py` for all days on the default year

## How to develop

1. Check out code
2. `pipenv install -d`
3. `pipenv shell`
4. `pre-commit install`
5. Run tests: `python -m unittest discover -s 2024`


## Download data

1. Install advent-of-code-data (included in `pipenv install -d`)
2. export Session token from Browser: `export AOC_SESSION=cafef00db01dfaceba5eba11deadbeef`
3. `aocd 2 2022 > data/2022/day13.txt`
