"""発展3。入力の形式と、完成した代入の充足を調べる。"""
import json
from pathlib import Path


def validate(n, clauses):
    if type(n) is not int or n < 0 or not isinstance(clauses, list):
        raise ValueError('nは非負整数、clausesはリスト')
    for clause in clauses:
        if not isinstance(clause, list):
            raise ValueError('節は整数のリスト')
        if any(type(lit) is not int or not 1 <= abs(lit) <= n for lit in clause):
            raise ValueError('リテラルは±1〜±n。0は使わない')


def read_case(path):
    data = json.loads(Path(path).read_text())
    validate(data['n'], data['clauses'])
    return data['n'], data['clauses']


def satisfies(n, clauses, assignment):
    if set(assignment) != set(range(1, n+1)):
        return False
    if any(type(value) is not bool for value in assignment.values()):
        return False
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
               for clause in clauses)
