"""選択M04のZ3版。同じ文字は同じ数字、異なる文字は異なる数字。"""
from z3 import Ints, Solver, Distinct
from integer_io import report


def build():
    S, E, N, D, M, O, R, Y = Ints('S E N D M O R Y')
    letters = [S, E, N, D, M, O, R, Y]
    s = Solver()
    # TODO(作業1): 各数字の範囲、先頭の非ゼロ、八文字の全相異なりを書く。
    # TODO(作業2): SEND・MORE・MONEYを桁の重みで表し、加算等式を書く。
    return s, dict(zip('SENDMORY', letters))


if __name__ == '__main__':
    status, values = report(*build())
    if values is not None:
        number = lambda word: int(''.join(str(values[c]) for c in word))
        print(number('SEND'), '+', number('MORE'), '=', number('MONEY'))
