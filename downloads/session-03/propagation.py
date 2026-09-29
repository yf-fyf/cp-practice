"""第03回の教材用規則。実際のMiniZincソルバーの探索ログではない。"""
from pathlib import Path
import json
import argparse

VALUES = {1, 2, 3, 4}
UNITS = (
    [[4*r+c for c in range(4)] for r in range(4)]
    + [[4*r+c for r in range(4)] for c in range(4)]
    + [[4*(r+i)+c+j for i in range(2) for j in range(2)]
       for r in (0,2) for c in (0,2)]
)
PEERS = [{j for unit in UNITS if i in unit for j in unit if j != i} for i in range(16)]


def initial(given):
    if len(given) != 16 or any(type(v) is not int or v not in range(5) for v in given):
        raise ValueError('givenは0〜4の整数16個とする')
    return [{v} if v else set(VALUES) for v in given]


def reduce_once(domains):
    # 同じ更新前の状態から、すべてのマスを同時に更新する。
    return [d - {next(iter(domains[j])) for j in PEERS[i] if len(domains[j]) == 1}
            if len(d) > 1 else set(d) for i, d in enumerate(domains)]


def propagate(domains):
    history = [[set(d) for d in domains]]
    while status(history[-1]) == 'stalled':
        new = reduce_once(history[-1])
        if new == history[-1]:
            break
        history.append(new)
    return history


def status(domains):
    if any(not d for d in domains):
        return 'contradiction'
    if any(domains[i] == domains[j] and len(domains[i]) == 1
           for i in range(16) for j in PEERS[i]):
        return 'contradiction'
    if all(len(d) == 1 for d in domains):
        return 'complete'
    return 'stalled'


def encode(domains):
    return [sorted(d) for d in domains]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--assume', nargs=3, type=int, metavar=('ROW', 'COL', 'VALUE'))
    args = parser.parse_args()
    given = json.loads(args.input.read_text())['given']
    history = propagate(initial(given))
    result = {}
    if args.assume:
        r, c, v = args.assume
        if r not in range(1,5) or c not in range(1,5):
            parser.error('行・列は1〜4で指定する')
        i = 4*(r-1)+c-1
        if status(history[-1]) != 'stalled' or v not in history[-1][i]:
            parser.error('停止した候補表に残っている値を仮定する')
        result['before_branch'] = encode(history[-1])
        branch = [set(d) for d in history[-1]]
        branch[i] = {v}
        history = propagate(branch)
    result.update(rounds=[encode(d) for d in history], status=status(history[-1]))
    print(json.dumps(result, ensure_ascii=False, indent=2))
