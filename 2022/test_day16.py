import unittest

from day16 import challenge1, challenge2_takes_to_long

test_data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


class TestDay16(unittest.TestCase):
    def test_challenge1(self):
        self.assertEqual(challenge1(test_data), 1_651)

    def test_challenge2(self):
        self.assertEqual(challenge2_takes_to_long(test_data), 1_707)


if __name__ == "__main__":
    unittest.main()
