import unittest

from day12 import challenge1, challenge2

test_input: str = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".strip()
test_input1: str = """
AAAA
BBCD
BBCC
EEEC
""".strip()
test_input2: str = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""".strip()
test_input3: str = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
""".strip()
test_input4: str = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
""".strip()


class TestDay12(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_input1), 140)
        self.assertEqual(challenge1(test_input2), 772)
        self.assertEqual(challenge1(test_input), 1930)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_input1), 80)
        self.assertEqual(challenge2(test_input2), 436)
        self.assertEqual(challenge2(test_input3), 236)
        self.assertEqual(challenge2(test_input4), 368)
        self.assertEqual(challenge2(test_input), 1206)


if __name__ == "__main__":
    unittest.main()
