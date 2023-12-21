from __future__ import annotations
import copy
import numpy as np


symbol_output_dict = {
    '.': lambda x: [x],
    '|': lambda x: [np.flip(x), -1 * np.flip(x)] if x[1] else [x],
    '\\': lambda x: [np.flip(x)],
    '-': lambda x: [np.flip(x), -1 * np.flip(x)] if x[0] else [x],
    '/': lambda x: [-1 * np.flip(x)],
}


class Beam:
    def __init__(self, direction: np.ndarray[int],
                 destination: np.ndarray[int]) -> None:
        self.direction = direction
        self.destination = destination

    def __eq__(self, __o: Beam) -> bool:
        return np.all(self.direction == __o.direction) and \
            np.all(self.destination == __o.destination)

    def __hash__(self) -> int:
        return tuple(np.concatenate(self.direction, self.destination))

    def __repr__(self) -> str:
        return f"{self.direction} --> {self.destination}"


class Tile:
    def __init__(self, symbol) -> None:
        self.symbol = symbol
        self.out_function = symbol_output_dict[symbol]
        self.energized = False
        self.beams: list[Beam] = []

    def __bool__(self):
        return self.energized

    def __repr__(self) -> str:
        return f"{self.symbol} - {self.energized}"

    def receive_beam(self, beam: Beam):
        if (beam in self.beams):
            return []

        self.energized = True
        self.beams.append(beam)
        out_directions = self.out_function(beam.direction)
        out_beam_maps = map(lambda x: Beam(x, beam.destination + x),
                            out_directions)

        return list(out_beam_maps)


def read_data(filename: str) -> list[list[int]]:
    with open(filename, 'r') as f:
        lines = f.read().split('\n')

    tile_matrix = [[Tile(char) for char in line] for line in lines]

    return np.array(tile_matrix, dtype=Tile)


def task1(tile_matrix: np.ndarray[Tile]) -> int:
    tm = copy.deepcopy(tile_matrix)
    height, width = tm.shape
    beams = [
        Beam(np.array([0, 1]), np.array([0, 0]))
    ]

    while beams:
        beam = beams.pop()
        if (
            (beam.destination[0] < 0 or beam.destination[0] == height) or
            (beam.destination[1] < 0 or beam.destination[1] == width)
        ):
            continue

        beams = beams + tm[*beam.destination].receive_beam(beam)

    return sum([1 for row in tm for tile in row if tile.energized])


def task2(tile_matrix: np.ndarray[Tile]) -> int:

    height, width = tile_matrix.shape
    energized_list = []

    from_left = [Beam(np.array([0, 1]), np.array([ii, 0]))
                 for ii in range(height)]
    from_right = [Beam(np.array([0, -1]), np.array([ii, width - 1]))
                  for ii in range(height)]
    from_top = [Beam(np.array([1, 0]), np.array([0, ii]))
                for ii in range(width)]
    from_bottom = [Beam(np.array([-1, 0]), np.array([height - 1, ii]))
                   for ii in range(width)]

    starting_beams = from_left + from_right + from_top + from_bottom

    for starting_beam in starting_beams:
        tm = copy.deepcopy(tile_matrix)
        beams = [starting_beam]

        while beams:
            beam = beams.pop()
            if (
                (beam.destination[0] < 0 or beam.destination[0] == height) or
                (beam.destination[1] < 0 or beam.destination[1] == width)
            ):
                continue

            beams = beams + tm[*beam.destination].receive_beam(beam)

        energized_list.append(sum([1 for row in tm
                                   for tile in row if tile.energized]))

    return max(energized_list)


if __name__ == "__main__":

    tile_matrix = read_data("input16.txt")

    print("task1:\t", task1(tile_matrix=tile_matrix))  # 7608

    print("task2:\t", task2(tile_matrix=tile_matrix))  # 8221
