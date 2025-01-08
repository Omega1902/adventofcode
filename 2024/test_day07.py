import unittest

from day07 import challenge1, challenge2, find_solutions, parse_input

test_input: str = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()


class TestDay07(unittest.TestCase):
    def test_challenge1(self):
        parsed = parse_input(test_input)
        self.assertEqual(tuple(next(parsed)), (190, 10, 19))
        self.assertEqual(tuple(next(parsed)), (3267, 81, 40, 27))
        self.assertEqual(find_solutions(190, 10, 19), 190)
        self.assertEqual(find_solutions(3267, 81, 40, 27), 3267)
        self.assertEqual(find_solutions(83, 17, 5), 0)
        self.assertEqual(challenge1(test_input), 3749)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_input), 11387)


if __name__ == "__main__":
    unittest.main()
