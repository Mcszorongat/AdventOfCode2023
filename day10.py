from __future__ import annotations
import math
import numpy as np


# F --> \u250C ┌
# 7 --> \u2510 ┐
# L --> \u2514 └
# J --> \u2518 ┘
# - --> \u2500 ─
# | --> \u2502 │
# S --> \u2588 █
# . --> \u0020

symbol_change_dict = {'F': '┌', '7': '┐', 'L': '└', 'J': '┘',
                      '-': '─', '|': '│', 'S': '█', '.': ' '}

symbol_direction_dict = {'┌': [np.array([0, 1]), np.array([1, 0])],
                         '┐': [np.array([0, -1]), np.array([1, 0])],
                         '└': [np.array([0, 1]), np.array([-1, 0])],
                         '┘': [np.array([0, -1]), np.array([-1, 0])],
                         '─': [np.array([0, 1]), np.array([0, -1])],
                         '│': [np.array([1, 0]), np.array([-1, 0])],
                         '█': [np.array([1, 0]), np.array([-1, 0]),
                               np.array([0, 1]), np.array([0, -1])],
                         ' ': []}


def read_data(filename: str) -> list[list[int]]:
    with open(filename, 'r') as f:
        text = f.read()

    for key, value in symbol_change_dict.items():
        text = text.replace(key, value)

    # 0 ── y
    # │
    # x
    return np.array([[char for char in line] for line in text.split('\n')])


def task1(matrix: np.ndarray, print=False) -> int:

    if (print):
        with open("output10_raw.txt", 'w', encoding='utf-8') as f:
            f.write(matrix2text(matrix))

    points_in_path = get_closed_loop(matrix)

    return math.floor(len(points_in_path) / 2)


def matrix2text(matrix: np.ndarray):
    text = '\n'.join([''.join(line) for line in matrix])
    return text


def get_closed_loop(matrix: np.ndarray) -> list[np.ndarray]:
    starting_point = np.array([element[0]
                               for element in np.where(matrix == '█')])

    next_points = get_next_points(matrix, starting_point)

    for next_point in next_points:
        points_in_path = get_points_in_path(matrix, starting_point, next_point)

        # If it ended where it started,
        # assuming there is only one closed loop starting at S.
        if (np.all(points_in_path[-1] == starting_point)):
            break

    return points_in_path[0:-1]


def get_points_in_path(matrix, starting_point, next_point):
    tmp_previous = starting_point
    tmp_current = next_point

    point_log = [starting_point, tmp_current]

    while (not np.all(tmp_current == starting_point)
            and not np.all(tmp_current == np.array([-1, -1]))):
        tmp = get_next_points(matrix, tmp_current, tmp_previous)
        tmp_previous = tmp_current
        tmp_current = tmp[0]
        point_log.append(tmp_current)

    return point_log


def get_next_points(matrix: np.ndarray, current, previous=None):

    current_symbol = matrix[*current][0]
    possible_symbol_directions = symbol_direction_dict[current_symbol]

    possible_next_points = []
    for possible_direction in possible_symbol_directions:
        next_point = current + possible_direction
        # If started on edge or blind path collides with the border of the map.
        if (not in_limits(next_point, matrix.shape)):
            continue
        next_possible_directions = symbol_direction_dict[matrix[*next_point][0]]
        if (not next_possible_directions):
            continue
        possible_previous_points = next_point + next_possible_directions

        if (np.any(np.all(possible_previous_points == current, axis=1))):
            point = possible_direction + current
            if ((previous is not None) and np.all(point == previous)):
                continue
            possible_next_points.append(point)

    if (not possible_symbol_directions):
        return [np.array([-1, -1])]

    return possible_next_points


def in_limits(point, shape) -> bool:
    if ((0 <= point[0] < shape[0]) and (0 <= point[1] < shape[1])):
        return True
    return False


def task2(matrix: np.ndarray, print=False) -> int:
    points_in_path = get_closed_loop(matrix)

    # Replace the starting symbol so it can be handled together with the rest.
    new_starting_symbol = get_starting_symbol(points_in_path[0],
                                              points_in_path[1],
                                              points_in_path[-1])
    matrix[*points_in_path[0]] = new_starting_symbol

    # Counting edge crossings of the closed loop, thus a clean map is required.
    indices = np.array(points_in_path).transpose()
    clean_matrix = np.full_like(matrix, ' ')
    clean_matrix[*indices] = matrix[*indices]

    if (print):
        with open("output10_clean.txt", 'w', encoding='utf-8') as f:
            f.write(matrix2text(clean_matrix))

    # In respect to vertical edge crossings the horizontal edges has no
    # influence, just like the corner changes going back where they came from.
    string_lines = [''.join(line).
                    replace('─', '').
                    replace('└┘', '').
                    replace('└┐', '│').
                    replace('┌┐', '').
                    replace('┌┘', '│')
                    for line in clean_matrix]

    vertical_indices = [[index for index, symbol
                         in enumerate(line) if symbol == '│']
                        for line in string_lines]

    # out --> | <-- in (diff_2k+1) --> | --> out (diff_2k)
    inner_differences = [np.diff(line)[0::2] - 1 for line in vertical_indices]

    return sum([sum(row) for row in inner_differences])


def get_starting_symbol(starting_point, second_point, last_point):
    s_direction = (second_point - starting_point) +\
        (last_point - starting_point)

    if (np.all(s_direction == np.array([0, 0]))):
        return '│'
    else:
        for key, value in symbol_direction_dict.items():
            value_sum = np.sum(np.array(value), axis=0)
            if (np.all(value_sum == s_direction)):
                return key

    raise RuntimeError("No suitable substitute for starting symbol!")


if __name__ == "__main__":

    matrix = read_data("input10.txt")

    print("task1:\t", task1(matrix=matrix))  # 6754

    print("task2:\t", task2(matrix=matrix))  # 567
