"""第10回・必修2。AとCの両方が終わってからBを始める。"""
from schedule_base import build as build_base
from integer_io import read_input, report_schedule


def build(data):
    s, starts = build_base(data)
    sB, sC = starts['B'], starts['C']
    dC = data['duration']['C']
    # TODO(作業1): Cが終わってからBを始める先行条件を追加する。
    return s, starts


if __name__ == '__main__':
    # TODO(作業2): 期限6・7の入力を別々に実行し、判定と区間を照合する。
    data = read_input('wait-6.json')
    report_schedule(*build(data), data)
