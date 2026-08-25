---
description: 架空の市の5地区を3色で塗り分ける同じ問題を、Prolog・MiniZinc・Z3のBoolean符号化の3通りで書き比べる比較リファレンス
---

# グラフ彩色の3つの表現

**同じ問題**を Prolog（第02回）・MiniZinc（第03回）・Z3 の Boolean 符号化（第05回）で書いたものを、
1ページに並べてある。回をまたいで戻ってくるための比較用のページである。

::: important
見るべきなのは「どれが優れているか」ではない。
**問題そのものは同じで、変わったのは表現だけ**である。
何を書き、何を書かずに済ませたかを見比べる。
:::

## 問題

架空の市に5つの地区がある。隣り合う地区が同じ色にならないように、
3色（赤・緑・青）で塗り分ける。

![架空の5地区（北区・南区・東区・西区・中央区）の隣接関係と、3色で塗り分けた解の一例。中央区は他の4地区すべてと隣り合い、外側は北・東・南・西の順に環になっていて、辺は全部で8本ある。左は問題で、辺で結ばれた2地区が隣り合っていることを表す。右は解の一例で、どの辺の両端も異なる色になっている。](figures/graph-5districts.svg)

| 要素 | 内容 |
|---|---|
| 頂点（地区） | 北区・南区・東区・西区・中央区 |
| 辺（隣接） | 中央区は他の4地区すべてと隣り合う。外側は 北 → 東 → 南 → 西 → 北 の順に隣り合う |
| 色 | 赤・緑・青の3色 |
| 求めるもの | どの辺の両端も色が違う塗り分け |

3色での塗り分けは複数ある。**2色にすると解が無くなる**（UNSAT）。
どの表現でも、色を1つ減らして確かめられる。

## 3つの表現を1行で

| | 変数にあたるもの | 「違う色」の書き方 | 「1地区に1色」の保証 |
|---|---|---|---|
| Prolog | 地区ごとの変数 `Kita` など | `Kita \= Chuo` | 変数に値が1つしか入らないので自動 |
| MiniZinc | `paint[kita]` などの決定変数 | `paint[kita] != paint[chuo]` | 決定変数の定義域が色の集合なので自動 |
| Z3（Boolean） | 地区 × 色の真偽変数 `x[kita, red]` | 同じ色の変数が同時に真にならない | **明示的に書く必要がある**（ちょうど一つ） |

**表現が保証してくれる性質と、自分で書かなければならない性質が入れ替わる**のが要点である。

## Prolog（第02回）

候補を生成して条件で落とす「生成とテスト」で書く。

```{.prolog filename="coloring.pl"}
% 架空の市の5地区を3色で塗り分ける
color(red).
color(green).
color(blue).

% 中央区は北区・南区・東区・西区のすべてと隣り合う
% 外側は 北 - 東 - 南 - 西 - 北 の順に隣り合う
paint(Kita, Minami, Higashi, Nishi, Chuo) :-
    color(Kita), color(Minami), color(Higashi), color(Nishi), color(Chuo),
    Kita    \= Chuo,
    Minami  \= Chuo,
    Higashi \= Chuo,
    Nishi   \= Chuo,
    Kita    \= Higashi,
    Higashi \= Minami,
    Minami  \= Nishi,
    Nishi   \= Kita.
```

クエリ `paint(Kita, Minami, Higashi, Nishi, Chuo)` を実行する。

```text
解 1: Kita = red, Minami = red, Higashi = green, Nishi = green, Chuo = blue.
```

「次の解」を押すと別の塗り分けが出る。押し続けると `false.` になり、
それ以上は無いことが分かる。

::: {.hint summary="実行ページで開く"}
[グラフ彩色のサンプルを読み込んだ状態で実行ページを開く](../../tools/prolog/?example=graph-coloring)
:::

**この表現の特徴**

- 5つの `color(...)` が候補の生成、8つの `\=` がテストである。
- **探索の順序を自分で書いている**。`color(Kita), color(Minami), ...` を並べた順に候補が作られる。
- 地区が増えると、行を1つずつ足していくことになる。
- 「1地区に1色」は、変数に値が1つしか入らないという Prolog の性質が保証している。

## MiniZinc（第03回）

条件だけを書き、どう探すかはソルバーに任せる。

```{.minizinc filename="coloring.mzn"}
enum DISTRICTS = { kita, minami, higashi, nishi, chuo };
enum COLORS    = { red, green, blue };

array[DISTRICTS] of var COLORS: paint;

% 隣り合う地区の組
set of int: EDGES = 1..8;
array[EDGES, 1..2] of DISTRICTS: edge =
  [| kita,    chuo
   | minami,  chuo
   | higashi, chuo
   | nishi,   chuo
   | kita,    higashi
   | higashi, minami
   | minami,  nishi
   | nishi,   kita |];

constraint forall(e in EDGES)(
  paint[edge[e, 1]] != paint[edge[e, 2]]
);

solve satisfy;

output [ show(d) ++ ": " ++ show(paint[d]) ++ "\n" | d in DISTRICTS ];
```

```solver
kita: blue
minami: blue
higashi: green
nishi: green
chuo: red
----------
```

::: note
Playground の既定のソルバー（Gecode）で実行した結果である。
3色での塗り分けは1通りではないので、
ソルバーを替えると色の名前が入れ替わった別の解が返ることがある。
:::

