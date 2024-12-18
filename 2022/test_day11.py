import unittest

from day11 import challenge2  # , challenge1

test_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


class TestDay11(unittest.TestCase):
    @unittest.skip("Not implemented")
    def test_challenge1(self):
        # self.assertEqual(challenge1(test_data), 10605)
        pass

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data), 2713310158)


if __name__ == "__main__":
    unittest.main()
