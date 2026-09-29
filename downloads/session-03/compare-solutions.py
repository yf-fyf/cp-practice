"""探索の出力を、配布された確認用の完成盤面集合と照合する。"""
import json
from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit('usage: python3 compare-solutions.py empty answers.json')
known = json.loads(Path(__file__).with_name('solutions.json').read_text())
if sys.argv[1] not in known:
    raise SystemExit('入力名は demo / practice / branch / empty / conflict / compare')
actual = json.loads(Path(sys.argv[2]).read_text())
if not isinstance(actual, list) or any(
    not isinstance(row, list) or len(row) != 16
    or any(type(v) is not int or v not in range(1, 5) for v in row)
    for row in actual
):
    raise SystemExit('FAIL: 完成盤面の形式が違います')
found = {tuple(row) for row in actual}
wanted = {tuple(row) for row in known[sys.argv[1]]}
if len(found) != len(actual) or found != wanted:
    raise SystemExit('FAIL: 重複、余分な盤面、または不足があります')
print(f'PASS: {len(found)} solutions; no duplicates; full set matched')
