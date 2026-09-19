"""発展3。指標対をまとめ、支配されない対と代表表を返す。"""
import argparse
from roster_io import read_json
from metric_values import values


def frontier(tables, data):
    # TODO(作業1): values(work, data)が同じ表をまとめ、代表表を一つ残す。
    # TODO(作業2): 支配される対を除き、(指標対, 代表表)のリストを返す。
    raise NotImplementedError('作業1・2を完成させる')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('tables')
    args = parser.parse_args()
    for pair, work in frontier(read_json(args.tables), read_json(args.input)):
        print(pair, work)
