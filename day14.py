def read_data(filename: str) -> list[list[int]]:
    with open(filename, 'r') as f:
        lines = f.read().split('\n')

    return rotate_left(lines)


def rotate_left(lines: list[str]):
    return [''.join([line[ii] for line in lines])
            for ii in range(len(lines[0]) - 1, -1, -1)]


def rotate_right(lines: list[str]):
    return [''.join([line[ii] for line in lines[-1::-1]])
            for ii in range(len(lines[0]))]


def task1(lines: list[str]) -> int:
    return sum([calc_line_load(slide_line(line)) for line in lines])


def slide_line(line: str):
    tmp = line
    new_line = ''

    while (tmp):
        part, separator, tmp = tmp.partition('#')

        if (part):
            rock_number = len(part.replace('.', ''))
            line_part = 'O' * rock_number + '.' *\
                (len(part) - rock_number)
            new_line += line_part
        new_line += separator

    return new_line


def calc_line_load(line: str):
    return sum([ii for ii, char in enumerate(line[-1::-1], 1) if char == 'O'])


def task2(lines: list[str]) -> int:
    cycle_goal = 1000000000

    north_line_loads = []
    tmp_lines = lines
    sequence_offset = 0
    sequence_length = 0

    while (not sequence_length):
        tmp_lines = do_tilt_cycle(tmp_lines)
        north_line_loads.append(
            tuple(calc_line_load(line) for line in tmp_lines)
        )
        sequence_offset, sequence_length = search_sequence(north_line_loads)

    minimum_cycles = sequence_offset + sequence_length
    remainder_cycles = (cycle_goal - sequence_offset) % sequence_length

    for _ in range(minimum_cycles + remainder_cycles):
        lines = do_tilt_cycle(lines)

    return sum([calc_line_load(line) for line in lines])


def do_tilt_cycle(lines):
    for _ in range(4):
        lines = rotate_right([slide_line(line) for line in lines])
    return lines


def search_sequence(tuples: list[tuple[int]]):
    data_length = len(tuples)
    if (data_length < 2):
        return 0, 0

    for offset in range(data_length % 2, len(tuples) - 1, 2):
        length = int((data_length - offset) / 2)
        if (compare_tuple_lists(tuples[offset:offset + length],
                                tuples[offset + length::])):
            return offset, length

    return 0, 0


def compare_tuple_lists(list1: list[tuple], list2: list[tuple]):
    for element1, element2 in zip(list1, list2):
        if (element1 != element2):
            return False
    return True


if __name__ == "__main__":

    lines = read_data("input14.txt")

    print("task1:\t", task1(lines=lines))   # 109345

    print("task2:\t", task2(lines=lines))   # 112452
