import unittest

from day05 import Orders, challenge1, challenge2, check_update_invalid, get_middle_element

test_input: str = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".strip()


class TestDay05(unittest.TestCase):
    def test_order(self):
        order = Orders(1, 2)
        self.assertFalse(order.order_violated([1, 2]))
        self.assertTrue(order.order_violated([2, 1]))
        self.assertFalse(order.order_violated([1, 3]))
        self.assertFalse(order.order_violated([3, 2]))

    def test_check_orders(self):
        orders = (Orders(1, 2), Orders(2, 3), Orders(3, 4))
        self.assertFalse(check_update_invalid(orders, [1, 2, 3, 4]))
        self.assertTrue(check_update_invalid(orders, [1, 4, 3, 4]))
        self.assertFalse(check_update_invalid(orders, [1, 3, 4]))

    def test_get_middle_element(self):
        self.assertEqual(get_middle_element((1, 2, 3, 4, 5, 6, 7)), 4)
        self.assertEqual(get_middle_element((1, 2, 3, 4, 5)), 3)
        self.assertEqual(get_middle_element((1, 2, 3)), 2)

    def test_challenge1(self):
        self.assertEqual(challenge1(test_input), 143)

    def test_challenge2(self):
        self.assertEqual(challenge2(test_input), 123)


if __name__ == "__main__":
    unittest.main()
