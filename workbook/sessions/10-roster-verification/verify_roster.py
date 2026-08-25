#!/usr/bin/env python3
"""第10回 勤務表の検証器 — 穴埋め前

教材ページ: 講義（全15回）> 第10回 勤務表: 検証と性能評価
実行環境:   Python 3（外部ライブラリは要らない。Z3 も MiniZinc も使わない）

MiniZinc が出した勤務表を、**モデルとはまったく別のところで**検査する。
モデルに「合っていますか」と聞かないのが要点である。

    python3 verify_roster.py samples/good-small.txt small_pref.dzn
    python3 verify_roster.py --samples

読み取るのは、第09回の配布モデルが出している次の行である。

    #size <人数> <日数>
    #shift <名前> <D/N/O の並び>
    #value pref <整数>          … TODO を埋めたモデルだけが出す
    #value unfair <整数>
    #value night_unfair <整数>
    #value penalty <整数>

TODO は2か所ある。TODO(1) が必須演習、TODO(2) が標準演習である。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# 出力の1文字表記。enum SHIFTS = { day, night, off } に対応する。
DAY, NIGHT, OFF = "D", "N", "O"


# ── モデルの出力を読む ──────────────────────────────────────

def parse_output(text: str) -> tuple[list[str], list[str], dict[str, int]]:
    """モデルの出力から、職員名・シフトの並び・#value を取り出す。

    最適化では解が何本も出る。**最後の解だけ**を残す。
    """
    names: list[str] = []
    rows: list[str] = []
    values: dict[str, int] = {}
    size: tuple[int, int] | None = None
    for line in text.splitlines():
        m = re.match(r"^#size\s+(\d+)\s+(\d+)\s*$", line)
        if m:
            size = (int(m.group(1)), int(m.group(2)))
            names, rows, values = [], [], {}
            continue
        m = re.match(r"^#shift\s+(\S+)\s+([DNO]+)\s*$", line)
        if m:
            names.append(m.group(1))
            rows.append(m.group(2))
            continue
        m = re.match(r"^#value\s+(\w+)\s+(-?\d+)\s*$", line)
        if m:
            values[m.group(1)] = int(m.group(2))
    if size is None:
        raise ValueError("#size の行が無い。出力を全部コピーできているか確かめる")
    if (len(rows), len(rows[0]) if rows else 0) != size:
        raise ValueError(f"#size {size} と #shift の行数・長さが合わない")
    return names, rows, values


def parse_dzn(text: str) -> dict:
    """検査に要る値だけを .dzn から拾う。汎用の dzn 読み取りではない。"""
    text = re.sub(r"%[^\n]*", "", text)          # コメントを落とす
    out: dict = {}
    for key in ("ns", "nd"):
        m = re.search(rf"\b{key}\s*=\s*(\d+)\s*;", text)
        out[key] = int(m.group(1))
    for key in ("need_day", "need_night"):
        m = re.search(rf"\b{key}\s*=\s*\[([^\]]*)\]\s*;", text)
        out[key] = [int(v) for v in re.findall(r"-?\d+", m.group(1))]
    m = re.search(r"\bleader\s*=\s*\[([^\]]*)\]\s*;", text)
    out["leader"] = [v == "true" for v in re.findall(r"true|false", m.group(1))]
    m = re.search(r"\bwant_off\s*=\s*array2d\([^,]*,[^,]*,\s*\[(.*?)\]\s*\)\s*;", text, re.S)
    flat = [v == "true" for v in re.findall(r"true|false", m.group(1))] if m else []
    out["want_off"] = [flat[i * out["nd"]:(i + 1) * out["nd"]] for i in range(out["ns"])]
    for key in ("w_pref", "w_fair", "w_night"):
        m = re.search(rf"\b{key}\s*=\s*(-?\d+)\s*;", text)
        out[key] = int(m.group(1)) if m else 0
    return out


# ── ハード制約の検査 ────────────────────────────────────────
#
# どの関数も「見つけた違反を日本語で並べたリスト」を返す。
# 空のリストが返れば、その検査は通ったという意味である。

def check_coverage(rows: list[str], data: dict) -> list[str]:
    """必要人数: どの日も日勤・夜勤がちょうど決まった人数になっているか。"""
    bad = []
    for d in range(data["nd"]):
        col = [r[d] for r in rows]               # d 日目の列（全職員ぶん）
        if col.count(DAY) != data["need_day"][d]:
            bad.append(f"{d + 1}日目の日勤が {col.count(DAY)} 名（必要 {data['need_day'][d]} 名）")
        if col.count(NIGHT) != data["need_night"][d]:
            bad.append(f"{d + 1}日目の夜勤が {col.count(NIGHT)} 名（必要 {data['need_night'][d]} 名）")
    return bad


def check_qualification(rows: list[str], data: dict) -> list[str] | None:
    """資格: どの日も、夜勤に入る人のうち1人以上がリーダー資格を持つか。

    TODO(1) 必須演習: この関数の中身を書く。

      - 日 d の列を見て、「その日が夜勤」かつ「資格を持つ」職員を数える。
      - 職員 s が資格を持つかどうかは data["leader"][s]（True / False）で分かる。
      - 0 名の日があれば、次の書き方で違反を1件足す。
            bad.append(f"{d + 1}日目の夜勤に資格者がいない")
      - 最後に bad を返す。違反が無ければ空のリストが返る。

    書く前は None を返す。検証器は「この検査はまだ空である」と知らせて先へ進む。
    """
    return None                                  # ← TODO(1) ここを書き換える


def check_rest(rows: list[str], names: list[str], data: dict) -> list[str]:
    """休息: 夜勤に入った翌日が休みになっているか。"""
    bad = []
    for s, r in enumerate(rows):
        for d in range(data["nd"] - 1):          # 最終日の翌日は無い
            if r[d] == NIGHT and r[d + 1] != OFF:
                bad.append(f"職員{names[s]} の {d + 1}日目が夜勤なのに翌日が休みでない")
    return bad


# ── ペナルティを計算し直す ──────────────────────────────────

def count_pref(rows: list[str], data: dict) -> int | None:
    """希望休違反の件数を、モデルとは独立に数える。

    TODO(2) 標準演習: この関数の中身を書く。

      - data["want_off"][s][d] が True なら、職員 s は d 日目に休みを希望している。
      - その日が休み（OFF）でなければ違反1件である。
      - 全職員・全日を見て、違反の件数を返す。

    書く前は None を返す。そのあいだ、pref と penalty の突き合わせは飛ばされる。
    """
    return None                                  # ← TODO(2) ここを書き換える


def recompute(rows: list[str], data: dict) -> dict[str, int]:
    """モデルの #value と突き合わせる値を、こちら側で計算する。"""
    works = [sum(1 for c in r if c != OFF) for r in rows]     # 勤務日数
    nights = [r.count(NIGHT) for r in rows]                   # 夜勤の回数
    got = {
        "unfair": max(works) - min(works),
        "night_unfair": max(nights) - min(nights),
    }
    pref = count_pref(rows, data)
    if pref is not None:
        got["pref"] = pref
        got["penalty"] = (data["w_pref"] * pref
                          + data["w_fair"] * got["unfair"]
                          + data["w_night"] * got["night_unfair"])
    return got


