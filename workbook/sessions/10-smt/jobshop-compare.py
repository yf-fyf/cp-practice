"""発展3。自作モデルの全解と、自作の独立検査器による有限列挙を照合。"""
import argparse
import importlib.util
import json
from pathlib import Path
from z3 import Or, sat, unsat
from jobshop_tools import finite_starts


def compare(module, data):
    names = [t['name'] for t in data['tasks']]
    finite = {tuple(starts[n] for n in names) for starts in finite_starts(data)
              if module.valid_schedule(data, starts)}
    s, variables = module.build(data)
    actual = set()
    while True:
        status = s.check()
        if status == unsat:
            break
        if status != sat:
            raise RuntimeError('全列挙未完了: '+s.reason_unknown())
        starts = {n: s.model().evaluate(variables[n], model_completion=True).as_long() for n in names}
        row = tuple(starts[n] for n in names)
        if row in actual:
            raise AssertionError('同じ解を除外できていない')
        actual.add(row)
        s.add(Or([variables[n] != starts[n] for n in names]))
    if actual != finite:
        raise AssertionError({'SMTだけ': sorted(actual-finite), '列挙だけ': sorted(finite-actual)})
    return len(actual)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solution')
    parser.add_argument('cases', nargs='?', default=str(Path(__file__).with_name('jobshop-cases.json')))
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('learner_jobshop', Path(args.solution))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for i, data in enumerate(json.loads(Path(args.cases).read_text()), 1):
        print(i, 'PASS', compare(module, data))
