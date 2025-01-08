import unittest

from day02 import challenge1, challenge2


class TestDay02(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1("data/test_day02.txt"), 2)

    def test_challenge2(self):
        self.assertEqual(challenge2("data/test_day02.txt"), 4)


if __name__ == "__main__":
    unittest.main()
