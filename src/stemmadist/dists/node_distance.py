import sys


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input tree 1> [<input tree 2>]", file=sys.stderr)
        print(f"Example: {sys.argv[0]} tree1.tre tree2.tre", file=sys.stderr)
        return 1

    if sys.argv[1] in ["-h", "-help", "--help"]:
        print("l1_dist is a program computing L1 distance between two phylogenetic trees.", file=sys.stderr)
        print("Trees should be in Newick format.", file=sys.stderr)
        print("Both trees can be in one file or in separate files.", file=sys.stderr)
        print(f"Usage: {sys.argv[0]} <input file> [<input file 2>]", file=sys.stderr)
        print(f"Example: {sys.argv[0]} tree1.tre tree2.tre", file=sys.stderr)
        return 0

    try:
        with open(sys.argv[1], "r") as inflow:
            newick = ""
            while True:
                c = inflow.read(1)
                if not c or c == ';':
                    break
                if c not in ['\n', '\r']:
                    newick += c

            if not newick:
                print(f"Wrong tree format in \"{sys.argv[1]}\"!", file=sys.stderr)
                return 1

            intree1 = readbrackets(newick)

            if len(sys.argv) > 2:  # second tree is in a separate file
                with open(sys.argv[2], "r") as inflow:
                    newick = ""
                    while True:
                        c = inflow.read(1)
                        if not c or c == ';':
                            break
                        if c not in ['\n', '\r']:
                            newick += c

                    if not newick:
                        if len(sys.argv) > 2:
                            print(f"Wrong tree format in \"{sys.argv[2]}\"!", file=sys.stderr)
                        else:
                            print(f"Only one tree in \"{sys.argv[1]}\"!", file=sys.stderr)
                        return 1

            intree2 = readbrackets(newick)

    except FileNotFoundError:
        print(f"Can not open input file \"{sys.argv[1]}\"!", file=sys.stderr)
        return 1

    n = intree1.leavesnum
    if n == intree2.leavesnum:
        distance = treedist2(intree1, intree2, 1)
    elif n < intree2.leavesnum:
        distance = treedist2(intree1, subtree(intree2, intree1.leaf, n), 1)
    else:
        n = intree2.leavesnum
        distance = treedist2(subtree(intree1, intree2.leaf, n), intree2, 1)

    if distance >= 0:
        print(f"{(distance * 2) / (n * (n - 1)):.4f}")
    else:
        print("1000000")

if __name__ == "__main__":
    main()

