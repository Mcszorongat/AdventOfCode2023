from __future__ import annotations
import math
from multiprocessing.pool import ThreadPool


class Node:
    def __init__(self, line) -> None:
        self.name: str = line[0:3]
        self.neighbors: tuple[str] = (line[7:10], line[12:15])
        self.ends_with_A: bool = self.name.endswith('A')
        self.ends_with_Z: bool = self.name.endswith('Z')


def read_data(filename: str) -> tuple[callable[int, int], dict[str, Node]]:
    with open(filename, 'r') as f:
        text = f.read()

    text1, text2 = text.split("\n\n")

    directions = [int(char) for char
                  in text1.replace('L', '0').replace('R', '1')]
    directions_len = len(directions)

    def get_direction(ii):
        return directions[ii % directions_len]

    nodes = [Node(line) for line in text2.split('\n')]

    return get_direction, {node.name: node for node in nodes}


def task1(get_direction: callable[int, int], node_dict: dict[str, Node]) -> int:

    return go_until(get_direction, node_dict,
                    node_dict["AAA"], lambda x: x.name == "ZZZ")


def go_until(get_direction, node_dict, start_node, end_fcn) -> int:
    ii: int = 0
    while (not end_fcn(start_node)):
        start_node = node_dict[
            node_dict[start_node.name].neighbors[get_direction(ii)]
        ]
        ii += 1
    return ii


def task2(get_direction: callable[int, int], node_dict: dict[str, Node]) -> int:
    start_nodes = [node for node in node_dict.values() if node.ends_with_A]

    with ThreadPool(processes=len(start_nodes)) as pool:
        results = pool.starmap(
            go_until,
            [
                (get_direction, node_dict, start_node,
                 lambda x: x.ends_with_Z)
                for start_node in start_nodes
            ]
        )

    return math.lcm(*results)


if __name__ == "__main__":

    get_direction, node_dict = read_data("input08.txt")

    print("task1:\t", task1(get_direction, node_dict))  # 18113

    print("task2:\t", task2(get_direction, node_dict))  # 12315788159977
