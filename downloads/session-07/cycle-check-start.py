"""発展3：日ごとの二人の列を、勤務日集合など別の表現で検査する。"""
import argparse
import json
from pathlib import Path


def valid_schedule(data, pairs):
    g, n = data['group_size'], data['n_days']
    # 入力した表の形式と各群一人は用意する。人番号は1から。
    if not isinstance(pairs, list) or len(pairs) != n:
        return False
    if any(not isinstance(pair, list) or len(pair) != 2 or
           any(type(p) is not int for p in pair) or
           not (1 <= pair[0] <= g < pair[1] <= 2*g) for pair in pairs):
        return False
    # TODO(作業1) 各人の勤務日を集め、日数の下限・上限を検査する
    # TODO(作業2) 連続日と周期境界、同じ二人の組の再登場を検査する
    # MiniZincの式の転記だけでなく、集合の大きさや勤務日の差を使って考える。
    raise NotImplementedError('作業1と作業2を記入する')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('pairs', type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    pairs = json.loads(args.pairs.read_text())
    print('VALID' if valid_schedule(data, pairs) else 'INVALID')


if __name__ == '__main__':
    main()
