import re


def read_data(filename: str) -> list[list[int]]:
    colors = [" red", " green", " blue"]

    with open(filename, "r") as f:
        games = [line.split(';') for line in f.read().split("\n")]

    def pattern(x):
        return f'\d+(?={x})'

    def patterns(x):
        return [re.findall(pattern(color), x) or ['0'] for color in colors]

    game_results = [
        [
            [int(res[0]) for res in patterns(result)]
            for result in game
        ] for game in games
    ]

    return game_results


def task1(game_results: list[list[list[int]]]) -> int:
    def possible(results):
        for result in results:
            for ii, jj in zip([12, 13, 14], result):
                if (ii < jj):
                    return False
        return True

    numbers = [ii + 1 for ii,
               game_result in enumerate(game_results) if possible(game_result)]

    return sum(numbers)


def task2(game_results: list[str]) -> int:
    def min_possible(results):
        min = [0, 0, 0]
        for result in results:
            min = [max(ii, jj) for ii, jj in zip(min, result)]
        return min

    minimums = [min_possible(game_result) for game_result in game_results]

    return sum([x[0] * x[1] * x[2] for x in minimums])


if __name__ == "__main__":

    game_results = read_data("input02.txt")

    print("task1:\t", task1(game_results=game_results))  # 2085

    print("task2:\t", task2(game_results=game_results))  # 79315
