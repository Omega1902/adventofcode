import unittest

from day03 import challenge1, challenge2

test_data = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip()


class TestDay03(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data), 157)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data), 70)


if __name__ == "__main__":
    unittest.main()
