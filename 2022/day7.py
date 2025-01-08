from typing import Optional, Union

from utils import get_lines

lines = get_lines("input_day7.txt")


class Directory:
    def __init__(
        self, parent: Optional["Directory"], name: str, children: list[Union["Directory", "File"]] | None = None
    ):
        self.parent = parent
        self.name = name
        self.children = children or []

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)


class File:
    def __init__(self, parent: Directory, name: str, size: int):
        self.parent = parent
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size


def change_directory(line: str, current_directory: Directory) -> Directory:
    directory = line[5:]
    if directory == "/":
        return ROOT
    if directory == "..":
        if current_directory.parent is None:
            raise Exception("ROOT cannot go a directory up")
        return current_directory.parent
    try:
        return next(
            child for child in current_directory.children if child.name == directory and isinstance(child, Directory)
        )
    except IndexError:
        print(line)
        print(directory)
        print(
            [child for child in current_directory.children if child.name == directory and isinstance(child, Directory)]
        )
        raise


ROOT = Directory(None, "root")
current_directory = ROOT

in_ls_mode = False
for line in lines:
    if line.startswith("$ cd"):
        current_directory = change_directory(line, current_directory)
    elif line == "$ ls":
        continue
    elif line.startswith("dir"):
        new_directory = Directory(current_directory, line[4:])
        current_directory.children.append(new_directory)
    else:
        size, name = line.split(" ")
        new_file = File(current_directory, name, int(size))
        current_directory.children.append(new_file)


def find_directories_by_size(current_directory: Directory, threshold: int | None = 100000):
    result = []
    if threshold is None or current_directory.get_size() <= threshold:
        result.append(current_directory)
    for child in current_directory.children:
        if isinstance(child, Directory):
            result.extend(find_directories_by_size(child, threshold))
    return result


r1 = find_directories_by_size(ROOT)
r1 = sum(r.get_size() for r in r1)
print(r1)


total_size = 70_000_000
free_space_needed = 30_000_000
current_size = ROOT.get_size()
current_free = total_size - current_size
to_delete = free_space_needed - current_free
print(f"Currently free: {current_free}, Need {to_delete}")
r2 = find_directories_by_size(ROOT, None)
r2 = [child for child in r2 if child.get_size() > to_delete]
r2 = sorted(r2, key=lambda d: d.get_size())
print(r2[0].get_size())
