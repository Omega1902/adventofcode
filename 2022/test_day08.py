import unittest

from day08 import challenge1, challenge2

test_data = """
30373
25512
65332
33549
35390
""".strip()


class TestDay08(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data), 21)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data), 8)


if __name__ == "__main__":
    unittest.main()
