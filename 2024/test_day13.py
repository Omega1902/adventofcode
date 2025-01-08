import unittest

from day13 import challenge1
from day13 import challenge2_takes_too_long as challenge2

test_input: str = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip()


class TestDay13(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_input), 480)

    @unittest.skip("Takes too long")
    def test_challenge2(self):
        self.assertEqual(challenge2(test_input), 1206)


if __name__ == "__main__":
    unittest.main()
