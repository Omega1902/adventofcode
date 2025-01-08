import unittest

from day06 import challenge1, challenge2

test1 = "bvwbjplbgvbhsrlpgdmjqwftvncz"  # 5
test2 = "nppdvjthqldpwncqszvftbrmjlhg"  # 6
test3 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"  # 10
test4 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"  # 11
test5 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"  # 19
test6 = "bvwbjplbgvbhsrlpgdmjqwftvncz"  # 23
test7 = "nppdvjthqldpwncqszvftbrmjlhg"  # 23
test8 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"  # 29
test9 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"  # 26


class TestDay06(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test1), 5)
        self.assertEqual(challenge1(test2), 6)
        self.assertEqual(challenge1(test3), 10)
        self.assertEqual(challenge1(test4), 11)

    def test_challenge2(self):
        self.assertEqual(challenge2(test5), 19)
        self.assertEqual(challenge2(test6), 23)
        self.assertEqual(challenge2(test7), 23)
        self.assertEqual(challenge2(test8), 29)
        self.assertEqual(challenge2(test9), 26)


if __name__ == "__main__":
    unittest.main()
