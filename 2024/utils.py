from pathlib import Path


def get_abs_path(filename: str) -> Path:
    return Path(__file__).parent / filename


def get_data(filename: str) -> str:
    return get_abs_path(filename).read_text()


def get_lines(filename: str) -> list[str]:
    return get_data(filename).splitlines()
