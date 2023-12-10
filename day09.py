from __future__ import annotations
import numpy as np


def read_data(filename: str) -> list[list[int]]:
    with open(filename, "r") as f:
        lines = f.read().split("\n")

    return [[int(char) for char in line.split()] for line in lines]


def task1(lists: list[list[int]]) -> int:
    return sum([augment(list, -1) for list in lists])


def augment(list, index):
    diffs = [np.array(list)]

    while (len(set(diffs[-1])) != 1):
        diffs.append(np.diff(diffs[-1]))

    numbers_to_sum = [diff[index]*(-1)**(ii * (index + 1))
                      for ii, diff in enumerate(diffs)]

    return sum(numbers_to_sum)


def task2(lists: list[list[int]]) -> int:
    return sum([augment(list, 0) for list in lists])


if __name__ == "__main__":

    lists = read_data("input09.txt")

    print("task1:\t", task1(lists=lists))  # 1904165718

    print("task2:\t", task2(lists=lists))  # 964
