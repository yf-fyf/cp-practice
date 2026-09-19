"""発展3。伝播を利用して全解を返す探索を実装する。"""
from pathlib import Path
import json
import sys
from propagation import initial, propagate, status


def search(domains):
    # 戻り値は完成盤面（16個の整数）のリスト。解なしなら空リスト。
    # TODO(作業1): 伝播し、矛盾・完成・未確定を区別する。
    # 矛盾なら空リスト、完成なら16個の値からなる盤面を一つ入れたリストを返す。
    # statusは確定値同士の衝突も検査する。
    # TODO(作業2): 未確定マスの各候補を仮定し、独立な状態で再帰する。
    # 各枝の解をすべて集めて返す。
    raise NotImplementedError('探索を実装してください')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python3 search-start.py branch.json')
    given = json.loads(Path(sys.argv[1]).read_text())['given']
    answers = search(initial(given))
    if not isinstance(answers, list):
        raise TypeError('完成盤面のリストを返してください')
    print(json.dumps(answers, ensure_ascii=False))
