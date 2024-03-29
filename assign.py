from scipy.optimize import linear_sum_assignment
import numpy as np
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Assignment as csv")
parser.add_argument("--output", default="out.csv", help="Output the result assignment as csv")
args = parser.parse_args()


if __name__ == "__main__":
    names = []
    cost = []
    with open(args.input, "rt") as f:
        for row in csv.reader(f):
            names.append(row[0])
            cost.append([float(v) for v in row[1:]])
    cost = np.array(cost)

    print("input:")
    for name, row in zip(names, cost):
        print(f"{name:>10} {row}")

    row_ind, col_ind = linear_sum_assignment(cost, maximize=True)

    ret = np.zeros(cost.shape, dtype=int)
    for y, x in zip(row_ind, col_ind):
        ret[y, x] = 1

    print("assignment:")
    for name, row in zip(names, ret):
        print(f"{name:>10} {row}")

    with open(args.output, "wt") as f:
        writer = csv.writer(f)
        for name, row in zip(names, ret):
            writer.writerow([name] + list(row))