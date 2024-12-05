import unittest

from day14 import challenge1, challenge2

test_data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


class TestDay14(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data), 24)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data), 93)


if __name__ == "__main__":
    unittest.main()
