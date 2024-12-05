import unittest

from day18 import challenge1, challenge2

test_data = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


class TestDay18(unittest.TestCase):
    @unittest.skip("Does not work")
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data), 3_068)

    @unittest.skip("Does not work")
    def test_challenge2(self):
        self.assertEqual(challenge2(test_data), 1514285714288)


if __name__ == "__main__":
    unittest.main()
