"""発展用のMiniZinc CLI部品。判定と目的値を混同しないため終了状態も返す。"""
import json
from pathlib import Path
import subprocess


def run(model, datum, extra='', all_solutions=False):
    args=['minizinc','--solver','gecode','--json-stream','--output-mode','json',
          '--output-objective','--time-limit','10000']
    if all_solutions: args.append('--all-solutions')
    args.extend([str(model),str(datum)])
    if extra: args.extend(['-D',extra])
    result=subprocess.run(args,text=True,capture_output=True,timeout=20)
    events=[json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    errors=[e for e in events if e['type']=='error']
    if errors: raise RuntimeError('; '.join(describe(e) for e in errors))
    if result.returncode!=0: raise RuntimeError(result.stderr.strip() or 'MiniZincが異常終了した')
    statuses=[e['status'] for e in events if e['type']=='status']
    return dict(status=statuses[-1] if statuses else 'UNKNOWN',
                solutions=[e['output']['json'] for e in events if e['type']=='solution'])


def describe(error):
    loc=error.get('location')
    where=f" ({Path(loc['filename']).name}:{loc['firstLine']})" if loc else ''
    return error.get('what','error')+where+': '+error.get('message','')


def optimum(result):
    if result['status']!='OPTIMAL_SOLUTION' or not result['solutions']:
        raise ValueError('最適終了していない: '+result['status'])
    return result['solutions'][-1]['_objective']


def write_data(path, data):
    if any(type(value) is not int for value in data.values()):
        raise ValueError('入力値は整数にする')
    Path(path).write_text(''.join(f'{key} = {value};\n' for key,value in data.items()))