# ── まとめて検査する ────────────────────────────────────────

def verify(out_text: str, dzn_text: str) -> tuple[bool, list[str], list[str]]:
    """(合格したか, 違反の一覧, まだ書かれていない検査の一覧) を返す。"""
    names, rows, values = parse_output(out_text)
    data = parse_dzn(dzn_text)

    # 出力とデータファイルが組になっているかを先に見る。
    # 別々のものを渡すと、この先の検査は黙って的外れな答えを返す。
    if (len(rows), len(rows[0])) != (data["ns"], data["nd"]):
        raise ValueError(
            f"出力の大きさ（{len(rows)}人 {len(rows[0])}日）と"
            f"データファイル（{data['ns']}人 {data['nd']}日）が合わない。"
            "出力を作ったときと同じデータファイルを渡す")

    problems: list[str] = []
    skipped: list[str] = []

    problems += check_coverage(rows, data)

    qualification = check_qualification(rows, data)
    if qualification is None:
        skipped.append("資格の検査（TODO(1)）")
    else:
        problems += qualification

    problems += check_rest(rows, names, data)

    got = recompute(rows, data)
    if "pref" not in got:
        skipped.append("希望休違反の数え上げ（TODO(2)）")
    for key in ("pref", "unfair", "night_unfair", "penalty"):
        if key in values and key in got and values[key] != got[key]:
            problems.append(
                f"{key} がモデルの出力（{values[key]}）と一致しない"
                f"（独立に計算すると {got[key]}）")

    return not problems, problems, skipped


def run_one(out_path: Path, dzn_path: Path) -> bool:
    try:
        ok, problems, skipped = verify(out_path.read_text(encoding="utf-8"),
                                       dzn_path.read_text(encoding="utf-8"))
    except ValueError as e:                      # 読み取りの段階でつまずいた
        print("検査できない:", e)
        return False
    print("合格" if ok else "不合格")
    for p in problems:
        print(" -", p)
    for s in skipped:
        print(" (未実装)", s)
    return ok


# ── 同梱の例をまとめて判定する ──────────────────────────────
#
# 正常例は合格、反例は不合格になるはずである。
# **反例で不合格になること**まで確かめて、はじめて検査が働いていると言える。

SAMPLES = [
    ("samples/good-small.txt",            "small_pref.dzn", True),
    ("samples/good-week.txt",             "week_pref.dzn",  True),
    ("samples/broken-coverage.txt",       "small_pref.dzn", False),
    ("samples/broken-qualification.txt",  "small_pref.dzn", False),
    ("samples/broken-rest.txt",           "small_pref.dzn", False),
    ("samples/broken-value.txt",          "small_pref.dzn", False),
    ("samples/dropped-qualification.txt", "week_pref.dzn",  False),
    ("samples/dropped-rest.txt",          "week_pref.dzn",  False),
]


def run_samples() -> int:
    all_as_expected = True
    unwritten: list[str] = []
    for out_name, dzn_name, expect_ok in SAMPLES:
        ok, problems, skipped = verify((HERE / out_name).read_text(encoding="utf-8"),
                                       (HERE / dzn_name).read_text(encoding="utf-8"))
        for s in skipped:
            if s not in unwritten:
                unwritten.append(s)
        agrees = (ok == expect_ok)
        all_as_expected = all_as_expected and agrees
        print(f"{Path(out_name).name:32s} 期待 {'合格' if expect_ok else '不合格'}"
              f" / 結果 {'合格' if ok else '不合格'}"
              f"  {'期待どおり' if agrees else '← 期待と違う'}")
        for p in problems:
            print("      -", p)
    print()
    for s in unwritten:
        print("まだ書かれていない検査:", s)
    print("すべて期待どおりである。" if all_as_expected
          else "期待と違う行がある。検査関数を見直すこと。")
    return 0 if all_as_expected else 1


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--samples":
        sys.exit(run_samples())
    if len(sys.argv) == 3:
        sys.exit(0 if run_one(Path(sys.argv[1]), Path(sys.argv[2])) else 1)
    print(__doc__)
    sys.exit(2)
