import unittest

from day08 import Point, challenge1, challenge2, find_antinodes

test_input: str = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()


class TestDay07(unittest.TestCase):
    def test_find_antinodes(self):
        tests = (
            ((tuple("...."), tuple("..a."), tuple("..a."), tuple("....")), {Point(2, 0), Point(2, 3)}),
            ((tuple("...."), tuple(".a.."), tuple("..a."), tuple("....")), {Point(0, 0), Point(3, 3)}),
            ((tuple("...."), tuple("..a."), tuple(".a.."), tuple("....")), {Point(3, 0), Point(0, 3)}),
        )
        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(find_antinodes(test[0], {"a"}), test[1])

    def test_challenge1(self):
        self.assertEqual(challenge1(test_input), 14)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_input), 34)


if __name__ == "__main__":
    unittest.main()
