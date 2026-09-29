"""第09回と同じ三分岐で判定し、整数の代入を読む。"""
import argparse
import json
from pathlib import Path
from z3 import sat, unsat


def read_input(default):
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default=str(Path(__file__).with_name(default)))
    args = parser.parse_args()
    return json.loads(Path(args.input).read_text())


def report(solver, variables):
    result = solver.check()
    if result == sat:
        model = solver.model()
        values = {name: model.evaluate(var, model_completion=True).as_long()
                  for name, var in variables.items()}
        print('SAT')
        for name, value in values.items():
            print(f'{name}={value}')
        return 'sat', values
    if result == unsat:
        print('UNSAT')
        return 'unsat', None
    print('UNKNOWN:', solver.reason_unknown())
    return 'unknown', None


def report_schedule(solver, starts, data):
    status, values = report(solver, starts)
    if values is not None:
        for name, begin in values.items():
            print(f'{name}: [{begin}, {begin + data["duration"][name]})')
    return status, values


def run_schedule_exercise(build, default):
    """必修1の入力実行、またはそのモデルへの固定検査を行う。"""
    parser = argparse.ArgumentParser(description='日程の実行と固定検査')
    parser.add_argument('input', nargs='?')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    folder = Path(__file__).parent
    if args.check:
        if args.input:
            parser.error('--checkでは各検査の入力を使うため、入力ファイルを同時に指定しない')
        cases = json.loads((folder / 'schedule-checks.json').read_text())
        failures = 0
        checked = 0
        for case in cases:
            if case['model'] != 'basic':
                continue
            data = json.loads((folder / case['input']).read_text())
            solver, starts = build(data)
            for name, value in zip('ABC', case['start']):
                solver.add(starts[name] == value)
            result = solver.check()
            expected = sat if case['valid'] else unsat
            ok = result == expected
            checked += 1
            failures += not ok
            print(f"{case['name']}: {str(result).upper()} / expected {str(expected).upper()} / {'PASS' if ok else 'FAIL'}")
            if result not in (sat, unsat):
                print('UNKNOWN:', solver.reason_unknown())
        if checked == 0:
            raise ValueError('必修1の検査例がない')
        print(f'{checked} checks, {failures} failures')
        if failures:
            raise SystemExit(1)
    else:
        file = Path(args.input) if args.input else folder / default
        data = json.loads(file.read_text())
        report_schedule(*build(data), data)
