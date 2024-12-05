import unittest

from day13 import challenge1, challenge2

test_data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


class TestDay13(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data), 13)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data), 140)


if __name__ == "__main__":
    unittest.main()
