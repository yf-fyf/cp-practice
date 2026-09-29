"""発展3用に提供する指標の再計算。発展1の完成を前提にしない。"""
from roster_io import basic_errors


def values(work, data):
    if basic_errors(work, data):
        raise ValueError('基本勤務条件を満たさない表')
    days = [sum(row) for row in work]
    violations = sum(work[p][d] * data['request'][p][d]
                     for p in range(len(work)) for d in range(len(work[p])))
    return violations, max(days) - min(days)
