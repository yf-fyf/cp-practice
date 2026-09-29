"""配列の読み込みと基本条件の確認。目的値や最適性は判定しない。"""
import json
from pathlib import Path


def read_json(path):
    return json.loads(Path(path).read_text())


def basic_errors(work, data):
    available = data['available']
    n = len(available)
    m = len(data['required'])
    if len(work) != n or any(len(row) != m for row in work):
        return ['shape']
    if any(type(v) is not int or v not in (0, 1) for row in work for v in row):
        return ['binary']
    errors = []
    if any(work[p][d] > available[p][d] for p in range(n) for d in range(m)):
        errors.append('available')
    if any(sum(work[p][d] for p in range(n)) != data['required'][d] for d in range(m)):
        errors.append('staff')
    if any(sum(work[p]) > data['max_days'][p] for p in range(n)):
        errors.append('max_days')
    return errors
