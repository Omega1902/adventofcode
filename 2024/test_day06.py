import unittest

from day06 import challenge1, challenge2

test_input: str = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()


class TestDay05(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_input), 41)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_input), 6)


if __name__ == "__main__":
    unittest.main()
