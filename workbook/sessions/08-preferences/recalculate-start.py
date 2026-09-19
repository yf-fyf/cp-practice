"""発展1。Python標準ライブラリのみで、配列から独立に再計算する。"""
import argparse
from roster_io import read_json, basic_errors


def recalculate(work, data, k=None):
    errors = basic_errors(work, data)
    if errors:
        return {'valid': False, 'errors': errors}
    # TODO(作業1): 全員の日数load、希望違反V、日数差Fを計算する。
    # TODO(作業2): kが指定された場合にV <= kも調べ、結果を返す。
    raise NotImplementedError('作業1・2を完成させる')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('tables')
    parser.add_argument('--k', type=int)
    args = parser.parse_args()
    for example in read_json(args.tables):
        print(example['name'], recalculate(example['work'], read_json(args.input), args.k))
