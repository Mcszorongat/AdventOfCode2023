from __future__ import annotations

hash_cache = {}


def read_data(filename: str) -> list[list[int]]:
    with open(filename, 'r') as f:
        steps = f.read().split(',')

    return steps


def task1(steps: list[str]) -> int:
    hashes = [get_hash(step) for step in steps]

    return sum(hashes)


def get_hash(step: str) -> int:
    global hash_cache

    value = hash_cache.get(step) or hash(step)

    if (not step in hash_cache):
        hash_cache[step] = value

    return value


def hash(step: str) -> int:
    current_value = 0
    for char in step:
        current_value += ord(char)
        current_value = current_value * 17 % 256

    return current_value


class Step:
    def __init__(self, step_string: str) -> None:
        label, _, focal_length = step_string.partition('=')
        self.operation = lambda x: x.update({label: int(focal_length)})

        if (not focal_length):
            label, _, _ = step_string.partition('-')
            self.operation = lambda x: x.pop(label, None)

        self.box_index = get_hash(label)


class Box:
    def __init__(self) -> None:
        self.lens_dict = {}

    def do_operation(self, func: callable[dict, None]):
        func(self.lens_dict)

    def get_focal_power(self, box_index: int):
        return sum([(box_index + 1) * slot_number * focal_length
                    for slot_number, focal_length
                    in enumerate(self.lens_dict.values(), 1)])


class BoxRow:
    def __init__(self) -> None:
        self.box_list = [Box() for _ in range(256)]

    def do_step(self, step: Step):
        self.box_list[step.box_index].do_operation(step.operation)

    def get_focal_power(self):
        return sum([box.get_focal_power(box_index)
                    for box_index, box in enumerate(self.box_list)])


def task2(steps: list[str]) -> int:
    _steps: list[Step] = [Step(step_string) for step_string in steps]
    box_row = BoxRow()

    for step in _steps:
        box_row.do_step(step)

    return box_row.get_focal_power()


if __name__ == "__main__":

    steps = read_data("input15.txt")

    print("task1:\t", task1(steps=steps))  # 522547

    print("task2:\t", task2(steps=steps))  # 229271
