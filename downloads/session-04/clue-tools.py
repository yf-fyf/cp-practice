"""発展3の共通部品。盤面は行順16整数、内部のマス番号は0〜15。"""
from itertools import combinations
import json
from pathlib import Path


def regions():
    return [tuple(sorted(4*(r+dr)+c+dc for dr, dc in corner))
            for r in range(3) for c in range(3)
            for corner in combinations([(0,0),(0,1),(1,0),(1,1)], 3)]


def read_inputs(target_path):
    boards = [tuple(x) for x in json.loads(
        Path(__file__).with_name('boards.json').read_text())]
    target = tuple(json.loads(Path(target_path).read_text()))
    if len(target) != 16 or any(type(v) is not int for v in target) or target not in boards:
        raise ValueError('基本数独を満たす行順16整数の完成盤面を指定する')
    return boards, target


def remaining(boards, target, selected):
    cells = regions()
    totals = [sum(target[i] for i in region) for region in cells]
    return {board for board in boards if all(
        sum(board[i] for i in cells[k]) == totals[k] for k in selected)}


def dzn(target, selected):
    cells = regions()
    def matrix(name, rows):
        return name + ' = [| ' + '\n | '.join(
            ', '.join(map(str, row)) for row in rows) + ' |];\n'
    return (matrix('given', [[0]*4]*4) + 'n = 36;\n'
            + matrix('clue_r', [[i//4+1 for i in row] for row in cells])
            + matrix('clue_c', [[i%4+1 for i in row] for row in cells])
            + 'total = ' + str([sum(target[i] for i in row) for row in cells]) + ';\n'
            + 'enabled = ' + str([int(k in selected) for k in range(36)]) + ';\n')
