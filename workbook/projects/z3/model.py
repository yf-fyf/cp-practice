#!/usr/bin/env python3
"""自由課題の最小雛形（Python + Z3）

教材ページ: 自由課題 > 第12回 最小実行モデル
実行環境:   Python 3 + z3-solver（版は requirements.txt で固定してある）

    pip install -r requirements.txt
    python3 model.py

そのままでも動く（制約が1本も無いので、どんな解でも返る）。
まず動かしてから、TODO(1) の制約を1本ずつ足していく。

変数の取り方はこの形でなくてよい。ここでは「対象ごとに値を1つ決める」
いちばん素直な形にしてある。真偽の組合せが制約の中心なら、
Int ではなく Bool の2次元で持つほうが書きやすいことがある。
"""
from __future__ import annotations

from z3 import Int, Solver, sat

# ── 入力 ────────────────────────────────────────────────────
# 最小インスタンスは「紙の上で答えを1つ作れる大きさ」にする。
# 企画書の節6に書き下した数値を、ここへ写す。
# 入力が増えてきたら、別ファイル（JSON など）へ分けてここで読み込む。
# モデルとデータを分けておくと、規模を変えるときにモデルを触らずに済む。

N = 4                                # 決める対象の数
K = 2                                # 各対象が取り得る値の数
NAMES = ["A", "B", "C", "D"]         # 対象の名前（N 個）


def build() -> tuple[Solver, list]:
    """ソルバーと決定変数を作って返す。"""
    # ── 決定変数と定義域 ───────────────────────────────────
    x = [Int(f"x_{i}") for i in range(N)]
    solver = Solver()
    for xi in x:
        solver.add(1 <= xi, xi <= K)

    # ── ハード制約 ─────────────────────────────────────────
    # TODO(1) 企画書の H1 から順に、1本ずつ足す。
    #         1本足すたびに実行して、解が変わったかを見る。
    #         期待どおりでなければ、いま足した1本を疑う。ほかを疑わない。
    #
    #         書き方の例（企画書の番号をコメントに残しておくと後で追える）:
    #
    # # H1. 同じ値を2つの対象に割り当てない
    # from z3 import Distinct
    # solver.add(Distinct(x))
    #
    # # H2. 対象 0 と対象 1 は違う値にする
    # solver.add(x[0] != x[1])
    #
    # # H3. どの値も、使われる回数は 2 回までにする
    # from z3 import If, Sum
    # for v in range(1, K + 1):
    #     solver.add(Sum([If(xi == v, 1, 0) for xi in x]) <= 2)

    # ── ソフト制約と目的 ───────────────────────────────────
    # TODO(2) 目的が無い問題は、このままでよい（充足だけを求める）。
    #         目的があるなら Solver ではなく Optimize を使う。
    #
    # from z3 import Optimize, If, Sum
    # opt = Optimize()
    # ... 上と同じ制約を opt.add(...) で入れる ...
    # penalty = Sum([If(xi != 1, 1, 0) for xi in x])
    # opt.minimize(penalty)

    return solver, x


def main() -> int:
    solver, x = build()
    if solver.check() != sat:
        print("解なし（unsat）")
        print("制約を1本ずつ外して、どれが解を消しているかを探す。")
        return 1

    model = solver.model()
    values = [model[xi].as_long() for xi in x]

    # 検証器が読む行（# で始まる行）。verify.py はこれだけを読む。
    print(f"#size {N} {K}")
    for name, value in zip(NAMES, values):
        print(f"#assign {name} {value}")
    # 目的関数を足したら、次の1行も出しておく。
    # print(f"#value penalty {penalty_value}")

    # 人が読む行。
    print()
    for name, value in zip(NAMES, values):
        print(f"{name} -> {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
