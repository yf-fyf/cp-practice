"""発展2。必修1のA〜Eの全代入を列挙する。"""
from z3 import Or, sat, unsat
from features_base import build
from sat_io import read_values


def enumerate_models(s, variables):
    results = []
    # TODO(作業1): checkがsatの間、read_values(s.model(), variables)を記録する。
    # TODO(作業2): 全指定変数の少なくとも一つが今の値と違う条件を追加する。
    # 終了がunsatなら全列挙完了。unknownなら完了として返さない。
    raise NotImplementedError('作業1・2を完成させる')


if __name__ == '__main__':
    for values in enumerate_models(*build()):
        print(values)
