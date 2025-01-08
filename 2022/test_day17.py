import unittest

from day17 import challenge1, challenge2_takes_too_long

test_data = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


class TestDay17(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data), 3_068)

    @unittest.skip("Takes too long")
    def test_challenge2(self):
        self.assertEqual(challenge2_takes_too_long(test_data), 1514285714288)


if __name__ == "__main__":
    unittest.main()
