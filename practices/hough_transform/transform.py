import csv
import numpy as np
import matplotlib.pyplot as plt
import threading
import time

THRESHOLD = 50

base_path = 'C:/Users/jesus/vc-repo/cv_lab/practices/hough_transform/'

borders = np.loadtxt(f"{base_path}matriz_bordes_calle_jpg.csv", delimiter=',')
height, width = borders.shape

matrix_votes_1 = np.zeros((height, width), dtype=int)
checked_borders_1 = np.ones((height, width), dtype=bool)
matrix_votes_2 = np.zeros((height, width), dtype=int)
checked_borders_2 = np.ones((height, width), dtype=bool)
matrix_votes_3 = np.zeros((height, width), dtype=int)
checked_borders_3 = np.ones((height, width), dtype=bool)
matrix_votes_4 = np.zeros((height, width), dtype=int)
checked_borders_4 = np.ones((height, width), dtype=bool)

matrix_votes_avg = np.zeros((height, width), dtype=float)

adjacent_border_counter = 0

def check_pixel(y, x, borders, checked_borders, trace_coordinates, coordinates_to_check):
    global adjacent_border_counter
    if borders[y, x] == 1 and not checked_borders[y, x]:
        adjacent_border_counter += 1
        trace_coordinates.append((y, x))
        coordinates_to_check.append((y, x))
        checked_borders[y, x] = True

def implementacion(start_y, end_y, step_y, start_x, end_x, step_x, matrix_votes, checked_borders):
    global adjacent_border_counter
    print(f"Iniciando implementación de {start_y}-{end_y} y {start_x}-{end_x}...")
    start_time = time.time()

    checked_borders[borders == 1] = False
    has_unchecked = np.any(borders == 1)

    while has_unchecked:
        trace_coordinates = []
        coordinates_to_check = []

        for y in range(start_y, end_y, step_y):
            if step_x == 1:
                x = np.where(~checked_borders[y, :])[0]
            else:
                x = np.where(~checked_borders[y, ::-1])[0]

            if len(x) > 0:
                if step_x == 1:
                    coordinates_to_check.append((y, x[0]))
                else:
                    coordinates_to_check.append((y, width - 1 - x[0]))
                checked_borders[y, coordinates_to_check[-1][1]] = True
                break

        while coordinates_to_check:
            y, x = coordinates_to_check.pop(0)
            adjacent_border_counter = 0

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

            trace_coordinates.append((y, x))
            trace_coordinates = list(dict.fromkeys(trace_coordinates))
            matrix_votes[y, x] += adjacent_border_counter
            for coord in trace_coordinates:
                matrix_votes[coord] += 1

        has_unchecked = np.any(~checked_borders)

    end_time = time.time()
    print(f"Implementación completada en {end_time - start_time:.2f} segundos.")



def implementacion_1():
    implementacion(0, height, 1, 0, width, 1, matrix_votes_1, checked_borders_1)

def implementacion_2():
    implementacion(height-1, -1, -1, width-1, -1, -1, matrix_votes_2, checked_borders_2)

def implementacion_3():
    implementacion(0, height, 1, width-1, -1, -1, matrix_votes_3, checked_borders_3)

def implementacion_4():
    implementacion(height-1, -1, -1, 0, width, 1, matrix_votes_4, checked_borders_4)

def calcular_promedio():
    global matrix_votes_avg
    print("Calculando promedio...")
    start_time = time.time()

    matrix_votes_avg = (matrix_votes_1 + matrix_votes_2 + matrix_votes_3 + matrix_votes_4) / 4

    end_time = time.time()
    print(f"Promedio calculado en {end_time - start_time:.2f} segundos.")

thread_1 = threading.Thread(target=implementacion_1)
thread_2 = threading.Thread(target=implementacion_2)
thread_3 = threading.Thread(target=implementacion_3)
thread_4 = threading.Thread(target=implementacion_4)

print("Iniciando procesamiento concurrente...")
start_time = time.time()
thread_1.start()
thread_2.start()
thread_3.start()
thread_4.start()

thread_1.join()
thread_2.join()
thread_3.join()
thread_4.join()

calcular_promedio()

end_time = time.time()
print(f"Procesamiento concurrente completo en {end_time - start_time:.2f} segundos.")

fig, axes = plt.subplots(1, 5, figsize=(20, 6))

axes[0].imshow(matrix_votes_1, cmap='hot', interpolation='nearest')
axes[0].set_title('Superior Izquierda')

axes[1].imshow(matrix_votes_2, cmap='hot', interpolation='nearest')
axes[1].set_title('Inferior Derecha')

axes[2].imshow(matrix_votes_3, cmap='hot', interpolation='nearest')
axes[2].set_title('Superior Derecha a Inferior Izquierda')

axes[3].imshow(matrix_votes_4, cmap='hot', interpolation='nearest')
axes[3].set_title('Inferior Izquierda a Superior Derecha')

axes[4].imshow(matrix_votes_avg, cmap='hot', interpolation='nearest')
axes[4].set_title('Promedio entre 4 implementaciones')

plt.show()


def guardar_resultado(matrix, nombre):
    with open(f"{base_path}{nombre}.csv", mode="w", newline="") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerows(matrix)


guardar_resultado(matrix_votes_1, "matriz_votos_1")
guardar_resultado(matrix_votes_2, "matriz_votos_2")
guardar_resultado(matrix_votes_3, "matriz_votos_3")
guardar_resultado(matrix_votes_4, "matriz_votos_4")
guardar_resultado(matrix_votes_avg, "matriz_votos_promedio")