"""第09回の解説例。A必須、A→B、B→C、CとDは共存不可。"""
import argparse
from z3 import Bool, And, Not, Implies, Solver
from sat_io import report


def build(case='normal'):
    # 手順1　Boolean変数
    A = Bool('A')
    B = Bool('B')
    C = Bool('C')
    D = Bool('D')
    # 手順2　依存と排他
    s = Solver()
    s.add(Implies(A, B), Implies(B, C), Not(And(C, D)))
    if case != 'without-A':
        s.add(A)
    if case == 'with-D':
        s.add(D)
    return s, {'A': A, 'B': B, 'C': C, 'D': D}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=['normal', 'with-D', 'without-A'], default='normal')
    args = parser.parse_args()
    # 手順3　判定と代入の確認
    report(*build(args.case))
