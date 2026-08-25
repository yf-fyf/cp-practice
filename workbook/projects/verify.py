#!/usr/bin/env python3
"""自由課題の検証器の雛形 — モデルとは独立に、解が仕様を満たすかを調べる

教材ページ: 自由課題 > 検証チェックリストと実験記録
実行環境:   Python 3（外部ライブラリは要らない。Z3 も MiniZinc も要らない）

    python3 verify.py out/small.txt
    python3 verify.py out/small.txt data/small.dzn

第10回の勤務表の検証器と同じ作りである。骨格だけを残してあるので、
自分の問題のハード制約を、1条件につき1つの関数として書き足す。

読み取るのは、モデルが出している次の行である
（workbook/projects/minizinc/model.mzn と z3/model.py が最初から出している）。

    #size <対象の数> <値の数>
    #assign <対象の名前> <値> [<値> ...]
    #value <名前> <整数>        … 目的関数を足したモデルだけが出す

#assign の値は**いくつ並んでもよい**。1つの対象について決めることが
2つ以上ある題材（たとえば「科目 → 時間帯 と 教室」）は、そのまま並べて出す。

    #assign 数学 1          … 決めることが1つ（時間帯だけ）
    #assign 数学 1 2        … 決めることが2つ（時間帯と教室）

読み取ったものは assign["数学"] = [1] や [1, 2] のように**必ずリスト**で入る。
i 番目の値だけを取り出すには column(assign, i) を使う（下にある）。
**この雛形を書き換える必要はない。**

# で始まらない行は読み飛ばすので、モデルの出力を**まるごと**保存してよい。

--------------------------------------------------------------------------
検査を書くときの決まり
--------------------------------------------------------------------------
1. 検査は「見つけた違反を並べたリスト」を返す。空のリストなら合格である。
2. **まだ書いていない検査は None を返す。** 空のリスト（違反なし）と
   区別できないと、検査を書き忘れたのに反例が合格した状態が正常に見える。
3. **検査はモデルを見ずに、企画書の制約の文から書く。**
   モデルを見ながら書くと、モデルと同じ間違いを写してしまう。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


# ── モデルの出力を読む ──────────────────────────────────────

def parse_output(text: str) -> tuple[dict[str, list], dict[str, int], tuple[int, int]]:
    """出力から (対象名 → 値のリスト, #value の一覧, (対象の数, 値の数)) を取り出す。

    #assign の行は空白で区切って読むだけなので、値がいくつ並んでいてもよい。
    整数に見える値は整数に、そうでない値（"大" など）は文字列のまま入れる。

    最適化では解が何本も出る。**最後の解だけ**を残す。
    """
    assign: dict[str, list] = {}
    values: dict[str, int] = {}
    size: tuple[int, int] | None = None

    for line in text.splitlines():
        m = re.match(r"^#size\s+(\d+)\s+(\d+)\s*$", line)
        if m:
            size = (int(m.group(1)), int(m.group(2)))
            assign, values = {}, {}          # 新しい解が始まった
            continue
        m = re.match(r"^#value\s+(\w+)\s+(-?\d+)\s*$", line)
        if m:
            values[m.group(1)] = int(m.group(2))
            continue
        if line.startswith("#assign"):
            parts = line.split()             # ["#assign", 名前, 値, 値, ...]
            if len(parts) < 3:
                raise ValueError(f"#assign の行に値が無い: {line!r}")
            name, rest = parts[1], parts[2:]
            assign[name] = [int(v) if re.fullmatch(r"-?\d+", v) else v for v in rest]

    if size is None:
        raise ValueError("#size の行が無い。出力を全部コピーできているか確かめる")
    if len(assign) != size[0]:
        raise ValueError(f"#size は {size[0]} 件だが、#assign が {len(assign)} 行しかない")
    widths = {len(v) for v in assign.values()}
    if len(widths) > 1:
        raise ValueError(f"#assign の値の個数が行によって違う（{sorted(widths)}）。"
                         "モデルの output を見直す")
    return assign, values, size


def column(assign: dict[str, list], i: int = 0) -> dict:
    """assign の i 番目の値だけを取り出して「対象名 → 値」の辞書にする。

    決めることが1つの題材:   slot = column(assign)
    決めることが2つの題材:   slot = column(assign, 0)
                             room = column(assign, 1)
    """
    try:
        return {name: values[i] for name, values in assign.items()}
    except IndexError:
        raise ValueError(f"{i} 番目の値が無い。#assign の値の個数を確かめる") from None


def parse_data(text: str) -> dict:
    """検査に要る値だけを入力データから拾う。汎用の読み取りではない。

    MiniZinc の .dzn を使うなら、下のように「要る名前だけ」を拾う。
    JSON を使うなら json.loads で置き換える。
    """
    text = re.sub(r"%[^\n]*", "", text)          # .dzn のコメントを落とす
    out: dict = {}
    for key in ("n", "k"):                       # 整数のパラメータ
        m = re.search(rf"\b{key}\s*=\s*(-?\d+)\s*;", text)
        if m:
            out[key] = int(m.group(1))
    # 配列を拾う例（要るものだけ足す）:
    # m = re.search(r"\bcap\s*=\s*\[([^\]]*)\]\s*;", text)
    # if m:
    #     out["cap"] = [int(v) for v in re.findall(r"-?\d+", m.group(1))]
    return out


# ── ハード制約の検査 ────────────────────────────────────────
#
# 企画書の H1・H2・… に1つずつ対応させる。関数名にも番号を残しておくと、
# 「どの条件を検査していないか」が一目で分かる。

def check_h1(assign: dict[str, list], data: dict) -> list[str] | None:
    """H1. <企画書に書いた条件の文をそのまま写す>

    TODO(1) この関数の中身を書く。

      - assign は「対象の名前 → 値のリスト」の辞書である。
        決めることが1つなら slot = column(assign) で「名前 → 値」に直せる。
        2つなら slot = column(assign, 0)、room = column(assign, 1) と分ける。
      - 条件を破っている箇所を見つけたら、次の書き方で違反を1件足す。
            bad.append(f"{name} の値が {value} になっている")
      - 最後に bad を返す。違反が無ければ空のリストが返る。

    書く前は None を返す。検証器は「この検査はまだ空である」と知らせて先へ進む。
    """
    return None                                  # ← TODO(1) ここを書き換える


def check_h2(assign: dict[str, list], data: dict) -> list[str] | None:
    """H2. <企画書に書いた条件の文をそのまま写す>

    条件の数だけ、この形の関数を足す。足したら CHECKS にも1行足す。
    """
    return None


# 検査の一覧。(表示名, 関数) の組を並べる。条件を足したらここにも足す。
CHECKS = [
    ("H1", check_h1),
    ("H2", check_h2),
]


# ── ソフト制約・目的関数を数え直す ──────────────────────────

def recount(assign: dict[str, list], data: dict) -> dict[str, int] | None:
    """モデルの #value と突き合わせる値を、こちら側で計算する。

    TODO(2) ソフト制約または目的関数があるなら、この関数の中身を書く。

      - 企画書の S1・S2・… を1つずつ数える。
      - 目的関数の値（重み付き和）も計算して返す。
      - 返す辞書のキーは、モデルが出している #value の名前と揃える。

    目的が無い問題（充足だけを求める）は、この関数を使わない。
    その場合は None を返したままでよい。
    """
    return None                                  # ← TODO(2) ここを書き換える


# ── まとめて検査する ────────────────────────────────────────

def verify(out_text: str, data_text: str = "") -> tuple[bool, list[str], list[str]]:
    """(合格したか, 違反の一覧, まだ書かれていない検査の一覧) を返す。"""
    assign, values, size = parse_output(out_text)
    data = parse_data(data_text) if data_text else {}

    # 出力とデータファイルが組になっているかを先に見る。
    # 別々のものを渡すと、この先の検査は黙って的外れな答えを返す。
    if "n" in data and len(assign) != data["n"]:
        raise ValueError(
            f"出力の対象数（{len(assign)}）とデータファイル（{data['n']}）が合わない。"
            "出力を作ったときと同じデータファイルを渡す")

    problems: list[str] = []
    skipped: list[str] = []

    for label, check in CHECKS:
        found = check(assign, data)
        if found is None:
            skipped.append(f"{label} の検査")
        else:
            problems += found

    got = recount(assign, data)
    if got is None:
        if values:
            skipped.append("#value の数え直し")
    else:
        for key, expected in got.items():
            if key in values and values[key] != expected:
                problems.append(
                    f"{key} がモデルの出力（{values[key]}）と一致しない"
                    f"（独立に計算すると {expected}）")

    return not problems, problems, skipped


def main(argv: list[str]) -> int:
    if not 2 <= len(argv) <= 3:
        print(__doc__)
        return 2
    out_text = Path(argv[1]).read_text(encoding="utf-8")
    data_text = Path(argv[2]).read_text(encoding="utf-8") if len(argv) == 3 else ""

    try:
        ok, problems, skipped = verify(out_text, data_text)
    except ValueError as error:                  # 読み取りの段階でつまずいた
        print("検査できない:", error)
        return 2

    print("合格" if ok else "不合格")
    for problem in problems:
        print(" -", problem)
    for item in skipped:
        print(" (未実装)", item)
    if skipped:
        print()
        print("未実装の検査がある。合格は「書いた検査を通った」以上のことを意味しない。")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
