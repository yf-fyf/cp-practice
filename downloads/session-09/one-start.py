"""発展1。n候補からちょうど一つを選ぶ。"""
import argparse
from itertools import combinations
from z3 import Bool, Or, Not, And, Solver
from sat_io import report


def build(n=5):
    if n < 0:
        raise ValueError('候補数は非負')
    variables = {f'X{i+1}': Bool(f'X{i+1}') for i in range(n)}
    candidates = list(variables.values())
    s = Solver()
    # TODO(作業1): candidatesの少なくとも一つを選ぶ条件を書く。
    for left, right in combinations(candidates, 2):
        # TODO(作業2): このペアの両方を選ぶことを禁止する。
        pass
    return s, variables


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('n', nargs='?', type=int, default=5)
    args = parser.parse_args()
    report(*build(args.n))
