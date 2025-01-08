import unittest

from day01 import challenge1, challenge2

test_input = """
3   4
4   3
2   5
1   3
3   9
3   3
""".strip()


class TestDay01(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_input), 11)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_input), 31)


if __name__ == "__main__":
    unittest.main()
