"""選択T10。A〜Dを一列の四席へ座らせる。"""
from itertools import combinations
from z3 import Ints, Solver, Or, Distinct
from integer_io import report


def build():
    posA, posB, posC, posD = Ints('posA posB posC posD')
    positions = [posA, posB, posC, posD]
    s = Solver()
    # TODO(作業1): 位置1〜4と、全員の位置が異なる条件を書く。
    # TODO(作業2): A・Bの隣接、Cが端、DがAの左という条件を書く。
    return s, dict(zip('ABCD', positions))


if __name__ == '__main__':
    report(*build())
