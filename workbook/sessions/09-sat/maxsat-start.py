"""選択S09b。Pythonの確定したboolで真理値表を作る。Z3は使わない。"""
from itertools import product


def row(p, q):
    # TODO(作業1): C1〜C4の真偽をPythonのor・notで計算し、リストにする。
    # TODO(作業2): (節の真偽リスト, 真になる節の個数)を返す。
    raise NotImplementedError('作業1・2を完成させる')


if __name__ == '__main__':
    for p, q in product([False, True], repeat=2):
        print(p, q, row(p, q))
