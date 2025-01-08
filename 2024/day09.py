def get_file_id(index: int) -> str:
    # return utf-8 character on given index
    if index >= 46:  # 46 is the index of "." and used to incicate free space
        index += 1
    return chr(index)


def get_index_of_file_id(file_id: str) -> int:
    # return index of utf-8 character
    index = ord(file_id)
    # 46 is the index of "." and used to incicate free space
    return index - 1 if index > 46 else index


def get_diskspace(data: str) -> str:
    disk = ""
    file_id = 0
    for i, char in enumerate(data):
        if i % 2:
            disk += "." * int(char)
        else:
            disk += get_file_id(file_id) * int(char)
            file_id += 1
    return disk


def defragment_disk_fragment_files(disk: str) -> str:
    disk_builder = list(disk)
    pointer1 = find_next_free_space(disk_builder, 0)
    pointer2 = find_previous_file(disk_builder, len(disk) - 1)
    while pointer1 < pointer2:
        disk_builder[pointer1] = disk_builder[pointer2]
        disk_builder[pointer2] = "."
        pointer1 = find_next_free_space(disk_builder, pointer1 + 1)
        pointer2 = find_previous_file(disk_builder, pointer2 - 1)
    return "".join(disk_builder)


def find_next_free_space(disk_builder: list[str], start: int) -> int:
    while disk_builder[start] != ".":
        start += 1
    return start


def find_previous_file(disk_builder: list[str], start: int) -> int:
    while disk_builder[start] == ".":
        start -= 1
    return start


def disk_builder_find_free_space(disk_builder: list[str], size: int, start: int) -> int:
    start_pointer = start
    length = 1
    while disk_builder[start_pointer + length] == ".":
        length += 1
    while length < size:
        start_pointer = find_next_free_space(disk_builder, start_pointer + length)
        length = 1
        while disk_builder[start_pointer + length] == ".":
            length += 1
    return start_pointer


def defragemnt_disk_whole_files(disk: str) -> str:
    disk_builder = list(disk)
    pointer_first_free = find_next_free_space(disk_builder, 0)
    pointer2 = find_previous_file(disk_builder, len(disk) - 1)
    while pointer_first_free < pointer2:
        file_length = 1
        while disk_builder[pointer2 - file_length] == disk_builder[pointer2]:
            file_length += 1

        try:
            start_free_space = disk_builder_find_free_space(disk_builder, file_length, pointer_first_free)
        except IndexError:
            # No free space left, cannot move file. Omit file by only seting pointer2 to the next file
            pass
        else:
            # Only move file if the free space is in front of it
            if start_free_space < pointer2 - file_length:
                for i in range(file_length):
                    disk_builder[start_free_space + i] = disk_builder[pointer2 - i]
                    disk_builder[pointer2 - i] = "."

                pointer_first_free = find_next_free_space(disk_builder, 0)
        pointer2 = find_previous_file(disk_builder, pointer2 - file_length)
    return "".join(disk_builder)


def filesystem_checksum(disk: str) -> int:
    return sum(x * get_index_of_file_id(y) for x, y in enumerate(disk) if y != ".")


def challenge1(data: str) -> int:
    disk = get_diskspace(data.strip())
    disk = defragment_disk_fragment_files(disk)
    return filesystem_checksum(disk)


def challenge2(data: str) -> int:
    disk = get_diskspace(data.strip())
    disk = defragemnt_disk_whole_files(disk)
    return filesystem_checksum(disk)
