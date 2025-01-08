import unittest

from day09 import challenge1, challenge2, defragemnt_disk_whole_files, defragment_disk_fragment_files, get_diskspace

test_input: str = "2333133121414131402"


class TestDay09(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(
            get_diskspace(test_input),
            f"{chr(0)*2}...{chr(1)*3}...{chr(2)*1}...{chr(3)*3}.{chr(4)*2}.{chr(5)*4}.{chr(6)*4}.{chr(7)*3}."
            f"{chr(8)*4}{chr(9)*2}",
        )
        self.assertEqual(
            defragment_disk_fragment_files("00...111...2...333.44.5555.6666.777.888899"),
            "0099811188827773336446555566..............",
        )
        self.assertEqual(challenge1(test_input), 1928)

    def test_challenge2(self):
        self.assertEqual(
            defragemnt_disk_whole_files("00...111...2...333.44.5555.6666.777.888899"),
            "00992111777.44.333....5555.6666.....8888..",
        )
        self.assertEqual(challenge2(test_input), 2858)


if __name__ == "__main__":
    unittest.main()
