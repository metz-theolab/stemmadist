"""Tests that the Robinsons-Foulds and derivatives distances are computed
correctly."""

import unittest
from stemmadist.dists.rf.rf import rf_distance
from stemmadist.dists.rf.rf_jaccard import rf_jaccard
from stemmadist.dists.rf.matching_split import rf_matching_split


class TestRF(unittest.TestCase):
    """Tests that the Robinsons-Foulds Jaccard distance is computed
    correctly."""

    def setUp(self):
        self.tree_1 = "((A,B)X,(C,D)Y)Z;"
        self.tree_2 = "((A,C)X,(B,D)Y)Z;"

    def test_rf_distance(self):
        """Test that the Robinsons-Foulds Jaccard distance is computed
        correctly.
        """
        self.assertEqual(rf_distance(self.tree_1, self.tree_2), 2)

    def test_rf_distance_self(self):
        """Test that the Robinsons-Foulds Jaccard distance is computed
        correctly for the same tree.
        """
        self.assertEqual(rf_distance(self.tree_1, self.tree_1), 0)

    def test_rf_jaccard(self):
        """Test that the Robinsons-Foulds Jaccard distance is computed
        correctly.
        """
        self.assertEqual(rf_jaccard(self.tree_1, self.tree_2), 0.5)

    def test_rf_jaccard_self(self):
        """Test that the Robinsons-Foulds Jaccard distance is computed
        correctly for the same tree.
        """
        self.assertEqual(rf_jaccard(self.tree_1, self.tree_1), 1)

    def test_rf_matching_split(self):
        """Test that the Robinsons-Foulds Jaccard distance is computed
        correctly.
        """
        from stemmadist.utils.utils import load_tree
        print("\n")
        print(load_tree(self.tree_1).ascii_art())
        print(load_tree(self.tree_2).ascii_art())

        self.assertEqual(rf_matching_split(self.tree_1, self.tree_2), 2)

    def test_rf_matching_split_self(self):
        """Test that the Robinsons-Foulds Jaccard distance is computed
        correctly for the same tree.
        """
        self.assertEqual(rf_matching_split(self.tree_1, self.tree_1), 0)

    def test_rf_matching_split_non_bifid(self):
        """Test that the Robinsons-Foulds Jaccard distance is computed
        correctly for a non bifid tree.
        Taken from the original paper of matching split.
        """
        tree_1_str = "((A,B),(C,F),(D,E));"
        tree_2_str = "((A,C,D,F),(B,E));"
        expected_distance = 3
        self.assertEqual(rf_matching_split(tree_1_str, tree_2_str), expected_distance)


if __name__ == "__main__":
    unittest.main()
