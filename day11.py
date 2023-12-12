import itertools as it


def read_data(filename: str) -> list[list[int]]:
    with open(filename, 'r') as f:
        lines = f.read().replace('.', ' ').split('\n')

    points = [(ii, jj) for ii, line in enumerate(lines)
              for jj, char in enumerate(line) if char == '#']
    empty_row_indices = [ii for ii, line
                         in enumerate(lines) if '#' not in line]
    empty_column_indices = [jj for jj in range(len(lines[0]))
                            if '#' not in ''.join([line[jj]
                                                  for line in lines])]

    horizontal_expansion_list =\
        [len([empty_row_index for empty_row_index in empty_row_indices
              if empty_row_index < ii])
         for ii in range(len(lines[0]))]
    vertical_expansion_list =\
        [len([empty_column_index for empty_column_index in empty_column_indices
              if empty_column_index < ii])
         for ii in range(len(lines))]

    return points, horizontal_expansion_list, vertical_expansion_list


def task1(points, horizontal_expansion_list, vertical_expansion_list) -> int:
    point_groups = generate_point_groups(points)

    distances = map(
        lambda x: expand_and_get_distance(
            x, horizontal_expansion_list, vertical_expansion_list, 2 - 1
        ),
        point_groups
    )

    return sum(distances)


def generate_point_groups(points, group_size=2):
    return list(it.combinations(points, group_size))


def expand_and_get_distance(point_group, horizontal_expansion_list,
                            vertical_expansion_list, expansion_increment):
    expanded_p1 = expand_point(point_group[0], horizontal_expansion_list,
                               vertical_expansion_list, expansion_increment)
    expanded_p2 = expand_point(point_group[1], horizontal_expansion_list,
                               vertical_expansion_list, expansion_increment)
    return get_manhattan_distance(expanded_p1, expanded_p2)


def expand_point(p, horizontal_expansion_list,
                 vertical_expansion_list, expansion_increment):
    x, y = p
    expanded_x = x + horizontal_expansion_list[x] * expansion_increment
    expanded_y = y + vertical_expansion_list[y] * expansion_increment
    return expanded_x, expanded_y


def get_manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def task2(points, horizontal_expansion_list, vertical_expansion_list) -> int:
    point_groups = generate_point_groups(points)

    distances = map(
        lambda x: expand_and_get_distance(
            x, horizontal_expansion_list,
            vertical_expansion_list, 1000000 - 1
        ),
        point_groups
    )

    return sum(distances)


if __name__ == "__main__":

    points, horizontal_expansion_list, vertical_expansion_list =\
        read_data("input11.txt")

    print("task1:\t", task1(points, horizontal_expansion_list,
                            vertical_expansion_list))  # 9521776

    print("task2:\t", task2(points, horizontal_expansion_list,
                            vertical_expansion_list))  # 553224415344