**この表現の特徴**

- **隣接関係がデータになった**。地区や辺が増えても `edge` の行を足すだけで、制約は1つのままである。
- 探索の順序はどこにも書いていない。`solve satisfy;` がソルバーへの指示のすべてである。
- `var COLORS` と書いた時点で、定義域（3色のどれか）が決まる。
- Prolog 版の8行の `\=` が、`forall` 1つに畳まれている。

::: note
色を2色にするには `enum COLORS = { red, green };` に書き換える。
`=====UNSATISFIABLE=====` が出る。
:::

::: note
第03回の配布ファイル `coloring5.mzn` は、**同じ内容を `enum` を使わずに書いてある**。
地区も色も `1` から始まる番号で表し、名前は表示用の文字列の配列で持っている。
`enum` を導入するのは[第08回](../sessions/08-roster-hard.md)なので、
第03回の時点では番号のまま扱う。辺の本数と隣接関係はこのページとまったく同じである。
:::

## Z3 の Boolean 符号化（第05回）

真偽変数だけで表す。**「地区 $d$ を色 $c$ で塗る」を1つの真偽変数**にする。

$$x_{d,c} = \text{真} \iff \text{地区 } d \text{ を色 } c \text{ で塗る}$$

地区5つ × 色3つで、真偽変数は15個になる。

```{.z3py filename="coloring.py"}
from z3 import *

DISTRICTS = ["kita", "minami", "higashi", "nishi", "chuo"]
COLORS = ["red", "green", "blue"]
EDGES = [
    ("kita", "chuo"), ("minami", "chuo"), ("higashi", "chuo"),
    ("nishi", "chuo"), ("kita", "higashi"), ("higashi", "minami"),
    ("minami", "nishi"), ("nishi", "kita"),
]

# 地区 d を色 c で塗るなら真
x = {(d, c): Bool(f"x_{d}_{c}") for d in DISTRICTS for c in COLORS}

s = Solver()

# 各地区はちょうど一つの色で塗る
for d in DISTRICTS:
    s.add(Or([x[d, c] for c in COLORS]))                     # 少なくとも一つ
    for i in range(len(COLORS)):
        for j in range(i + 1, len(COLORS)):
            s.add(Or(Not(x[d, COLORS[i]]), Not(x[d, COLORS[j]])))   # 高々一つ

# 隣り合う地区は同じ色にしない
for a, b in EDGES:
    for c in COLORS:
        s.add(Or(Not(x[a, c]), Not(x[b, c])))

if s.check() == sat:
    m = s.model()
    for d in DISTRICTS:
        for c in COLORS:
            if is_true(m[x[d, c]]):
                print(d, c)
else:
    print("塗り分けられない")
```

```solver
kita blue
minami blue
higashi green
nishi green
chuo red
```

**この表現の特徴**

- **「1地区に1色」を自分で書かなければならない**。
  他の2つでは表現そのものが保証していた性質である。書き忘れると、
  1つの地区に2色が同時に真になる割り当てが返ってくる。
- 「隣り合う地区は違う色」は、色ごとに「両方は真にならない」と書く。
- 解を読むときも、真になっている変数を探す一手間が要る。
- そのかわり、**条件がすべて論理式だけで表せている**。
  SAT ソルバーが受け取れる形に最も近い。

::: note
色を2色にするには `COLORS = ["red", "green"]` に書き換える。`unsat` が出る。
:::

## 書き比べてみる

3つを並べたときに気付いてほしいことを挙げておく。
第03回・第05回の考察の材料である。

::: {.discuss}
1. **同じ条件が、どこに現れたか。** 「隣り合う地区は違う色」は
   3つの表現でそれぞれどう書かれているか。
2. **書かなくて済んだ条件はどれか。** 「1地区に1色」は Prolog と MiniZinc では
   書いていない。なぜ書かずに済んだのか。
3. **地区が20に増えたら、どれが一番書き換えが少ないか。**
4. **探索の順序を決めているのは誰か。** 3つの表現で答えが違う。
:::

## 発展の方向

授業では扱わないが、自由課題で伸ばすならこの向きがある。

| 発展 | 内容 |
|---|---|
| 彩色数の最小化 | 「3色で塗れるか」ではなく「最小で何色必要か」を問う。目的関数が要る（[第07回](../sessions/07-theme-assignment.md)の道具） |
| 対称性の除去 | 色の名前を入れ替えただけの解を数えないようにする。たとえば北区の色を固定する |
| 規模を大きくする | 実在しない地図を自動生成し、地区数を増やしたときの解けかたを比べる |
| 隣接データを外に出す | 隣接関係を `.dzn` やテキストファイルに分け、地図を差し替えられるようにする（第04回の道具） |

## 関連ページ

- [Prolog 早見表](prolog-cheatsheet.md) / [MiniZinc 早見表](minizinc-cheatsheet.md) / [Z3Py 早見表](z3py-cheatsheet.md)
- [SAT・SMT 概説](logic-sat-smt.md) — 「ちょうど一つ」などの符号化の考え方
- [定式化の7手順](modeling-steps.md) — 問題を分解する順序
- [用語集](glossary.md) — グラフ・彩色問題・Boolean 符号化などの定義
