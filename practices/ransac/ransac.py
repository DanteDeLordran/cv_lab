import numpy as np
from tkinter import filedialog
from numpy import ndarray


def ransac_method(votes_matrix: ndarray, m_max: int = 0, threshold: float = 1.0):
    best_line = None
    best_inliers = None

    # Iterate over all pairs of points
    for i in range(len(votes_matrix)):
        for j in range(i + 1, len(votes_matrix)):
            # Define line from points i and j
            p1, p2 = votes_matrix[i], votes_matrix[j]
            A = p2[1] - p1[1]
            B = p1[0] - p2[0]
            C = p2[0] * p1[1] - p1[0] * p2[1]

            # Count inliers within the threshold distance
            M = 0
            inliers = []
            for k in range(len(votes_matrix)):
                point = votes_matrix[k]
                distance = abs(A * point[0] + B * point[1] + C) / np.sqrt(A**2 + B**2)

                if distance < threshold:
                    M += 1
                    inliers.append(point)

            # Update best line if this line has more inliers
            if M > m_max and M >= m_max:
                m_max = M
                best_line = (A, B, C)
                best_inliers = np.array(inliers)

    return best_line, best_inliers


def __run__():
    votes_matrix = np.loadtxt(filedialog.askopenfilename())
    m_max = int(input('Minimum votes number'))
    ransac_method(votes_matrix, m_max)


if __name__ == '__main__':
    __run__()