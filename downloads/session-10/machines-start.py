"""発展2。二台の同じ装置へ、三作業の装置と開始時刻を割り当てる。"""
from itertools import combinations
from z3 import Int, Solver, Or
from integer_io import read_input, report


def build(data):
    tasks = list(data['duration'])
    start = {name: Int('start_'+name) for name in tasks}
    machine = {name: Int('machine_'+name) for name in tasks}
    s = Solver()
    for name in tasks:
        s.add(0 <= start[name], start[name] <= data['H']-data['duration'][name])
        s.add(1 <= machine[name], machine[name] <= data['machines'])
    for a, b in combinations(tasks, 2):
        # TODO(作業1): 装置が同じ場合と異なる場合に許す重なりを分け、条件を書く。
        pass
    # TODO(作業2): 期限5・6を別々に実行し、同時刻でも別装置なら許すか確かめる。
    return s, {**{'s'+t: start[t] for t in tasks}, **{'m'+t: machine[t] for t in tasks}}


if __name__ == '__main__':
    report(*build(read_input('machines-5.json')))
