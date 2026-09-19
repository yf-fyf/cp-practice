"""第09回・操作例。二つのうち少なくとも一つを真にする。"""
from z3 import Bool, Or, Solver
from sat_io import report


def build():
    p = Bool('p')
    q = Bool('q')
    s = Solver()
    s.add(Or(p, q))
    return s, {'p': p, 'q': q}


if __name__ == '__main__':
    report(*build())
