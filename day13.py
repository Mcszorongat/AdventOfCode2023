import numpy as np


def read_data(filename: str) -> list[list[int]]:
    with open(filename, 'r') as f:
        string_matrices = f.read().\
            replace('#', '1').replace('.', '0').split('\n\n')

    matrices = [np.array([[int(char) for char in line]
                          for line in string_matrix.split('\n')], dtype=bool)
                for string_matrix in string_matrices]

    return matrices


def task1(matrices: list[np.ndarray]) -> int:

    def get_value(matrix: np.ndarray):
        for ii in range(1, matrix.shape[0]):
            if np.all(get_folded(matrix, ii) == matrix):
                return ii
        return 0

    return sum([get_value(matrix) * 100 + get_value(matrix.transpose())
                for matrix in matrices])


def get_folded(original: np.ndarray, rows_to_fold):
    top = original[0:rows_to_fold, :]
    mid = np.flipud(original[0:rows_to_fold, :])
    bot = original[2*rows_to_fold:, :]

    return np.vstack((top, mid, bot))[:original.shape[0], :]


def task2(matrices: list[np.ndarray]) -> int:

    def get_value(matrix: np.ndarray):
        for ii in range(1, matrix.shape[0]):
            if (np.sum(np.bitwise_xor(get_folded(matrix, ii), matrix)) == 1):
                return ii
        return 0

    return sum([get_value(matrix) * 100 + get_value(matrix.transpose())
                for matrix in matrices])


if __name__ == "__main__":

    matrices = read_data("input13.txt")

    print("task1:\t", task1(matrices=matrices))  # 34889

    print("task2:\t", task2(matrices=matrices))  # 34224
