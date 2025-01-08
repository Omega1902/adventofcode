import unittest

from day04 import (
    challenge1,
    challenge2,
    mas_left_left,
    mas_left_right,
    mas_right_left,
    mas_right_right,
    xmas_bottom_to_top,
    xmas_left_to_right,
    xmas_right_to_left,
    xmas_to_bottom_left,
    xmas_to_bottom_right,
    xmas_to_top_left,
    xmas_to_top_right,
    xmas_top_to_bottom,
)

test_input: str = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

test_grid: list[str] = test_input.strip().splitlines()

X_MAX = len(test_grid) - 1
Y_MAX = len(test_grid[0]) - 1


class TestDay04(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(xmas_bottom_to_top(test_grid, 4, 6, X_MAX, Y_MAX), 1)
        self.assertEqual(xmas_bottom_to_top(test_grid, 3, 6, X_MAX, Y_MAX), 0)

        self.assertEqual(xmas_top_to_bottom(test_grid, 3, 9, X_MAX, Y_MAX), 1)
        self.assertEqual(xmas_top_to_bottom(test_grid, 3, 8, X_MAX, Y_MAX), 0)

        self.assertEqual(xmas_left_to_right(test_grid, 4, 0, X_MAX, Y_MAX), 1)
        self.assertEqual(xmas_left_to_right(test_grid, 5, 0, X_MAX, Y_MAX), 0)

        self.assertEqual(xmas_right_to_left(test_grid, 1, 4, X_MAX, Y_MAX), 1)
        self.assertEqual(xmas_right_to_left(test_grid, 1, 5, X_MAX, Y_MAX), 0)

        self.assertEqual(xmas_to_top_left(test_grid, X_MAX, Y_MAX, X_MAX, Y_MAX), 1)
        self.assertEqual(xmas_to_top_left(test_grid, 1, 5, X_MAX, Y_MAX), 0)

        self.assertEqual(xmas_to_top_right(test_grid, X_MAX, 1, X_MAX, Y_MAX), 1)
        self.assertEqual(xmas_to_top_right(test_grid, X_MAX, 3, X_MAX, Y_MAX), 1)
        self.assertEqual(xmas_to_top_right(test_grid, X_MAX, 2, X_MAX, Y_MAX), 0)

        self.assertEqual(xmas_to_bottom_right(test_grid, 0, 4, X_MAX, Y_MAX), 1)
        self.assertEqual(xmas_to_bottom_right(test_grid, 1, 5, X_MAX, Y_MAX), 0)

        self.assertEqual(xmas_to_bottom_left(test_grid, 3, Y_MAX, X_MAX, Y_MAX), 1)
        self.assertEqual(xmas_to_bottom_left(test_grid, 1, 5, X_MAX, Y_MAX), 0)

        self.assertEqual(challenge1(test_input), 18)

    def test_challenge2(self):
        self.assertTrue(mas_right_right(test_grid, 1, 2, X_MAX, Y_MAX))
        self.assertFalse(mas_right_right(test_grid, 1, 3, X_MAX, Y_MAX))

        self.assertTrue(mas_left_right(test_grid, 7, 1, X_MAX, Y_MAX))
        self.assertFalse(mas_left_right(test_grid, 1, 3, X_MAX, Y_MAX))

        self.assertTrue(mas_right_left(test_grid, 2, 6, X_MAX, Y_MAX))
        self.assertFalse(mas_right_left(test_grid, 1, 3, X_MAX, Y_MAX))

        self.assertTrue(mas_left_left(test_grid, 3, 4, X_MAX, Y_MAX))
        self.assertFalse(mas_left_left(test_grid, 1, 3, X_MAX, Y_MAX))

        self.assertEqual(challenge2(test_input), 9)


if __name__ == "__main__":
    unittest.main()
