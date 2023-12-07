def read_data(filename: str) -> list[list[int]]:
    with open(filename, "r") as f:
        lines = [line.rpartition(": ")[2] for line in f.read().split("\n")]
    cards_str = [[part.split(" ") for part in line.split(" | ")]
                 for line in lines]
    cards_int = [[set(int(number) for number in side if number) for side in sides]
                 for sides in cards_str]
    return [len(card[0] & card[1]) for card in cards_int]


def task1(overlaps: list[int]) -> int:

    return sum([2**(overlap - 1) for overlap in overlaps if overlap])


def task2(overlaps: list[int]) -> int:
    len_n = len(overlaps)
    overlap_lists = [[overlap] for overlap in overlaps]

    for ii, overlap_list in enumerate(overlap_lists):
        for jj in range(ii + 1, min(ii + 1 + overlap_list[0], len_n + 1)):
            overlap_lists[jj].extend(
                [overlap_lists[jj][0]] * len(overlap_list))

    return sum([len(overlap_list) for overlap_list in overlap_lists])


if __name__ == "__main__":

    overlaps = read_data("input04.txt")

    print("task1:\t", task1(overlaps=overlaps))  # 27845

    print("task2:\t", task2(overlaps=overlaps))  # 9496801
