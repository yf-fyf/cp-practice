"""発展1。解説例の期限を変え、最初のSATを探す。"""
from z3 import sat, unsat
from schedule_base import build


def at_deadline(H):
    data = {'duration': {'A': 2, 'B': 3, 'C': 2}, 'H': H}
    s, starts = build(data)
    status = s.check()
    if status == sat:
        return {name: s.model().evaluate(var).as_long() for name, var in starts.items()}
    if status == unsat:
        return None
    raise RuntimeError('判定未完了: ' + s.reason_unknown())


def minimum_deadline():
    # TODO(作業1): 所要時間と条件から、探索する期限の下限・上限を決める。
    # TODO(作業2): at_deadline(H)で判定し、最小期限と成立する日程を返す。
    raise NotImplementedError('作業1・2を完成させる')


if __name__ == '__main__':
    print(minimum_deadline())
