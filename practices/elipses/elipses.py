import csv

import cv2
import numpy as np


def build_neighborhood(borders_matrix: np.ndarray[np.float64], pos_y, pos_x) -> np.ndarray[np.float64]:
    mat_height, mat_width = borders_matrix.shape
    neighborhood = np.zeros((3, 3), dtype=np.float64)

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            ny, nx = pos_y + dy, pos_x + dx
            if 0 <= ny < mat_height and 0 <= nx < mat_width:
                neighborhood[dy + 1, dx + 1] = borders_matrix[ny, nx]

    return neighborhood


def is_adjacent(nb: np.ndarray[np.float64], previously: (int, int)):
    for y in range(3):
        row = nb[y]
        for x in range(3):

            if y == 1 and x == 1:
                continue

            if y == previously[0] and x == previously[1]:
                continue

            pixel: float = row[x]

            if pixel == 1.0 or pixel == 255:
                return True, (y, x)

    return False, (-1, -1)


def check_elipses(matrix: np.ndarray[np.float64]):
    pass


def detect_ellipses(image: np.ndarray):
    # Detectar bordes usando el algoritmo de Canny
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
    mat_height, mat_width = edges.shape
    visited = np.zeros_like(edges, dtype=bool)
    ellipses = []

    def dfs(pos_y, pos_x, group):
        """Depth-First Search para encontrar píxeles conectados."""
        stack = [(pos_y, pos_x)]
        while stack:
            y, x = stack.pop()
            if visited[y, x]:
                continue
            visited[y, x] = True
            group.append((x, y))  # Almacenar como (x, y) para OpenCV
            neighborhood = build_neighborhood(edges, y, x)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < mat_height and 0 <= nx < mat_width and not visited[ny, nx]:
                        if neighborhood[dy + 1, dx + 1] == 255:
                            stack.append((ny, nx))

    # Agrupar píxeles conectados
    for y in range(mat_height):
        for x in range(mat_width):
            if (edges[y, x] == 1 or edges[y, x] == 255) and not visited[y, x]:
                group = []
                dfs(y, x, group)
                if len(group) > 10:  # Filtrar contornos muy pequeños
                    ellipses.append(group)

    # Ajustar elipses a cada grupo
    fitted_ellipses = []
    for group in ellipses:
        points = np.array(group, dtype=np.int32)
        if len(points) >= 5:  # Se requieren al menos 5 puntos para ajustar una elipse
            ellipse = cv2.fitEllipse(points)
            fitted_ellipses.append(ellipse)

    return fitted_ellipses


if __name__ == '__main__':

    image = cv2.imread("../../img/spine.webp", cv2.IMREAD_GRAYSCALE)
    detected_ellipses = detect_ellipses(image)

    # Dibujar las elipses detectadas
    output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for ellipse in detected_ellipses:
        cv2.ellipse(output_image, ellipse, (0, 255, 0), 2)

    cv2.imshow("Detected Ellipses", output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()