"""第10回・必修1。所要時間を入力から読み、日程の条件を書く。"""
from z3 import Int, Solver, Or
from integer_io import run_schedule_exercise


def build(data):
    duration = data['duration']
    H = data['H']
    starts = {name: Int('s' + name) for name in duration}
    sA, sB, sC = (starts[name] for name in 'ABC')
    dA, dB, dC = (duration[name] for name in 'ABC')
    s = Solver()
    # TODO(作業1): durationの各作業について、開始下限と期限からの開始上限を生成する。
    # TODO(作業2): AからBへの先行と、A・Cの非重複を書く。
    return s, starts


if __name__ == '__main__':
    run_schedule_exercise(build, 'practice.json')
