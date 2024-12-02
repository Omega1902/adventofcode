import unittest

from day01 import challenge1, challenge2


class TestDay01(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1("data/test_day01.txt"), 11)

    def test_challenge2(self):
        self.assertEqual(challenge2("data/test_day01.txt"), 31)


if __name__ == "__main__":
    unittest.main()
