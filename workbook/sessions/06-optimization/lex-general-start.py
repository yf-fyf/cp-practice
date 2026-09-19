"""発展3：完成した二段階法と重み付き法を、複数の小入力で比較する。"""
import json
from pathlib import Path
import sys
import tempfile
from solve_tools import run, optimum, write_data


def compare(case, models):
    with tempfile.TemporaryDirectory() as directory:
        datum=Path(directory)/'input.dzn'
        write_data(datum,case)
        # TODO(作業1): 第一目的を最大化し、最適値を固定して時間を最小化する。
        # TODO(作業2): 時間上限から重みを決めて解き、二段階法と比較する。
        # run(model, datum, 'best=5;')のように追加の入力値を渡せる。
        # optimum(result)は最適終了を確認し、その目的値を返す。
        raise NotImplementedError('二段階法と重み付き法を比較する')


if __name__=='__main__':
    folder=Path(__file__).resolve().parent
    models=dict(first=folder/'kits-base.mzn',second=folder/'lex-start.mzn',
                weighted=folder/'weighted-start.mzn')
    cases=json.loads(Path(sys.argv[1]).read_text())
    print(json.dumps([compare(case,models) for case in cases],indent=2))
