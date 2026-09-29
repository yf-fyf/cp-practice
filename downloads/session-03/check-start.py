"""発展2。判定部分を自分で実装する。入出力は提供する。"""
from pathlib import Path
import json
import sys


def is_solution(given, grid):
    # TODO(作業1): gridの長さ・整数型・1〜4の範囲と、初期値の保持を確認する。
    # TODO(作業2): 各行・各列・四つの2×2ブロックの重複を確認する。
    raise NotImplementedError('判定部分を実装してください')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python3 check-start.py V1.json')
    data = json.loads(Path(sys.argv[1]).read_text())
    given, grid = data['given'], data['grid']
    if len(given) != 16 or any(type(v) is not int or v not in range(5) for v in given):
        raise ValueError('givenの形式が違います')
    result = is_solution(given, grid)
    if type(result) is not bool:
        raise TypeError('is_solutionはTrueかFalseを返してください')
    print(json.dumps(result))
