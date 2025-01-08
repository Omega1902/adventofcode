import unittest

from day14 import challenge1

from utils import GridBounds

test_input: str = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip()


class TestDay14(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_input, GridBounds(10, 6)), 12)

    @unittest.skip("Not implemented")
    def test_challenge2(self):
        # self.assertEqual(challenge2(test_input), 1206)
        pass


if __name__ == "__main__":
    unittest.main()
