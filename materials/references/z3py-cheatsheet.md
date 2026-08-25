---
description: 第05〜06回で使うZ3PyのAPI早見表。Bool・Int・論理演算・Solverの操作・解の読み方・Optimizeの入口を、初出回への案内つきでまとめる
---

# Z3Py 早見表

第05〜06回で**実際に使う API だけ**を並べてある。
Z3 の全機能ではない。導入のしかたは
[Z3 実行環境の使い方](setup-z3.md)を見る。

::: note
この表の「初出」は、その API を最初に使う回である。
まだ習っていない API は、この表にも載せていない。
:::

## 一覧

| 書き方 | 読み | 初出 |
|---|---|---|
| `from z3 import *` | Z3 の名前をまとめて読み込む | [第05回](../sessions/05-sat-dependencies.md) |
| `Bool("p")` | 真偽の変数を1つ作る | [第05回](../sessions/05-sat-dependencies.md) |
| `Bools("p q r")` | 真偽の変数をまとめて作る | [第05回](../sessions/05-sat-dependencies.md) |
| `Not(a)` | 否定 | [第05回](../sessions/05-sat-dependencies.md) |
| `And(a, b)` / `And([...])` | 論理積（かつ） | [第05回](../sessions/05-sat-dependencies.md) |
| `Or(a, b)` / `Or([...])` | 論理和（または） | [第05回](../sessions/05-sat-dependencies.md) |
| `Implies(a, b)` | 含意（`a` ならば `b`） | [第05回](../sessions/05-sat-dependencies.md) |
| `s = Solver()` | ソルバーを作る | [第05回](../sessions/05-sat-dependencies.md) |
| `s.add(制約)` | 制約を足す | [第05回](../sessions/05-sat-dependencies.md) |
| `s.check()` | 解けるかどうかを調べる | [第05回](../sessions/05-sat-dependencies.md) |
| `sat` / `unsat` / `unknown` | `check()` の結果 | [第05回](../sessions/05-sat-dependencies.md) |
| `s.model()` | 見つかった割り当てを取り出す | [第05回](../sessions/05-sat-dependencies.md) |
| `is_true(m[x])` | 真偽変数の値を Python の真偽値で読む | [第05回](../sessions/05-sat-dependencies.md) |
| `Int("n")` / `Ints("a b")` | 整数の変数を作る | [第06回](../sessions/06-smt-versions.md) |
| `x == y` `x != y` `x <= y` `x < y` | 比較（制約になる） | [第06回](../sessions/06-smt-versions.md) |
| `m[x].as_long()` | 整数変数の値を Python の `int` で読む | [第06回](../sessions/06-smt-versions.md) |
| `s.push()` / `s.pop()` | 制約を一時的に足して戻す | [第06回](../sessions/06-smt-versions.md) |
| `Optimize()` と `minimize` / `maximize` | 目的の値が最も良い解を探す | [第06回](../sessions/06-smt-versions.md)（発展） |
| `Sum([...])` / `If(条件, a, b)` | 足し合わせる／場合分けする（数え上げに使う） | [第06回](../sessions/06-smt-versions.md)（発展） |

## 基本の形

Z3 のプログラムは、どれも同じ4段構えになる。

```{.z3py filename="骨格"}
from z3 import *

# 1. 変数を作る
p, q = Bools("p q")

# 2. ソルバーに制約を足す
s = Solver()
s.add(Or(p, q))
s.add(Not(p))

# 3. 解けるかどうかを調べる
if s.check() == sat:
    # 4. 割り当てを読む
    m = s.model()
    print("p =", is_true(m[p]), " q =", is_true(m[q]))
else:
    print("条件を同時に満たす割り当ては無い")
```

```solver
p = False  q = True
```

## 判定は `== sat` で書く

::: warning
**`if s.check():` と書いてはいけない。**
`check()` が返すのは `sat` / `unsat` / `unknown` という値であって、真偽値ではない。
Python はこれをすべて「真」と見なすので、`unsat` でも分岐に入ってしまう。
:::

```{.z3py filename="判定の書き分け"}
r = s.check()

if r == sat:
    m = s.model()          # 解があるときだけ model() を呼べる
elif r == unsat:
    print("同時に満たせない")
else:
    print("分からなかった（unknown）")
```

`unsat` のときに `s.model()` を呼ぶと
`Z3Exception: model is not available` になる。

## Python の `and` / `or` / `not` は使えない

Z3 の式は Python の真偽値ではないので、Python の演算子では組み立てられない。

```{.z3py filename="間違い"}
s.add(p and q)          # Z3Exception になる
s.add(not p)            # 同上
```

```{.z3py filename="正しい書き方"}
s.add(And(p, q))
s.add(Not(p))
```

一方、比較演算子（`==` `!=` `<=` `<`）は Z3 の式を返すので**そのまま使える**。

## 変数をまとめて作る

題材の要素が増えると、変数を1つずつ手で書くのは現実的でない。
辞書に入れて名前で引けるようにする。

```{.z3py filename="辞書で持つ"}
PACKAGES = ["editor", "parser", "logger"]

use = {name: Bool(f"use_{name}") for name in PACKAGES}

s = Solver()
s.add(use["editor"])
s.add(Implies(use["editor"], use["parser"]))
s.add(Not(And(use["parser"], use["logger"])))

if s.check() == sat:
    m = s.model()
    for name in PACKAGES:
        print(name, is_true(m[use[name]]))
```

