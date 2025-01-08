import unittest

from day03 import challenge1, challenge2

test_data1 = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""".strip()

test_data2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""".strip()


class TestDay03(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data1), 161)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data2), 48)


if __name__ == "__main__":
    unittest.main()
