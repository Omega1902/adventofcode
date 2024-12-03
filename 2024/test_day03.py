import unittest

from day03 import challenge1, challenge2


class TestDay03(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1("data/test_day03.txt"), 161)

    def test_challenge2(self):
        self.assertEqual(challenge2("data/test_day03_2.txt"), 48)


if __name__ == "__main__":
    unittest.main()