```solver
editor True
parser True
logger False
```

## 「ちょうど一つ」を書く

選択肢のうち1つだけを選ぶ、という条件は
**「少なくとも一つ」と「高々一つ」に分けて**書く。

```{.z3py filename="ちょうど一つ"}
choices = [Bool(f"c{i}") for i in range(3)]

s = Solver()
s.add(Or(choices))                              # 少なくとも一つ
for i in range(len(choices)):
    for j in range(i + 1, len(choices)):
        s.add(Or(Not(choices[i]), Not(choices[j])))   # 高々一つ
```

考え方は [SAT・SMT 概説](logic-sat-smt.md)に、
グラフ彩色での使い方は[グラフ彩色の3つの表現](graph-coloring.md)にある。

## 整数変数（[第06回](../sessions/06-smt-versions.md)）

```{.z3py filename="整数"}
n = Int("n")
a, b = Ints("a b")

s = Solver()
s.add(n >= 0, n <= 3)                # add は複数の制約をまとめて受け取れる
s.add(a != b)
s.add(Implies(n != 0, a >= 1))
```

値を読むときは `as_long()` で Python の `int` に変換する。

```{.z3py filename="整数の値を読む"}
if s.check() == sat:
    m = s.model()
    print(m[n].as_long() + 1)
```

::: warning
`m[n]` は Z3 の値（`IntNumRef`）であって Python の `int` ではない。
`m[n] + 1` と書くと `3 + 1` という**式**が表示されるだけで、計算されない。
`as_long()` を通してから計算する。
:::

::: note
制約に一度も現れない変数を `m[x]` で引くと `None` が返る。
「値が入っていない」ときは、その変数を制約に入れ忘れていないか確かめる。
:::

## 制約を試しに足して戻す

「この条件を足したら解けなくなるか」を調べるときに使う。

```{.z3py filename="push と pop"}
s.push()                 # ここまでの状態を覚える
s.add(n < 0)
print(s.check())         # unsat
s.pop()                  # 足した制約を捨てて元に戻す
print(s.check())         # sat
```

## 数え上げ（`Sum` と `If`）

「条件を満たすものがいくつあるか」を式にするときに使う。
最適化の目的関数を作るための道具である。

```{.z3py filename="数える"}
changes = Sum([If(v[name] != CURRENT[name], 1, 0) for name in PACKAGES])
```

`If(条件, a, b)` は、条件が成り立てば `a`、そうでなければ `b` になる**式**である
（Python の `if` 文ではない）。
`Sum([...])` は Z3 の式のリストを足し合わせる。

::: note
MiniZinc の `sum` + `bool2int` と同じ考え方である
（[MiniZinc 早見表](minizinc-cheatsheet.md)の「集計と数え上げ」）。
:::

## `Optimize`（[第06回](../sessions/06-smt-versions.md)の発展）

`Solver()` は「条件を満たすものを1つ」返す。
**目的の値がいちばん良いもの**を返してほしいときは `Optimize()` を使う。
第06回の発展演習で入口だけ触れる。

```{.z3py filename="入口だけ"}
o = Optimize()
o.add(制約)                       # 制約の足し方は Solver と同じ
o.minimize(式)                    # または o.maximize(式)
if o.check() == sat:
    m = o.model()
```

::: note
**最適化そのものは[第07回](../sessions/07-theme-assignment.md)から MiniZinc で扱う。**
目的関数の設計・重み付け・公平性は、そちらが本番である。
ここで覚えるのは「Z3 にも同じことができる入口がある」ということだけでよい。
:::

## `Bool` と `Int` の使い分け

| 表したいもの | 型 | 例 |
|---|---|---|
| 入れるか入れないかの2択 | `Bool` | パッケージを導入するか（[第05回](../sessions/05-sat-dependencies.md)） |
| いくつかの選択肢から1つ | `Bool` を選択肢の数だけ + 「ちょうど一つ」 | 地区の色（[第05回](../sessions/05-sat-dependencies.md)） |
| 順序や大小に意味がある数 | `Int` | パッケージのバージョン番号（[第06回](../sessions/06-smt-versions.md)） |

判断の指針は [SAT・SMT 概説](logic-sat-smt.md)の「型の選び方」にある。

## この科目では使わない API

| API | 何をするもの | この科目では |
|---|---|---|
| `Real` / `BitVec` | 実数・ビット列の変数 | 名前と用途だけ [SAT・SMT 概説](logic-sat-smt.md)に載せる |
| `unsat_core()` | 矛盾の原因になった制約の抽出 | 扱わない |
| `Tactic` / `Goal` | 求解の手順の指定 | 扱わない |
| SMT-LIB ファイルの読み書き | 別形式での入出力 | Python からだけ呼ぶ |

自由課題でこれらが必要になったら
[Z3 の公式ガイド](https://z3prover.github.io/papers/programmingz3.html)を見る。

## 関連ページ

- [Z3 実行環境の使い方](setup-z3.md) — 導入・バージョン確認・最小動作確認
- [SAT・SMT 概説](logic-sat-smt.md) — 真理値表・CNF・Boolean 符号化・型の選び方
- [よくあるエラーと対処](errors.md) — Z3 の例外とその読み方
- [用語集](glossary.md) — 命題変数・充足可能性・SMT などの定義
