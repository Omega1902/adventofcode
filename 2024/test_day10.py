import unittest

from day10 import challenge1, challenge2

test_input1: str = """
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
""".strip()
test_input2: str = """
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
""".strip()
test_input3: str = """
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
""".strip()
test_input: str = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()

test_input5: str = """
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
""".strip()

test_input6: str = """
012345
123456
234567
345678
4.6789
56789.
""".strip()


class TestDay10(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_input1), 2)
        self.assertEqual(challenge1(test_input2), 4)
        self.assertEqual(challenge1(test_input3), 3)
        self.assertEqual(challenge1(test_input), 36)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_input5), 3)
        self.assertEqual(challenge2(test_input2), 13)
        self.assertEqual(challenge2(test_input6), 227)
        self.assertEqual(challenge2(test_input), 81)


if __name__ == "__main__":
    unittest.main()
