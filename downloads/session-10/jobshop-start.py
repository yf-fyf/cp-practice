"""発展3。入力から一般の日程モデルと独立した時刻別検査を作る。"""
from itertools import combinations
from z3 import Int, Solver, Or
from integer_io import read_input, report
from jobshop_tools import validate


def build(data):
    validate(data)
    tasks = data['tasks']
    starts = {task['name']: Int('start_'+task['name']) for task in tasks}
    s = Solver()
    # TODO(作業1): 入力から開始範囲・先行辺・同装置の全ペアの条件を生成する。
    return s, starts


def valid_schedule(data, starts):
    validate(data)
    # TODO(作業2): 範囲・先行を確認し、各整数時刻の装置使用数を数えて検査する。
    # startsは名前→Pythonの整数。ペアのOrをそのまま複製しない。
    raise NotImplementedError('作業2を完成させる')


if __name__ == '__main__':
    data = read_input('jobshop.json')
    status, starts = report(*build(data))
    if starts is not None:
        try:
            checked = valid_schedule(data, starts)
        except NotImplementedError:
            print('独立検査: 未実装（妥当性は未確認）')
        else:
            print('独立検査:', checked)
