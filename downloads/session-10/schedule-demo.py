"""第10回の解説例。A→B、AとCが同じ装置。"""
from z3 import Ints, Solver, Or
from integer_io import read_input, report_schedule


def build(data):
    # 手順1　開始時刻と境界
    dA, dB, dC = (data['duration'][name] for name in 'ABC')
    H = data['H']
    sA, sB, sC = Ints('sA sB sC')
    s = Solver()
    s.add(0 <= sA, sA <= H-dA)
    s.add(0 <= sB, sB <= H-dB)
    s.add(0 <= sC, sC <= H-dC)
    # 手順2　先行と非重複
    s.add(sA+dA <= sB)
    s.add(Or(sA+dA <= sC, sC+dC <= sA))
    return s, {'A': sA, 'B': sB, 'C': sC}


if __name__ == '__main__':
    data = read_input('demo.json')
    # 手順3　判定と区間の確認
    report_schedule(*build(data), data)
