"""第09回・必修2。必修1へ独立した新Fを加え、AとFのちょうど一方。"""
import argparse
from z3 import Bool, Or, Not, And
from features_base import build as build_base
from sat_io import report, fix_pair


def build():
    s, variables = build_base()
    A = variables['A']
    F = Bool('F')
    variables['F'] = F
    # TODO(作業1): AとFの少なくとも一方を選ぶ条件を書く。
    # TODO(作業2): AとFを両方選ぶことを禁止する条件を書く。
    return s, variables


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=['normal', 'both-true', 'both-false'], default='normal')
    args = parser.parse_args()
    s, variables = build()
    fix_pair(s, variables, args.case)
    report(s, variables)
