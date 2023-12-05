import re


def read_data(filename: str) -> list[list[int]]:
    with open(filename, "r") as f:
        lines = f.read().split("\n")
    return lines


def task1(lines: list[str]) -> int:
    number_lists = [[int(char) for char in line if char.isnumeric()]
                    for line in lines]
    return sum([10 * numbers[0] + numbers[-1] for numbers in number_lists if numbers])


number_map = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
              "six": 6, "seven": 7, "eight": 8, "nine": 9, "1": 1, "2": 2,
              "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}


def task2(lines: list[str]) -> int:
    reduced_lines = [reduce_line(line) for line in lines]
    numbers = [get_number(line) for line in reduced_lines]
    return sum(numbers)


def reduce_line(line: str) -> str:
    matches = list(re.finditer(r'[1-9]', line))
    if (len(matches) > 1):
        p1 = matches[0].span()[1]
        p2 = matches[-1].span()[0]
        p0 = 0 if p1 > 3 else p1 - 1
        p3 = None if len(line) - p2 > 3 else p2 + 1
        line = line[p0:p1] + line[p2:p3]

    return ''.join(line)


def get_number(line: str) -> int:
    indices = [len(line), 0]
    matching_keys = [None, None]

    for key in number_map.keys():
        matches = list(re.finditer(key, line))
        if (len(matches)):
            if (matches[0].span()[0] <= indices[0]):
                indices[0] = matches[0].span()[0]
                matching_keys[0] = key
            if (matches[-1].span()[0] >= indices[1]):
                indices[1] = matches[-1].span()[0]
                matching_keys[1] = key

    return 10 * number_map[matching_keys[0]] + number_map[matching_keys[1]]


if __name__ == "__main__":

    lines = read_data("input01.txt")

    print("task1:\t", task1(lines=lines))  # 53974

    print("task2:\t", task2(lines=lines))  # 52840
