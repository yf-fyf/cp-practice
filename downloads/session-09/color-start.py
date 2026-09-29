"""選択S09a。各地域ちょうど一色、隣接地域は同色不可。"""
import argparse
import json
from itertools import combinations
from pathlib import Path
from z3 import Bool, Or, Not, And, Solver, sat, unsat
from sat_io import read_values


def build(data):
    regions, colors = data['regions'], data['colors']
    x = {(v, c): Bool(f'{v}_{c}') for v in regions for c in colors}
    s = Solver()
    for v in regions:
        # TODO(作業1): この地域に少なくとも一色を選ぶ。
        for c1, c2 in combinations(colors, 2):
            # TODO(作業2): 同じ地域の二色を同時に選ぶことを禁止する。
            pass
    for u, v in data['edges']:
        for c in colors:
            # TODO(作業3): 隣接二地域で同じ色を同時に選ぶことを禁止する。
            pass
    return s, x


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', default=str(Path(__file__).with_name('australia.json')))
    parser.add_argument('--case', choices=['normal', 'all-false', 'T-two', 'valid'], default='normal')
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text())
    s, x = build(data)
    if args.case != 'normal':
        checks = json.loads(Path(__file__).with_name('color-checks.json').read_text())
        chosen = checks[args.case]
        s.add(*[var == (c in chosen[v]) for (v, c), var in x.items()])
    status = s.check()
    if status == sat:
        print('SAT')
        values = read_values(s.model(), x)
        for v in data['regions']:
            print(v, [c for c in data['colors'] if values[v, c]])
    elif status == unsat:
        print('UNSAT')
    else:
        print('UNKNOWN:', s.reason_unknown())
