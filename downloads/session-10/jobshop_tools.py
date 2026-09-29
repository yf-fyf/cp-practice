"""発展3の入力検査と有限な開始時刻の列挙の足場。"""
from itertools import product


def validate(data):
    tasks = data['tasks']
    names = [task['name'] for task in tasks]
    if len(names) != len(set(names)) or not all(isinstance(n, str) and n for n in names):
        raise ValueError('作業名は空でない異なる文字列')
    if type(data['H']) is not int or data['H'] < 0:
        raise ValueError('期限は非負整数')
    if any(type(t['duration']) is not int or t['duration'] <= 0 for t in tasks):
        raise ValueError('所要時間は正整数')
    if any(type(t['machine']) is not int or t['machine'] <= 0 for t in tasks):
        raise ValueError('装置番号は正整数')
    if any(len(edge) != 2 or any(n not in names for n in edge) for edge in data['precedence']):
        raise ValueError('先行辺は入力中の二つの作業名')


def finite_starts(data):
    validate(data)
    tasks = data['tasks']
    ranges = [range(data['H']-task['duration']+1) for task in tasks]
    for times in product(*ranges):
        yield dict(zip([t['name'] for t in tasks], times))
