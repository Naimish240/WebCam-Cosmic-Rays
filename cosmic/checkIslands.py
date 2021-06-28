import numpy as np


def preprocess(arr):
    # Set to 0/1 pixels for island calculations
    b = arr > 0
    b = b.astype(int)

    return b


def dfs(arr, x, y, area=False):
    h, w = arr.shape
    arr[x][y] = 0
    adjacent = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    num = 1

    for row, col in adjacent:
        valid_row = row >= 0 and row < h
        valid_col = col >= 0 and col < w
        if valid_col and valid_row and arr[row][col] == 1:
            num += dfs(arr, row, col)

    return num


def calc(arr):
    # Builds on Island problem
    x, y = arr.shape
    islands = 0
    areas = []

    for i in range(x):
        for j in range(y):
            if arr[i][j] == 1:
                areas.append(dfs(arr, i, j))
                islands += 1
    return islands, areas


def boxes(arr):
    # https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
    pass


def calculate(image):
    binaryImage = preprocess(image)
    islands, areas = calc(binaryImage)
    # box = boxes(image)

    return islands, areas, binaryImage


if __name__ == '__main__':
    arr = np.array([
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1]
    ])

    islands, area = calc(arr)
    print("Islands : ", islands)
    print("Area list: ", area)
