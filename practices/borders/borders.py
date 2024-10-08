import csv
import cv2
import numpy as np

THRESHOLD = 70

img = cv2.imread('../../img/screenshot.png')
height, width, _ = img.shape

matrix = np.zeros((height, width))

for i in range(height):
    for j in range(width):
        matrix[i][j] = int(round((int(img[i][j][0]) + int(img[i][j][1]) + int(img[i][j][2])) / 3))

matrix_colored = [[False for _ in range(width)] for _ in range(height)]
matrix_borders = np.zeros((height, width))

neighborhoods = [[None for _ in range(width)] for _ in range(height)]
current_nb = 0


def has_uncolored():
    for row in matrix_colored:
        for is_i_pixel_colored in row:
            if not is_i_pixel_colored:
                return True
    return False


def when_pixel_applies_to_nb(y, x):
    matrix_colored[y][x] = True
    matrix_checked[y][x] = True
    neighborhoods[y][x] = current_nb

    if y > 0:
        if x > 0: check_nb(y - 1, x - 1)
        check_nb(y - 1, x)
        if x < width - 1: check_nb(y - 1, x + 1)

    if x > 0: check_nb(y, x - 1)
    if x < width - 1: check_nb(y, x + 1)

    if y < height - 1:
        if x > 0: check_nb(y + 1, x - 1)
        check_nb(y + 1, x)
        if x < width - 1: check_nb(y + 1, x + 1)


def check_nb(y, x):
    if not matrix_checked[y][x] and nb_pivot - THRESHOLD <= matrix[y][x] <= nb_pivot + THRESHOLD:
        matrix_to_check.append((y, x))
    matrix_checked[y][x] = True


def is_border(y, x):
    if y > 0:
        if x > 0 and neighborhoods[y][x] != neighborhoods[y - 1][x - 1]:
            return True
        if neighborhoods[y][x] != neighborhoods[y - 1][x]:
            return True
        if x < width - 1 and neighborhoods[y][x] != neighborhoods[y - 1][x + 1]:
            return True

    if x > 0 and neighborhoods[y][x] != neighborhoods[y][x - 1]:
        return True
    if x < width - 1 and neighborhoods[y][x] != neighborhoods[y][x + 1]:
        return True

    if y < height - 1:
        if x > 0 and neighborhoods[y][x] != neighborhoods[y + 1][x - 1]:
            return True
        if neighborhoods[y][x] != neighborhoods[y + 1][x]:
            return True
        if x < width - 1 and neighborhoods[y][x] != neighborhoods[y + 1][x + 1]:
            return True

    return False


while has_uncolored():
    nb_pivot = None

    matrix_checked = np.copy(matrix_colored)
    matrix_to_check = []

    for i, row in enumerate(matrix_colored):
        if nb_pivot is None:
            for j, is_i_pixel_colored in enumerate(row):
                if not is_i_pixel_colored:
                    nb_pivot = matrix[i][j]
                    when_pixel_applies_to_nb(i, j)
                    break

    while len(matrix_to_check) != 0:
        y, x = matrix_to_check.pop(0)
        when_pixel_applies_to_nb(y, x)

    current_nb += 1

for i, row in enumerate(neighborhoods):
    for j, pixel in enumerate(row):
        if is_border(i, j):
            matrix_borders[i][j] = 1.

decimal_matrix = np.zeros((height, width))

for i in range(height):
    for j in range(width):
        decimal_matrix[i][j] = matrix[i][j] / 255

with open("matriz_gris.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(decimal_matrix)

cv2.imshow('Imagen Gris', decimal_matrix)
cv2.imshow('Imagen Bordes', matrix_borders)
cv2.waitKey(0)
cv2.destroyAllWindows()
