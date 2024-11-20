"""Tests for the sign_similarity function in the dists module.
"""

import unittest
from stemmadist.dists.signed_similarity.signed_similarity import (
    build_node_paths,
    calculate_distance,
    compute_u,
    compute_roos_similarity,
    roos_similarity,
)
from stemmadist.utils.utils import load_tree


class TestRoosSimilarity(unittest.TestCase):
    """Tests for the Roos similarity function."""

    def setUp(self):
        """Load trees for testing."""
        self.tree_1_str = "((A,B)X,(C,D)Y)Z;"
        self.tree_2_str = "((A,C)X,(B,D)Y)Z;"
        self.tree_3_str = "(((A,B)X,C)Y,D)Z;"
        # Load trees for testing
        self.tree_1 = load_tree(self.tree_1_str)
        self.tree_2 = load_tree(self.tree_2_str)
        self.tree_3 = load_tree(self.tree_3_str)

    def test_build_node_paths(self):
        """Tests that building the node paths behaves as expected."""
        paths = build_node_paths(self.tree_1)

        expected_paths = {
            "Z": ["Z"],
            "X": ["Z", "X"],
            "A": ["Z", "X", "A"],
            "B": ["Z", "X", "B"],
            "Y": ["Z", "Y"],
            "C": ["Z", "Y", "C"],
            "D": ["Z", "Y", "D"],
        }
        self.assertEqual(paths, expected_paths)

    def test_calculate_distance(self):
        """Tests that computing the distance between two nodes behaves as
        expected.
        """
        paths = build_node_paths(self.tree_1)
        distance_AB = calculate_distance(paths, "A", "B")
        distance_AC = calculate_distance(paths, "A", "C")
        self.assertEqual(distance_AB, 2)  # A and B have 2 edges between them
        self.assertEqual(distance_AC, 4)  # A and C are 4 edges apart

    def test_compute_u(self):
        """Tests that computing the u value behaves as expected."""
        tree_paths_1 = build_node_paths(self.tree_1)
        tree_paths_2 = build_node_paths(self.tree_2)
        u_value = compute_u(tree_paths_1, tree_paths_2, "A", "B", "C")
        self.assertIn(u_value, [0, 1])  # u should be either 0 or 1

    def test_compute_roos_similarity(self):
        """Tests that computing the Roos similarity behaves as expected."""
        similarity_score = compute_roos_similarity(self.tree_1, self.tree_2)
        self.assertIsInstance(similarity_score, float)
        self.assertGreaterEqual(similarity_score, 0)
        self.assertAlmostEqual(similarity_score, 0.59, 2)

        # Check with identical trees
        identical_score = compute_roos_similarity(self.tree_1, self.tree_1)
        self.assertEqual(identical_score, 1)

    def test_roos_similarity(self):
        """Tests that computing the Roos similarity between two trees specified
        as string behaves as expected."""
        similarity_score = roos_similarity(self.tree_1_str, self.tree_2_str)
        self.assertIsInstance(similarity_score, float)
        self.assertGreaterEqual(similarity_score, 0)
        self.assertAlmostEqual(similarity_score, 0.59, 2)


if __name__ == "__main__":
    unittest.main()
