# Stemmadist
![Unittest workflow](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)

A Python repository for the distance measurement between trees, implemented in Python. 
While designed to work with computational stemmatology, any tree can be used, as long as it is expressed in the Newick format.

## Basic CLI use
The most basic use of this library is through its CLI, after install, run to obtain the similarity value:

```bash
compute --distance rf --tree1 "((A,B)X,(C,D)Y)Z;" --tree2 "((A,C)X,(B,D)Y)Z;"
```

Among implemented similarities:
- **rf**: Robinson-Foulds distance, a classic measure of tree dissimilarity based on differing splits.
- **rf_jaccard**: Jaccard index of the Robinson-Foulds distance, representing similarity as a ratio.
- **matching_split**: Counts the matching splits between two trees for a measure of similarity.
- **adjacency_matrix**: Distance based on differences in adjacency matrices of the trees.
- **graph_edit_distance**: Measures similarity by the minimal graph edit operations needed to transform one tree into another.
- **signed_similarity**: Measures the signed similarity between two trees.