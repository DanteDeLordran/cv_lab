import numpy as np
from tkinter import filedialog
import matplotlib.pyplot as plt


def ransac_method(votes_matrix: np.ndarray, m_min: int):
    # Filtrar píxeles con votos mayores a m_min
    y_coords, x_coords = np.where(votes_matrix >= m_min)
    votes_filtered = np.array([(x, y, votes_matrix[y, x]) for y, x in zip(y_coords, x_coords)])
    if votes_filtered.size == 0:
        print("No hay suficientes votos.")
        return None, None

    # Ordenar por número de votos (descendente)
    votes_filtered = votes_filtered[votes_filtered[:, 2].argsort()[::-1]]

    # Convertir a enteros
    votes_filtered = votes_filtered.astype(int)

    # Inicializar salidas
    classified = np.zeros_like(votes_matrix)
    unclassified = votes_matrix.copy()

    # Iterar por los pares más votados
    for i, (x1, y1, _) in enumerate(votes_filtered):
        for x2, y2, _ in votes_filtered[i + 1:]:
            if classified[y1, x1] or classified[y2, x2]:
                continue  # Saltar píxeles ya clasificados

            # Calcular línea usando RANSAC (simplificado aquí)
            dx, dy = x2 - x1, y2 - y1
            if dx == 0 or dy == 0:
                continue  # Evitar divisiones por cero

            slope = dy / dx
            intercept = y1 - slope * x1

            # Validar qué puntos están en la línea
            inliers = []
            for x, y, _ in votes_filtered:
                if classified[y, x]:
                    continue  # Ya clasificado
                if abs(y - (slope * x + intercept)) <= 1:  # Tolerancia
                    inliers.append((x, y))

            if len(inliers) >= m_min:
                for x, y in inliers:
                    classified[y, x] = votes_matrix[y, x]
                    unclassified[y, x] = 0

    return classified, unclassified



def __run__():
    file_path = filedialog.askopenfilename()
    votes_matrix = np.loadtxt(file_path, delimiter=",")
    m_min = int(input("Número mínimo de votos: "))

    classified, unclassified = ransac_method(votes_matrix, m_min)
    if classified is not None:
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title("Clasificado como línea recta")
        plt.imshow(classified, cmap="gray")
        plt.subplot(1, 2, 2)
        plt.title("No clasificado")
        plt.imshow(unclassified, cmap="gray")
        plt.show()


if __name__ == "__main__":
    __run__()
