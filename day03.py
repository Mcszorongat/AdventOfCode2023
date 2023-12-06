import re
import math
import itertools as it


def read_data(filename: str) -> list[list[int]]:
    with open(filename, "r") as f:
        lines = f.read().split('\n')
    return lines


def task1(lines: list[str]) -> int:
    pattern_symbols = r'[^\d.]'
    pattern_numbers = r'\d+'
    line_n = len(lines)

    symbol_indices_list = [
        [match.start() for match in re.finditer(pattern_symbols, line)]
        for line in lines
    ]

    possible_part_indices_list = [set()] * line_n

    def add_symbol(line, indices) -> None:
        for index in indices:
            possible_part_indices_list[line] =\
                possible_part_indices_list[line] | {index-1, index, index+1}

    for i, symbol_indices in enumerate(symbol_indices_list):
        add_symbol(i, symbol_indices)
        if (i > 0):
            add_symbol(i - 1, symbol_indices)
        if (i < line_n - 1):
            add_symbol(i + 1, symbol_indices)

    number_indices_list = [
        [list(range(*match.span()))
         for match in re.finditer(pattern_numbers, line)]
        for line in lines
    ]

    def is_intersecting(numbers, possible):
        return bool(set(numbers) & possible)

    sum = 0

    for i, [possible_part_indices, number_indices] in enumerate(zip(possible_part_indices_list, number_indices_list)):
        for numbers in number_indices:
            if (is_intersecting(numbers, possible_part_indices)):
                sum += int(lines[i][
                    numbers[0]:
                    (numbers[-1] + 1 if numbers[-1] < len(lines[i]) else None)
                ])

    return sum


def task2(lines: list[str]) -> int:
    pattern_asterix = r'[*]+'
    pattern_numbers = r'\d+'
    line_n = len(lines)

    asterix_indices_list = [
        [(ii, match.start())
         for match in re.finditer(pattern_asterix, line) if match.start()]
        for ii, line in enumerate(lines)
    ]

    number_indices_list = [
        [(int(match.group()), list(zip(it.repeat(ii), range(*match.span()))))
         for match in re.finditer(pattern_numbers, line)]
        for ii, line in enumerate(lines)
    ]

    asterix_coordinates = [
        asterix_index
        for asterix_indices in asterix_indices_list
        for asterix_index in asterix_indices
    ]

    def is_neighbouring(point, array):
        for p in array:
            distance = math.sqrt((p[0] - point[0])**2 + (p[1] - point[1])**2)
            if (distance < 2):
                return True
        return False

    asterix_match_list = [(asterix_coordinate, [])
                          for asterix_coordinate in asterix_coordinates]

    for asterix_match in asterix_match_list:
        valid_limits = [
            asterix_match[0][0] - 1 if asterix_match[0][0]
            else asterix_match[0][0],
            asterix_match[0][0] + 2 if asterix_match[0][0] < line_n
            else asterix_match[0][0]
        ]
        valid_numbers = [
            number
            for numbers in number_indices_list[valid_limits[0]:valid_limits[1]]
            for number in numbers
        ]

        for valid_number in valid_numbers:
            if (is_neighbouring(asterix_match[0], valid_number[1])):
                asterix_match[1].append(valid_number[0])

        gear_ratios = [
            asterix_match[1][0] * asterix_match[1][1]
            for asterix_match in asterix_match_list
            if (len(asterix_match[1]) == 2)
        ]

    return sum(gear_ratios)


if __name__ == "__main__":

    lines = read_data("input03.txt")

    print("task1:\t", task1(lines=lines))  # 546312

    print("task2:\t", task2(lines=lines))  # 87449461
