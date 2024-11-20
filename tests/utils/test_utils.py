"""Tests that the utils functions behave as expected.
"""

import unittest
from stemmadist.utils.utils import (
    load_tree,
    get_nodes,
    get_splits,
    get_unique_values_splits,
    are_splits_incompatible,
)


class TestGraphManipulationUtilities(unittest.TestCase):

    def test_load_tree(self):
        """Tests that loading the tree behaves as expected.
        """
        newick_str = "((A,B),(C,D))R;"
        tree = load_tree(newick_str)
        self.assertEqual(tree.name, "R")
        self.assertEqual(len(tree.descendants), 2)
        self.assertEqual(tree.descendants[0].descendants[0].name, "A")
        self.assertEqual(tree.descendants[1].descendants[1].name, "D")

    def test_get_nodes(self):
        """Tests that getting the nodes behaves as expected."""
        newick_str = "((A,B),(C,D))R;"
        tree = load_tree(newick_str)
        nodes = get_nodes(tree)
        self.assertEqual(nodes, {"A", "B", "C", "D", "R"})

    def test_get_splits(self):
        """Tests that getting the splits behaves as expected."""
        newick_str = "((A,B),(C,D))R;"
        tree = load_tree(newick_str)
        splits = get_splits(tree)
        expected_splits = [({"A", "B"}, {"C", "D"})]
        self.assertEqual(splits, expected_splits)

    def test_get_unique_values_splits(self):
        """Tests that getting the unique values from two splits behaves as
        expected.
        """
        split_1 = [({"A", "B"}, {"C", "D"})]
        split_2 = [({"C", "D"}, {"E", "F"})]
        unique_values = get_unique_values_splits(split_1, split_2)
        self.assertEqual(unique_values, 6)

    def test_are_splits_incompatible(self):
        """Tests the function that checks if two splits are incompatible.
        """
        split_1 = ({"A", "B"}, {"C", "D"})
        split_2 = ({"B", "C"}, {"D", "E"})
        self.assertTrue(are_splits_incompatible(split_1, split_2))

        # Compatible splits
        split_1 = ({"A", "B"}, {"C", "D"})
        split_2 = ({"E", "F"}, {"C", "D"})
        self.assertFalse(are_splits_incompatible(split_1, split_2))


if __name__ == '__main__':
    unittest.main()
