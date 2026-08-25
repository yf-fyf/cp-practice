#!/usr/bin/env python3
"""ソルバーが出した数独の盤面を、モデルとは独立に確かめる。

MiniZinc Playground の出力をそのまま貼り付けて使う。

    python3 check_sudoku.py            # 盤面を貼り付けて Ctrl-D（Windows は Ctrl-Z Enter）
    python3 check_sudoku.py board.txt  # ファイルから読む

「ソルバーが解を返した」ことと「制約を書き切れている」ことは別である。
制約を1つ書き忘れていても、ソルバーはその条件を無視した盤面を平気で返す。
このスクリプトはモデルを見ずに盤面だけを検査するので、書き忘れに気づける。

初期値の照合には、既定でこのファイルの GIVEN（第03回の 4×4 盤面）を使う。
第04回のように盤面を差し替えるときは、データファイルを渡す。

    python3 check_sudoku.py --given puzzle-a.dzn board.txt
    python3 check_sudoku.py --no-given board.txt     # 初期値の照合を省く
"""

from __future__ import annotations

import math
import re
import sys

# sudoku4.mzn の given と同じ盤面（0 は空きマス）
GIVEN = [
    [1, 0, 3, 0],
    [0, 0, 0, 2],
    [2, 0, 0, 0],
    [0, 3, 0, 1],
]

USAGE = ("使い方: python3 check_sudoku.py [--no-given | --given データ.dzn] "
         "[盤面のファイル]")


def read_board(text: str) -> list[list[int]]:
    """数字だけを拾って正方形に並べ直す。空行・区切り・記号は読み飛ばす。

    1桁ずつ拾うので、値が9までの盤面（4×4・9×9）だけを対象にする。
    `%` で始まる行から下は読まない。第04回のモデルは盤面のあとに
    `.dzn` へ貼るための行を出すので、そこで切らないと数が合わなくなる。
    """
    body = []
    for line in text.splitlines():
        if line.lstrip().startswith("%"):
            break
        body.append(line)
    digits = [int(ch) for ch in "\n".join(body) if ch.isdigit()]
    size = math.isqrt(len(digits))
    if size * size != len(digits):
        raise SystemExit(f"数字が {len(digits)} 個ある。正方形にならない")
    return [digits[r * size:(r + 1) * size] for r in range(size)]


def read_given(path: str) -> list[list[int]]:
    """`.dzn` の `given = [| ... |];` を読んで初期値の盤面にする。"""
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as error:
        raise SystemExit(f"データファイルを読めない: {error}")
    text = re.sub(r"%[^\n]*", "", text)          # コメントを落とす
    head, marker, rest = text.partition("given")
    if not marker:
        raise SystemExit(f"{path} に given の代入が見つからない")
    body = rest.split(";", 1)[0]
    return read_board(body)


def problems(board: list[list[int]],
             given: list[list[int]] | None) -> list[str]:
    n = len(board)
    b = math.isqrt(n)
    if b * b != n:
        return [f"一辺 {n} はブロックに分けられない（4, 9, 16 のいずれかを想定）"]

    found: list[str] = []
    values = set(range(1, n + 1))

    for r in range(n):
        if set(board[r]) != values:
            found.append(f"{r + 1} 行目に重複か範囲外がある: {board[r]}")
    for c in range(n):
        column = [board[r][c] for r in range(n)]
        if set(column) != values:
            found.append(f"{c + 1} 列目に重複か範囲外がある: {column}")
    for br in range(0, n, b):
        for bc in range(0, n, b):
            block = [board[br + i][bc + j] for i in range(b) for j in range(b)]
            if set(block) != values:
                found.append(
                    f"左上が ({br + 1}, {bc + 1}) のブロックに重複か範囲外がある: {block}")

    if given is not None:
        if len(given) != n:
            found.append("初期値の大きさが盤面と違う"
                         "（--given でこの盤面のデータを渡すか、--no-given を付ける）")
        else:
            for r in range(n):
                for c in range(n):
                    if given[r][c] and board[r][c] != given[r][c]:
                        found.append(
                            f"({r + 1}, {c + 1}) の初期値 {given[r][c]} が "
                            f"{board[r][c]} に変わっている")
    return found


def parse_args(argv: list[str]) -> tuple[list[list[int]] | None, str | None]:
    """(照合に使う初期値, 盤面のファイル) を返す。ファイルが None なら標準入力。"""
    given: list[list[int]] | None = GIVEN
    board_file: str | None = None
    rest = list(argv)
    while rest:
        item = rest.pop(0)
        if item == "--no-given":
            given = None
        elif item == "--given":
            if not rest:
                raise SystemExit(USAGE)
            given = read_given(rest.pop(0))
        elif item.startswith("-"):
            raise SystemExit(USAGE)
        elif board_file is None:
            board_file = item
        else:
            raise SystemExit(USAGE)
    return given, board_file


def main() -> int:
    given, board_file = parse_args(sys.argv[1:])
    text = (open(board_file, encoding="utf-8").read() if board_file
            else sys.stdin.read())

    board = read_board(text)
    for row in board:
        print(" ".join(str(v) for v in row))
    print()

    found = problems(board, given)
    if found:
        print(f"満たしていない条件が {len(found)} 件ある:")
        for item in found:
            print(f"  - {item}")
        return 1
    print("行・列・ブロック"
          + ("・初期値" if given is not None else "")
          + " のすべての条件を満たしている。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
