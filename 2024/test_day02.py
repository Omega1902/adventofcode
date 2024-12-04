import unittest

from day02 import challenge1, challenge2

input_data = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()


class TestDay02(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(input_data), 2)

    def test_challenge2(self):
        self.assertEqual(challenge2(input_data), 4)


if __name__ == "__main__":
    unittest.main()
