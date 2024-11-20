"""Tests the information distance function.
"""

# DEPRECATED in V0.0.0

# import unittest
# import math
# from stemmadist.dists.shared_information.shared_phylogenetic_information \
#     import (
#         double_factorial,
#         P_Phy,
#         phylogenetic_information_content,
#         shared_phylogenetic_information_score,
#         shared_phylogenetic_information,
#         probability_splits
#         )
# from stemmadist.utils.utils import get_unique_values_splits, \
#     are_splits_incompatible


# class TestSharedPhylogneticInformationDistance(unittest.TestCase):
#     """Tests that computation the shared phylogenetic information behaves
#     as expected.
#     """
#     def test_double_factorial(self):
#         self.assertEqual(double_factorial(0), 1)
#         self.assertEqual(double_factorial(1), 1)
#         self.assertEqual(double_factorial(5), 15)  # 5 * 3 * 1
#         self.assertEqual(double_factorial(6), 48)  # 6 * 4 * 2

#     def test_P_Phy(self):
#         split = ({"A", "B"}, {"C", "D"})
#         self.assertAlmostEqual(P_Phy(split), 0.0667, places=4)  # Example value

#     def test_phylogenetic_information_content(self):
#         split = ({"A", "B"}, {"C", "D"})
#         expected_value = -math.log(P_Phy(split))
#         self.assertAlmostEqual(phylogenetic_information_content(split), expected_value, places=4)

#     def test_probability_splits(self):
#         split_1 = ({"A", "B"}, {"C", "D"})
#         split_2 = ({"A"}, {"B", "C", "D"})
#         expected_value = -math.log(probability_splits(split_1, split_2))
#         self.assertAlmostEqual(probability_splits(split_1, split_2), expected_value, places=4)

#     def test_shared_phylogenetic_information_score_compatible(self):
#         split_1 = ({"A", "B"}, {"C", "D"})
#         split_2 = ({"A"}, {"B", "C", "D"})
#         score = shared_phylogenetic_information_score(split_1, split_2)
#         print("!!!!")
#         print(score)
#         self.assertTrue(score > 0)

#     def test_shared_phylogenetic_information_score_incompatible(self):
#         split_1 = ({"A", "B"}, {"C", "D"})
#         split_2 = ({"C"}, {"A", "B", "D"})
#         score = shared_phylogenetic_information_score(split_1, split_2)
#         self.assertEqual(score, 0)

#     def test_shared_phylogenetic_information(self):
#         tree_1 = "((A,B),(C,D));"
#         tree_2 = "((A,C),(B,D));"
#         score = shared_phylogenetic_information(tree_1, tree_2)
#         self.assertTrue(score >= 0)


# if __name__ == "__main__":
#     unittest.main()
