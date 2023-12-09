from __future__ import annotations


default_value_dict = {'A': '14', 'K': '13', 'Q': '12', 'J': '11',
                      'T': '10', '9': '09', '8': '08', '7': '07',
                      '6': '06', '5': '05', '4': '04', '3': '03', '2': '02'}


class Hand:
    def __init__(self, line) -> None:
        tmp = line.split(" ")
        self.cards = tmp[0]
        self.bid = int(tmp[1])
        self.combat_power = 0

    def __lt__(self, other: Hand):
        return self.combat_power < other.combat_power

    def init_combat_power(self, value_dict, trump_card=""):
        cards = self.cards.replace(trump_card, "")
        max_occurence =\
            max([list(cards).count(card) for card in cards]) if cards else 0
        different_cards = max(len(set(cards)), 1)
        trump_upgrade = 5 - len(cards)

        power_level = (max_occurence - different_cards) + 5 + trump_upgrade
        base_power = int(''.join([value_dict[card] for card in self.cards]))
        power_up = 10**(5*2)*power_level

        self.combat_power = base_power + power_up


def read_data(filename: str) -> list[list[int]]:
    with open(filename, "r") as f:
        lines = f.read().split("\n")
    hands: list[Hand] = [Hand(line) for line in lines]

    return hands


def task1(hands: list[Hand]) -> int:

    [hand.init_combat_power(default_value_dict) for hand in hands]

    return sum([rank * hand.bid for rank, hand in enumerate(sorted(hands), 1)])


def task2(hands: list[Hand]) -> int:
    new_value_dict = {**default_value_dict, 'J': '01'}

    [hand.init_combat_power(new_value_dict, 'J') for hand in hands]

    return sum([rank * hand.bid for rank, hand in enumerate(sorted(hands), 1)])


if __name__ == "__main__":

    hands = read_data("input07.txt")

    print("task1:\t", task1(hands=hands))  # 251216224

    print("task2:\t", task2(hands=hands))  # 250825971
