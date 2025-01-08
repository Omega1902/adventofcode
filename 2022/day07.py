from typing import Optional, Union


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


def change_directory(line: str, current_directory: Directory, root: Directory) -> Directory:
    directory = line[5:]
    if directory == "/":
        return root
    if directory == "..":
        if current_directory.parent is None:
            raise Exception("root cannot go a directory up")
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


def find_directories_by_size(current_directory: Directory, threshold: int | None = 100000):
    result = []
    if threshold is None or current_directory.get_size() <= threshold:
        result.append(current_directory)
    for child in current_directory.children:
        if isinstance(child, Directory):
            result.extend(find_directories_by_size(child, threshold))
    return result


def parse_filesystems(data: str) -> Directory:
    root = Directory(None, "root")
    current_directory = root

    for line in data.splitlines():
        if line.startswith("$ cd"):
            current_directory = change_directory(line, current_directory, root)
        elif line == "$ ls":
            continue
        elif line.startswith("dir"):
            new_directory = Directory(current_directory, line[4:])
            current_directory.children.append(new_directory)
        else:
            size, name = line.split(" ")
            new_file = File(current_directory, name, int(size))
            current_directory.children.append(new_file)
    return root


def challenge1(data: str) -> int:
    root = parse_filesystems(data)
    r1 = find_directories_by_size(root)
    return sum(r.get_size() for r in r1)


def challenge2(data: str) -> int:
    root = parse_filesystems(data)
    total_size = 70_000_000
    free_space_needed = 30_000_000
    current_size = root.get_size()
    current_free = total_size - current_size
    to_delete = free_space_needed - current_free
    r2 = find_directories_by_size(root, None)
    r2 = [child for child in r2 if child.get_size() > to_delete]
    r2 = sorted(r2, key=lambda d: d.get_size())
    return r2[0].get_size()
