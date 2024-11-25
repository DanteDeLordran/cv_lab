import unittest
from practices.elipses.elipses import build_neighborhood
import numpy as np


class MyTestCase(unittest.TestCase):

    def test_building_neighborhood_1(self):
        image_example = [
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
        ]

        result_list = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]

        result_arr = np.array(result_list, dtype=np.float64)

        image_matrix = np.array(image_example, dtype=np.float64)

        actual_result = build_neighborhood(image_matrix, 2, 2)

        result = np.array_equal(actual_result, result_arr)

        self.assertEqual(result, True, 'Arrays are not equal')

    def test_building_neighborhood_2(self):
        image_example = [
            [1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ]

        result_list = [
            [1, 0, 0],
            [0, 1, 1],
            [1, 1, 1],
        ]

        result_arr = np.array(result_list, dtype=np.float64)

        image_matrix = np.array(image_example, dtype=np.float64)

        actual_result = build_neighborhood(image_matrix, 1, 1)

        result = np.array_equal(actual_result, result_arr)

        self.assertEqual(result, True, 'Arrays are not equal')

    def test_building_neighborhood_3(self):
        image_example = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ]

        result_list = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]

        result_arr = np.array(result_list, dtype=np.float64)

        image_matrix = np.array(image_example, dtype=np.float64)

        actual_result = build_neighborhood(image_matrix, 2, 2)

        result = np.array_equal(actual_result, result_arr)

        self.assertEqual(result, True, 'Arrays are not equal')


if __name__ == '__main__':
    unittest.main()
