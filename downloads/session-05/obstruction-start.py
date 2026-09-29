"""発展3：小さい人の集合から、利用できる定員が足りない集合を探す。"""
from itertools import combinations
import json
from pathlib import Path
import sys


def minimum_obstruction(allowed, cap):
    # TODO(作業1): 人の集合を少ない人数から列挙する。
    # TODO(作業2): 利用できる講座の定員総和が人数未満なら集合を返す。
    # 人・講座の内部番号は0始まり。見つからなければNoneを返す。
    raise NotImplementedError('障害集合の探索を実装する')


if __name__ == '__main__':
    data = json.loads(Path(sys.argv[1]).read_text())
    selected = minimum_obstruction(data['allowed'], data['cap'])
    if selected is None:
        print('定員不足の人の集合は見つからなかった')
    else:
        courses = {c for p in selected for c, ok in enumerate(data['allowed'][p]) if ok}
        print('人の番号:', [p+1 for p in selected])
        print('利用できる講座:', [c+1 for c in sorted(courses)])
        print('人数:', len(selected), '定員総和:', sum(data['cap'][c] for c in courses))
