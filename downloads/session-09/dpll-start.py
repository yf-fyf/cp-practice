"""発展3。整数リテラルのCNFを単位伝播・分岐・復元で解く。"""
import argparse
from cnf_tools import read_case, validate, satisfies


def solve(n, clauses):
    validate(n, clauses)
    # TODO(作業1): 部分代入で節を簡約し、単位伝播と矛盾・成功を判定する。
    # TODO(作業2): 未定変数の二値へ分岐し、失敗した枝の変更を持ち越さない。
    # SATなら1〜n全変数のbool辞書、UNSATならNone。入力は変更しない。
    raise NotImplementedError('作業1・2を完成させる')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    args = parser.parse_args()
    n, clauses = read_case(args.input)
    result = solve(n, clauses)
    if result is None:
        print('UNSAT')
    else:
        assert satisfies(n, clauses, result), '返した代入が元のCNFを満たしていない'
        print('SAT', result)
