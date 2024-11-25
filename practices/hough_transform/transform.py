import csv
import threading
from tkinter import filedialog

import numpy as np

base_path = filedialog.askopenfilename()

borders = np.loadtxt(base_path, delimiter=',')
height, width = borders.shape

matrix_votes_1 = np.zeros((height, width), dtype=int)
matrix_votes_2 = np.zeros((height, width), dtype=int)
matrix_votes_3 = np.zeros((height, width), dtype=int)
matrix_votes_4 = np.zeros((height, width), dtype=int)
matrix_votes_avg = np.zeros((height, width), dtype=float)

def check_pixel(y, x, borders, checked_borders, trace_coordinates, coordinates_to_check):
    if borders[y, x] == 1 and not checked_borders[y, x]:
        trace_coordinates.append((y, x))
        coordinates_to_check.append((y, x))
        checked_borders[y, x] = True

def vertical_scan(start_y, end_y, step_y, step_x, matrix_votes):
    checked_borders = np.ones((height, width), dtype=bool)
    checked_borders[borders == 1] = False

    has_unchecked = np.any(~checked_borders)

    while has_unchecked:
        trace_coordinates = []
        coordinates_to_check = []

        for y in range(start_y, end_y, step_y):
            unchecked_x = np.where(~checked_borders[y, :])[0]
            if len(unchecked_x) > 0:
                x = unchecked_x[0] if step_x == 1 else unchecked_x[-1]
                coordinates_to_check.append((y, x))
                checked_borders[y, x] = True
                break

        while coordinates_to_check:
            y, x = coordinates_to_check.pop(0)

            if y > 0:
                if x > 0:
                    check_pixel(y - 1, x - 1, borders, checked_borders, trace_coordinates, coordinates_to_check)
                check_pixel(y - 1, x, borders, checked_borders, trace_coordinates, coordinates_to_check)
                if x < width - 1:
                    check_pixel(y - 1, x + 1, borders, checked_borders, trace_coordinates, coordinates_to_check)

            if x > 0:
                check_pixel(y, x - 1, borders, checked_borders, trace_coordinates, coordinates_to_check)
            if x < width - 1:
                check_pixel(y, x + 1, borders, checked_borders, trace_coordinates, coordinates_to_check)

            if y < height - 1:
                if x > 0:
                    check_pixel(y + 1, x - 1, borders, checked_borders, trace_coordinates, coordinates_to_check)
                check_pixel(y + 1, x, borders, checked_borders, trace_coordinates, coordinates_to_check)
                if x < width - 1:
                    check_pixel(y + 1, x + 1, borders, checked_borders, trace_coordinates, coordinates_to_check)

            matrix_votes[y, x] += len(trace_coordinates)

        has_unchecked = np.any(~checked_borders)

def get_average():
    global matrix_votes_avg
    matrix_votes_avg = (matrix_votes_1 + matrix_votes_2 + matrix_votes_3 + matrix_votes_4) / 4

def horizontal_scan(start_x, end_x, step_x, step_y, matrix_votes):
    checked_borders = np.ones((height, width), dtype=bool)
    checked_borders[borders == 1] = False

    has_unchecked = np.any(~checked_borders)

    while has_unchecked:
        trace_coordinates = []
        coordinates_to_check = []

        for x in range(start_x, end_x, step_x):
            unchecked_y = np.where(~checked_borders[:, x])[0]
            if len(unchecked_y) > 0:
                y = unchecked_y[0] if step_y == 1 else unchecked_y[-1]
                coordinates_to_check.append((y, x))
                checked_borders[y, x] = True
                break

        while coordinates_to_check:
            y, x = coordinates_to_check.pop(0)

            if y > 0:
                if x > 0:
                    check_pixel(y - 1, x - 1, borders, checked_borders, trace_coordinates, coordinates_to_check)
                check_pixel(y - 1, x, borders, checked_borders, trace_coordinates, coordinates_to_check)
                if x < width - 1:
                    check_pixel(y - 1, x + 1, borders, checked_borders, trace_coordinates, coordinates_to_check)

            if x > 0:
                check_pixel(y, x - 1, borders, checked_borders, trace_coordinates, coordinates_to_check)
            if x < width - 1:
                check_pixel(y, x + 1, borders, checked_borders, trace_coordinates, coordinates_to_check)

            if y < height - 1:
                if x > 0:
                    check_pixel(y + 1, x - 1, borders, checked_borders, trace_coordinates, coordinates_to_check)
                check_pixel(y + 1, x, borders, checked_borders, trace_coordinates, coordinates_to_check)
                if x < width - 1:
                    check_pixel(y + 1, x + 1, borders, checked_borders, trace_coordinates, coordinates_to_check)

            matrix_votes[y, x] += len(trace_coordinates)

        has_unchecked = np.any(~checked_borders)

threads = [
    threading.Thread(target=vertical_scan, args=(height - 1, -1, -1,1, matrix_votes_1)),
    threading.Thread(target=vertical_scan, args=(0, height, 1, width - 1, matrix_votes_2)),
    threading.Thread(target=horizontal_scan, args=(width - 1, -1, -1, 0, matrix_votes_3)),
    threading.Thread(target=horizontal_scan, args=(0, width, 1, height - 1, matrix_votes_4))
]

for t in threads:
    t.start()

for t in threads:
    t.join()

get_average()

max_value = matrix_votes_avg.max()
min_value_threshold = max_value / 100

matrix_votes_filtered = np.copy(matrix_votes_avg)
matrix_votes_filtered[matrix_votes_filtered < min_value_threshold] = 0

def guardar_resultado(matrix, nombre):
    with open(f"{nombre}.csv", mode="w", newline="") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerows(matrix)

guardar_resultado(matrix_votes_1, "matriz_votos_1")
guardar_resultado(matrix_votes_2, "matriz_votos_2")
guardar_resultado(matrix_votes_3, "matriz_votos_3")
guardar_resultado(matrix_votes_4, "matriz_votos_4")
guardar_resultado(matrix_votes_avg, "matriz_votos_promedio")
guardar_resultado(matrix_votes_filtered, "matriz_votos")
