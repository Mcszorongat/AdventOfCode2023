from __future__ import annotations
import math


class SeedMapRange:
    def __init__(self, destination: int, source: int, length: int) -> None:
        self.source = (source, source + length)
        self.destination = (destination, destination + length)
        self.increment = destination - source

    def __repr__(self) -> str:
        return f"{self.source} --> {self.destination}"

    def __lt__(self, other: SeedMapRange):
        return self.source[0] < other.source[0]

    def in_source(self, number: int):
        return self.source[0] <= number < self.source[1]

    def in_destination(self, number: int):
        return self.destination[0] <= number < self.destination[1]


class SeedMap:
    def __init__(self, seed_map_ranges: list[SeedMapRange]) -> None:
        sorted_ranges = sorted(seed_map_ranges)
        augmenting_ranges = []
        for ii, seed_map_range in enumerate(sorted_ranges[:-1]):
            if (ii == 0 and seed_map_range.source[0] != 0):
                augmenting_ranges.append(
                    SeedMapRange(0, 0, seed_map_range.source[0])
                )
            if (seed_map_range.source[1] != sorted_ranges[ii + 1].source[0]):
                augmenting_ranges.append(
                    SeedMapRange(seed_map_range.source[1],
                                 seed_map_range.source[1],
                                 sorted_ranges[ii + 1].source[0] -
                                 seed_map_range.source[1])
                )
        self.seed_map_ranges = sorted([*seed_map_ranges, *augmenting_ranges])
        if (seed_map_ranges[-1].source[1] < math.inf):
            self.seed_map_ranges.append(
                SeedMapRange(
                    self.seed_map_ranges[-1].source[1],
                    self.seed_map_ranges[-1].source[1],
                    math.inf
                )
            )

    def __add__(self, other: SeedMap):
        seed_map_ranges_a = self.seed_map_ranges
        output_limits_a = [limit
                           for range_a in seed_map_ranges_a
                           for limit in range_a.destination]
        seed_map_ranges_b = other.seed_map_ranges
        input_limits_b = [limit
                          for range_b in seed_map_ranges_b
                          for limit in range_b.source]

        internal_range_limits = sorted(
            list(set([*output_limits_a, *input_limits_b])))

        new_seed_map_ranges = []

        for internal_range_lower_limit in internal_range_limits[:-1]:
            a = self.get_destination_range(internal_range_lower_limit)
            b = other.get_source_range(internal_range_lower_limit)

            source_range_lower_limit = internal_range_lower_limit - a.increment
            destination_range_lower_limit =\
                internal_range_lower_limit + b.increment
            total_length =\
                min(a.destination[1], b.source[1]) - internal_range_lower_limit

            new_seed_map_ranges.append(SeedMapRange(
                destination_range_lower_limit,
                source_range_lower_limit,
                total_length
            ))
        return SeedMap(new_seed_map_ranges)

    def __repr__(self) -> str:
        return " | ".join([seed_map_range.source.__repr__()
                           for seed_map_range in self.seed_map_ranges])

    def get_source_range(self, number):
        return [r for r in self.seed_map_ranges if r.in_source(number)][0]

    def get_destination_range(self, number):
        return [r for r in self.seed_map_ranges if r.in_destination(number)][0]

    def transform_number(self, number):
        return number + self.get_source_range(number).increment

    def transform_range(self, input_range: tuple[int]) -> list[tuple[int]]:
        return [(x1 + smr.increment, x2 + smr.increment)
                for smr in self.seed_map_ranges
                if ((x1 := max(smr.source[0], input_range[0])) -
                    (x2 := min(smr.source[1], input_range[1])) and
                    (x2 - x1 > 0))]


def read_data(filename: str) -> tuple[list[int], SeedMap]:
    with open(filename, "r") as f:
        file = f.read().replace("seeds:", "")
    lines = [
        [line for line in block.split("\n") if ":" not in line]
        for block in file.split("\n\n")
    ]
    seed_numbers = [int(number) for number in lines[0][0].split(" ") if number]
    seed_map_numbers = [
        [
            [int(number) for number in block_part.split(" ")]
            for block_part in map_block
        ]
        for map_block in lines[1:]
    ]

    seed_maps = [
        SeedMap([SeedMapRange(*params) for params in seed_map])
        for seed_map in seed_map_numbers
    ]

    net_map: SeedMap = seed_maps[0]
    for seed_map in seed_maps[1:]:
        net_map = net_map + seed_map

    # seed_map_range < seed_map < seed_maps
    return (seed_numbers, net_map)


def task1(seed_numbers: list[int], seed_map: SeedMap) -> int:

    locations = [seed_map.transform_number(seed_number)
                 for seed_number in seed_numbers]

    return min(locations)


def task2(seed_numbers: list[int], seed_map: SeedMap) -> int:
    seed_ranges = [(start, start + length)
                   for start, length
                   in zip(seed_numbers[0::2], seed_numbers[1::2])]

    location_ranges = [location_range
                       for seed_range in seed_ranges
                       for location_range
                       in seed_map.transform_range(seed_range)]

    return sorted(location_ranges, key=lambda x: x[0])[0][0]


if __name__ == "__main__":

    seed_numbers, seed_map = read_data("input05.txt")

    print("task1:\t", task1(seed_numbers, seed_map))  # 388071289

    print("task2:\t", task2(seed_numbers, seed_map))  # 84206669
