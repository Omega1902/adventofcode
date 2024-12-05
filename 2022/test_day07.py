import unittest

from day07 import challenge1, challenge2

test_data = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip()


class TestDay07(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data), 95437)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_data), 24933642)


if __name__ == "__main__":
    unittest.main()
