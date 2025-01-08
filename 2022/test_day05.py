import unittest

from day05 import challenge2

test_data = """
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".strip()


class TestDay05(unittest.TestCase):
    @unittest.skip("NotImplemented")
    def test_challenge1(self):
        # self.assertEqual(challenge1(test_data), 161)
        pass

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data), "HDPNQTHQM")


if __name__ == "__main__":
    unittest.main()
