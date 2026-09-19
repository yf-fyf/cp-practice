"""第09回・必修1。E必須、E→C、A→B、B→C、CとDは共存不可。"""
import argparse
from z3 import Bool, And, Not, Implies, Solver
from sat_io import report


def build():
    A = Bool('A')
    B = Bool('B')
    C = Bool('C')
    D = Bool('D')
    E = Bool('E')
    s = Solver()
    # TODO(作業1): 必須はEとし、EからCへの依存を追加する。
    # TODO(作業2): AからB、BからCへの依存と、C・Dの共存不可を追加する。
    return s, {'A': A, 'B': B, 'C': C, 'D': D, 'E': E}


CASES = {
    'A-false': (False, True, True, False, True),
    'A-without-B': (True, False, True, False, True),
    'E-without-C': (False, False, False, False, True),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=tuple(CASES))
    args = parser.parse_args()
    solver, variables = build()
    if args.case:
        for name, value in zip('ABCDE', CASES[args.case]):
            solver.add(variables[name] == value)
    report(solver, variables)


if __name__ == '__main__':
    main()
