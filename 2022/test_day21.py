import unittest

from day21 import challenge1, challenge2

test_data = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".strip()


class TestDay21(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data), 152)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data), 301)


if __name__ == "__main__":
    unittest.main()
