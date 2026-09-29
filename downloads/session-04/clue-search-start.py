"""発展3：完成盤面から最少ヒントを選ぶ。Python標準ライブラリだけを使う。"""
from itertools import combinations
import importlib.util
from pathlib import Path
import sys

spec = importlib.util.spec_from_file_location('clue_tools',
    Path(__file__).with_name('clue-tools.py'))
clues = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clues)


def minimum(boards, target):
    # TODO(作業1): 小さい個数から、36候補の組をすべて試す。
    # TODO(作業2): 残る集合がtargetだけなら、その組を返す。
    # 内部番号は0〜35。clues.remaining(boards, target, selected)を使える。
    raise NotImplementedError('最少の組の探索を実装する')


if __name__ == '__main__':
    boards, target = clues.read_inputs(sys.argv[1])
    selected = minimum(boards, target)
    if selected is None:
        raise SystemExit('この候補では一意にできない')
    print('候補番号:', [k+1 for k in selected], file=sys.stderr)
    print(clues.dzn(target, selected), end='')
