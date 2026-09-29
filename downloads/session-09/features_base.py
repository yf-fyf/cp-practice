"""必修2・発展2の完成した出発点。E必須、E→C、A→B、B→C、CとDは共存不可。"""
from z3 import Bool, And, Not, Implies, Solver
from sat_io import report


def build():
    A = Bool('A')
    B = Bool('B')
    C = Bool('C')
    D = Bool('D')
    E = Bool('E')
    s = Solver()
    s.add(E, Implies(E, C))
    s.add(Implies(A, B), Implies(B, C), Not(And(C, D)))
    return s, {'A': A, 'B': B, 'C': C, 'D': D, 'E': E}


if __name__ == '__main__':
    report(*build())
