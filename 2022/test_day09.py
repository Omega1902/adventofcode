import unittest

from day09 import challenge1, challenge2

test_data1 = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".strip()
test_data2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".strip()


class TestDay09(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data1), 13)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data2), 36)


if __name__ == "__main__":
    unittest.main()
