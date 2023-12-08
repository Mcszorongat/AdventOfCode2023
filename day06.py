import re
import math


def read_data(filename: str) -> list[list[int]]:
    with open(filename, "r") as f:
        lines = f.read().split("\n")

    return [line.partition(':')[2] for line in lines]


def task1(lines: list[str]) -> int:
    races = list(
        zip(
            [int(number) for number in re.findall(r'[\d]+', lines[0])],
            [int(number) for number in re.findall(r'[\d]+', lines[1])]
        )
    )

    return math.prod([ways_to_beat_race(*race) for race in races])


def ways_to_beat_race(time, distance):
    # f(x) = x * (time - x) - distance = -x^2 + time * x - distance

    D = (time**2 - 4 * -1 * -distance) ** 0.5
    p1 = (-time + D)/(-2)
    p2 = (-time - D)/(-2)
    p1 = int(math.ceil(p1) if p1 % 1 else p1 + 1)
    p2 = int(math.floor(p2) if p2 % 1 else p2 - 1)

    return p2 - p1 + 1


def task2(lines: list[int]) -> int:
    time = int(lines[0].replace(' ', ''))
    distance = int(lines[1].replace(' ', ''))

    return ways_to_beat_race(time, distance)


if __name__ == "__main__":

    lines = read_data("input06.txt")

    print("task1:\t", task1(lines=lines))  # 608902

    print("task2:\t", task2(lines=lines))  # 46173809
