"""判定状態を区別し、SATの場合だけ指定変数の値を表示する。"""
from z3 import sat, unsat, is_true


def read_values(model, variables):
    return {name: is_true(model.evaluate(var, model_completion=True))
            for name, var in variables.items()}


def report(solver, variables):
    result = solver.check()
    if result == sat:
        values = read_values(solver.model(), variables)
        print('SAT')
        for name, value in values.items():
            print(f'{name}={value}')
        return 'sat', values
    if result == unsat:
        print('UNSAT')
        return 'unsat', None
    print('UNKNOWN:', solver.reason_unknown())
    return 'unknown', None


def fix_pair(solver, variables, case):
    # 呼び出しごとに新しいsolverを渡す。二つの固定を積み重ねない。
    if case == 'both-true':
        solver.add(variables['A'] == True, variables['F'] == True)
    elif case == 'both-false':
        solver.add(variables['A'] == False, variables['F'] == False)
    elif case != 'normal':
        raise ValueError('unknown case')
