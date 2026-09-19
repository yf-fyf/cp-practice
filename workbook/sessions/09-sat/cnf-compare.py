"""発展3の独立確認。学習用ソルバーと小さいCNFの真理値表を照合する。"""
import argparse
from copy import deepcopy
import importlib.util
from itertools import combinations, product
from pathlib import Path
from cnf_tools import satisfies


def compare(solve):
    counts = {}
    for n, limit in [(2, 9), (3, 3)]:
        pool = [[i+1 if state > 0 else -(i+1)
                 for i, state in enumerate(states) if state]
                for states in product((-1, 0, 1), repeat=n)]
        count = 0
        for k in range(limit+1):
            for selection in combinations(pool, k):
                clauses = [list(clause) for clause in selection]
                original = deepcopy(clauses)
                expected = [dict(enumerate(row, 1))
                            for row in product([False, True], repeat=n)
                            if all(any(row[abs(lit)-1] == (lit > 0) for lit in clause)
                                   for clause in clauses)]
                result = solve(n, clauses)
                if clauses != original:
                    raise AssertionError(('入力の破壊', n, original))
                if (result is not None) != bool(expected):
                    raise AssertionError(('判定の不一致', n, original, result))
                if result is not None and not satisfies(n, original, result):
                    raise AssertionError(('代入の不一致', n, original, result))
                count += 1
        counts[n] = count
    return counts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solution')
    args = parser.parse_args()
    path = Path(args.solution).resolve()
    spec = importlib.util.spec_from_file_location('learner_solver', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print('PASS', compare(module.solve))
