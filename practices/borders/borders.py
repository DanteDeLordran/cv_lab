import csv
import math
import cv2
import numpy as np
import time
from tkinter import filedialog

THRESHOLD = 50

total_start = time.time()
setup_start = time.time()

full_path = filedialog.askopenfilename()
img = cv2.imread(full_path)
height, width, _ = img.shape

num_pixels = height * width

matrix = np.mean(img, axis=2)

matrix_colored = np.full((height, width), False, dtype=bool)
matrix_borders = np.zeros((height, width), dtype=np.float32)

neighborhoods = np.full((height, width), None)
current_nb = 0

setup_end = time.time()
print("Setup:", round(setup_end - setup_start), "seconds")
neighborhoods_start = time.time()

def has_uncolored():
    return not matrix_colored.all()


def when_pixel_applies_to_nb(y: int, x: int):
    matrix_colored[y, x] = True
    matrix_checked[y, x] = True
    neighborhoods[y, x] = current_nb

    if y > 0:
        if x > 0:
            check_nb(y - 1, x - 1)
        check_nb(y - 1, x)
        if x < width - 1:
            check_nb(y - 1, x + 1)

    if x > 0:
        check_nb(y, x - 1)

    if x < width - 1:
        check_nb(y, x + 1)

    if y < height - 1:
        if x > 0:
            check_nb(y + 1, x - 1)
        check_nb(y + 1, x)
        if x < width - 1:
            check_nb(y + 1, x + 1)


def check_nb(y, x):
    if not matrix_checked[y, x] and nb_pivot - THRESHOLD <= matrix[y, x] <= nb_pivot + THRESHOLD:
        matrix_to_check.append((y, x))
    matrix_checked[y, x] = True

def is_border(y, x):
    if y > 0:
        if x > 0 and neighborhoods[y, x] != neighborhoods[y - 1, x - 1]:
            return True
        if neighborhoods[y, x] != neighborhoods[y - 1, x]:
            return True
        if x < width - 1 and neighborhoods[y, x] != neighborhoods[y - 1, x + 1]:
            return True

    if x > 0 and neighborhoods[y, x] != neighborhoods[y, x - 1]:
        return True
    if x < width - 1 and neighborhoods[y, x] != neighborhoods[y, x + 1]:
        return True

    if y < height - 1:
        if x > 0 and neighborhoods[y, x] != neighborhoods[y + 1, x - 1]:
            return True
        if neighborhoods[y, x] != neighborhoods[y + 1, x]:
            return True
        if x < width - 1 and neighborhoods[y, x] != neighborhoods[y + 1, x + 1]:
            return True

    return False

while has_uncolored():
    nb_pivot = None

    if current_nb % 100 == 0:
        num_colored = np.sum(matrix_colored)
        print("Neighborhood progress:", math.floor(100 * num_colored / num_pixels), "%; #", current_nb, end="\r")

    matrix_checked = np.copy(matrix_colored)
    matrix_to_check = []

    for i in range(height):
        if nb_pivot is None:
            for j in range(width):
                if not matrix_colored[i, j]:
                    nb_pivot = matrix[i, j]
                    when_pixel_applies_to_nb(i, j)
                    break

    while len(matrix_to_check) != 0:
        pos_y, pos_x = matrix_to_check.pop(0)
        when_pixel_applies_to_nb(pos_y, pos_x)

    current_nb += 1

num_colored = np.sum(matrix_colored)
print("Neighborhood progress:", math.floor(100 * num_colored / num_pixels), "%; #", current_nb)

neighborhoods_end = time.time()
print("Neighborhoods:", round(neighborhoods_end - neighborhoods_start), "seconds")
borders_start = time.time()

for i in range(height):
    for j in range(width):
        if is_border(i, j):
            matrix_borders[i, j] = 1.0

borders_end = time.time()
print("Borders:", round(borders_end - borders_start), "seconds")

decimal_matrix = matrix / 255.0

with open(f"matriz_gris_.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(decimal_matrix)

with open(f"matriz_vecindarios_.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(neighborhoods)

with open(f"matriz_bordes_.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(matrix_borders)

total_end = time.time()
print("Total:", round(total_end - total_start), "seconds")

cv2.imshow('Imagen Gris', decimal_matrix)
cv2.imshow('Imagen Bordes', matrix_borders)
cv2.waitKey(0)
cv2.destroyAllWindows()