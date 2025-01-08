import unittest

from day12 import challenge1, challenge2

test_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


class TestDay12(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data), 31)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data), 29)


if __name__ == "__main__":
    unittest.main()
