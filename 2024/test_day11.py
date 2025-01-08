import unittest

from day11 import challenge1, challenge2

test_input: str = "125 17"


class TestDay11(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_input, 6), 22)
        self.assertEqual(challenge1(test_input, 10), 109)
        self.assertEqual(challenge1(test_input), 55_312)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_input, 6), 22)
        self.assertEqual(challenge2(test_input, 10), 109)
        self.assertEqual(challenge2(test_input, 25), 55_312)
        self.assertEqual(challenge2(test_input), 65_601_038_650_482)


if __name__ == "__main__":
    unittest.main()
