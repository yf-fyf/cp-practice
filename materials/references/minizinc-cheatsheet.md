---
description: 第03〜04回と第07〜10回で使うMiniZinc構文の早見表。パラメータ・決定変数・配列・forall・大域制約・最適化・enum・集計を、初出回への案内つきでまとめる
---

# MiniZinc 早見表

この科目で**実際に使う書き方だけ**を並べてある。
MiniZinc の全構文ではない。実行のしかたは
[MiniZinc 実行環境の使い方](setup-minizinc.md)を見る。

::: note
この表の「初出」は、その書き方を最初に使う回である。
まだ習っていない書き方は、この表にも載せていない。
:::

## 一覧

| 書き方 | 読み | 初出 |
|---|---|---|
| `% 説明` | コメント（行末まで） | [第03回](../sessions/03-minizinc-sudoku.md) |
| `include "globals.mzn";` | 大域制約を使う宣言 | [第03回](../sessions/03-minizinc-sudoku.md) |
| `int: n = 4;` | パラメータ（値が決まっている） | [第03回](../sessions/03-minizinc-sudoku.md) |
| `var 1..4: y;` | 決定変数と定義域 | [第03回](../sessions/03-minizinc-sudoku.md) |
| `set of int: ROWS = 1..4;` | 添字集合に名前を付ける | [第03回](../sessions/03-minizinc-sudoku.md) |
| `array[ROWS, COLS] of var 1..4: x;` | 2次元の決定変数の並び | [第03回](../sessions/03-minizinc-sudoku.md) |
| `constraint 条件;` | 制約を1つ足す | [第03回](../sessions/03-minizinc-sudoku.md) |
| `forall(r in ROWS)( 条件 )` | すべての `r` について条件が成り立つ | [第03回](../sessions/03-minizinc-sudoku.md) |
| 配列内包表記 `[ 式 … 変数 in 集合 ]` | 集合の各要素から作った配列（下の例を見る） | [第03回](../sessions/03-minizinc-sudoku.md) |
| `A -> B` | ならば（含意） | [第03回](../sessions/03-minizinc-sudoku.md) |
| `A /\ B` | かつ（両方成り立つ） | [第03回](../sessions/03-minizinc-sudoku.md) |
| `A \/ B` | または（少なくとも一方が成り立つ） | （記法対応表のため。本文では使わない） |
| `not A` | 〜でない | （記法対応表のため。本文では使わない） |
| `all_different(配列)` | 要素が互いに異なる | [第03回](../sessions/03-minizinc-sudoku.md) |
| `solve satisfy;` | 解を1つ見つける | [第03回](../sessions/03-minizinc-sudoku.md) |
| `output [ ... ];` | 解の出し方を整える | [第03回](../sessions/03-minizinc-sudoku.md) |
| `int: n;`（値なし） | `.dzn` から受け取るパラメータ | [第04回](../sessions/04-sudoku-data-uniqueness.md) |
| `array2d(1..n, 1..n, [ ... ])` | `.dzn` での2次元データ | [第04回](../sessions/04-sudoku-data-uniqueness.md) |
| `exists(r in S)( 条件 )` | 条件が成り立つ `r` が少なくとも1つある | [第04回](../sessions/04-sudoku-data-uniqueness.md) |
| `solve maximize 式;` / `solve minimize 式;` | 最適化 | [第07回](../sessions/07-theme-assignment.md) |
| `sum(i in S)( 式 )` | 合計 | [第07回](../sessions/07-theme-assignment.md) |
| `count(配列, 値)` / `count(i in S)( 条件 )` | 個数を数える | [第07回](../sessions/07-theme-assignment.md) |
| `max(i in S)( 式 )` / `min(...)` | 最大・最小 | [第07回](../sessions/07-theme-assignment.md) |
| `forall(i in S where 条件)( ... )` | 繰り返しを条件で絞る | [第07回](../sessions/07-theme-assignment.md) |
| `enum SHIFTS = { day, night, off };` | 値に名前を付ける | [第08回](../sessions/08-roster-hard.md) |
| `bool2int(条件)` | 条件が成り立てば 1、そうでなければ 0 | [第07回](../sessions/07-theme-assignment.md) |
| `x[i] != x[i + 1]` | 隣り合う要素の参照 | [第08回](../sessions/08-roster-hard.md) |
| `if 条件 then A else B endif` | 場合分け（式） | [第09回](../sessions/09-roster-soft.md) |

## モデルの骨格

MiniZinc のモデルは「パラメータ → 決定変数 → 制約 → 解き方の指定 → 出力」の順に書く。
この順で書かなければならない決まりはないが、読む人のためにこの順で並べる。

```{.minizinc filename="骨格"}
include "globals.mzn";                       % 大域制約を使うとき

int: n = 4;                                  % パラメータ
set of int: ROWS = 1..n;
set of int: COLS = 1..n;

array[ROWS, COLS] of var 1..n: x;            % 決定変数と定義域

constraint forall(r in ROWS)(                % 制約
  all_different([ x[r, c] | c in COLS ])
);

solve satisfy;                               % 解き方の指定

output [ show(x[r, c]) ++ " " | r in ROWS, c in COLS ];   % 出力
```

## パラメータと決定変数

`var` が付くかどうかだけで区別する。

```{.minizinc filename="var の有無"}
int: n = 4;              % パラメータ。値はもう決まっている
var 1..4: y;             % 決定変数。1〜4 のどれかだが、まだ決まっていない
var bool: b;             % 真偽の決定変数
```

決定変数の宣言に書いた `1..4` が**定義域**である。
定義域を書いておけば「5 は入らない」という制約を別に書かなくてよい。

## 配列

```{.minizinc filename="配列"}
array[1..3] of var 1..9: a;              % 1次元
array[ROWS, COLS] of var 1..4: x;        % 2次元。x[r, c] で指す
array[1..3] of int: cap = [2, 3, 2];     % パラメータの配列
```

添字集合に名前を付けておくと（`set of int: ROWS = 1..n;`）、
規模を変えるときに1か所だけ直せばよくなる。

## 条件をつなぐ記号

条件どうしをつなぐ記号は4つある。**記号の形が独特なので、ここで確かめる。**

| 書き方 | 読み | 真になるとき |
|---|---|---|
| `A /\ B` | A **かつ** B | 両方が成り立つとき |
| `A \/ B` | A **または** B | 少なくとも一方が成り立つとき（両方成り立つときも真） |
| `not A` | A **でない** | A が成り立たないとき |
| `A -> B` | A **ならば** B | A が成り立つのに B が成り立たない、という場合以外 |

```{.minizinc filename="条件をつなぐ"}
constraint x = 1 /\ y = 2;              % x が 1 で、かつ y が 2
constraint x = 1 \/ x = 4;              % x が 1 か 4 のどちらか
constraint given[r, c] != 0 -> x[r, c] = given[r, c];   % 0 でないマスだけ固定する
```

`/\` は「かつ」を表す記号で、**割り算ではない**。`\/` が「または」である。
文字の向きが逆になるので、書くときに確かめる。

::: note
`constraint` を2行に分けて書けば、`/\` を使わなくても「かつ」になる。
制約を並べて書くこと自体が「かつ」だからである。
`/\` が要るのは、`->` の中や `if ... then ... endif` の中など、
**1つの式の内側で条件をつなぐ**ときである。
:::

道具ごとの記号の対応（Prolog・MiniZinc・Z3Py）は
[用語集](glossary.md)の「道具ごとの記法対応」にまとめてある。

## 繰り返しの2つの道具

```{.minizinc filename="forall と配列内包表記"}
forall(r in ROWS)( 条件 )          % すべての r について条件が成り立つ（制約になる）
[ x[r, c] | c in COLS ]            % c を動かして作った配列（値の並びになる）
```

`forall` は**条件**を作り、配列内包表記は**配列**を作る。
`all_different` のように配列を受け取る制約に渡すときは、後者で並べる。

`forall` には相棒がいる。`exists` は「1つでもあればよい」を表す。

```{.minizinc filename="forall と exists"}
forall(r in ROWS)( 条件 )          % すべての r について成り立つ（∀）
exists(r in ROWS)( 条件 )          % 成り立つ r が少なくとも1つある（∃）
```

「見つかった解とは違う盤面」のように、**否定を含む条件**を書くときに使う
（第04回）。

```{.minizinc filename="2つを組み合わせる"}
constraint forall(r in ROWS)(
  all_different([ x[r, c] | c in COLS ])
);
```

2つの添字を同時に動かすこともできる。

```{.minizinc filename="二重の繰り返し"}
constraint forall(r in ROWS, c in COLS)( x[r, c] != 0 );
```

条件を付けて絞ることもできる（`where`）。

```{.minizinc filename="条件付きの繰り返し"}
constraint forall(i in 1..n, j in 1..n where i < j)( a[i] != a[j] );
```

## 大域制約

よく使う条件にまとめて名前が付いているものを**大域制約**という。
使うときは先頭で `include "globals.mzn";` を書く。

| 大域制約 | 意味 |
|---|---|
| `all_different(配列)` | 配列の要素が互いに異なる |

::: note
この科目で使う大域制約は `all_different` だけである。
他にも多数あるので、自由課題で必要になったら
[公式ドキュメント](https://docs.minizinc.dev/)の一覧を見る。
:::

## モデルとデータを分ける

モデル（`.mzn`）側では**値を書かずに宣言**する。

```{.minizinc filename="sudoku.mzn（抜粋）"}
int: n;                                  % 値は .dzn から受け取る
array[1..n, 1..n] of int: given;
```

データ（`.dzn`）側で値を与える。2次元データは2通りの書き方がある。

```{.dzn filename="puzzle01.dzn"}
n = 4;

% 書き方1: | で行を区切る
given = [| 1, 0, 3, 0
         | 0, 0, 0, 2
         | 2, 0, 0, 0
         | 0, 3, 0, 1 |];
```

```{.dzn filename="puzzle02.dzn"}
n = 4;

% 書き方2: 1次元の並びを array2d で畳む
given = array2d(1..4, 1..4, [ 1, 0, 3, 0,
                              0, 0, 0, 2,
                              2, 0, 0, 0,
                              0, 3, 0, 1 ]);
```

::: warning
モデル側に `int: n = 4;` と**値まで書いてしまうと**、`.dzn` から上書きできない。
データで差し替えたいパラメータは `int: n;` と宣言だけにする。
:::

## 最適化

`solve satisfy;` を `minimize` / `maximize` に替えると、
制約を満たすもののうち目的の値が最も良いものを探す。

```{.minizinc filename="最適化"}
solve maximize sum(s in STUDENTS)( score[s, assign[s]] );
solve minimize total_penalty;
```

目的の式は決定変数を含んでよい。**添字に決定変数を使う**書き方も許される。

```{.minizinc filename="決定変数を添字に使う"}
array[STUDENTS] of var THEMES: assign;          % 誰にどのテーマを割り当てるか
array[STUDENTS, THEMES] of int: score;          % 希望の点数（パラメータ）

var int: total = sum(s in STUDENTS)( score[s, assign[s]] );
```

## 集計と数え上げ

```{.minizinc filename="集計"}
sum(d in DAYS)( bool2int(roster[s, d] = night) )   % 条件を満たす個数
sum(i in S)( cost[i] )                             % 値の合計
max(s in STAFF)( nights[s] )                       % 最大
min(s in STAFF)( nights[s] )                       % 最小
```

`bool2int(条件)` は、条件が成り立てば 1、成り立たなければ 0 になる。
**「何個あるか」を数えるときの基本の道具**である。

同じことは `count` でも書ける。**どちらも使う。**

```{.minizinc filename="count"}
count([ roster[s, d] | d in DAYS ], night)          % s の行に night がいくつあるか
count(i in S)( cost[i] > 0 )                       % 条件を満たす i の個数
count([ roster[s, d] | s in STAFF where leader[s] ], night)   % 資格者だけを数える
```

内包表記に `where` を足すと、数える相手を絞れる。

::: note
`count(配列, 値)` が数えられるのは「**ちょうどこの値**」だけである。
「この値**ではない**」を数えたいときは `sum` + `bool2int` を使う。

```{.minizinc filename="この値ではない、を数える"}
sum(d in DAYS)( bool2int(roster[s, d] != off) )     % 休みでない日の数
```
:::

::: note
`count` は「数える」という意図がそのまま名前になっている分、読みやすい。
一方 `sum` + `bool2int` は、数えた値をそのまま重み付き和へ入れられるので、
ソフト制約のペナルティ（[第09回](../sessions/09-roster-soft.md)）と同じ形で書ける。
**[第07回](../sessions/07-theme-assignment.md)で書くのは `count` だけ**で、
`sum` + `bool2int` を自分で書くのは[第09回](../sessions/09-roster-soft.md)からである。
1つのモデルの中では**どちらかに揃える**。
:::

## `enum` で値に名前を付ける

数字で表すより読みやすく、書き間違いをソルバーが見つけてくれる。

```{.minizinc filename="enum"}
enum SHIFTS = { day, night, off };
enum STAFF  = { a1, a2, a3, a4 };

set of int: DAYS = 1..7;

array[STAFF, DAYS] of var SHIFTS: roster;

constraint forall(s in STAFF, d in 1..6)(
  roster[s, d] = night -> roster[s, d + 1] = off
);
```

`->` は「ならば」（含意）である。
`roster[s, d + 1]` のように**隣の添字を参照する**ときは、
範囲をはみ出さないように `d in 1..6` と刻む。

## 場合分けとペナルティ

```{.minizinc filename="場合分け"}
% 各職員の夜勤数を数える
array[STAFF] of var 0..7: nights;
constraint forall(s in STAFF)(
  nights[s] = sum(d in DAYS)( bool2int(roster[s, d] = night) )
);

% 3 回を超えた分だけをペナルティとして数える
var int: penalty = sum(s in STAFF)(
  if nights[s] > 3 then nights[s] - 3 else 0 endif
);
```

`if ... then ... else ... endif` は**式**である。`endif` を忘れない。

## 出力

```{.minizinc filename="output"}
output [ "seat = ", show(seat), "\n" ];

output [ show(x[r, c]) ++ " " ++ (if c = n then "\n" else "" endif)
       | r in ROWS, c in COLS ];
```

`show(式)` は値を文字列にする。`++` は文字列の連結である。
**`output` は見せ方を整えるだけで、解の中身には関係しない。**

::: note
[第09回](../sessions/09-roster-soft.md)の配布モデルは、
人が読む表のほかに `#size` `#shift` `#value` で始まる行を出す。
[第10回](../sessions/10-roster-verification.md)の Python 検証器がこの行を読むためである。
**`output` は見せ方だけの話ではなく、別のプログラムとの受け渡し口にもなる。**
:::

## 関連ページ

- [MiniZinc 実行環境の使い方](setup-minizinc.md) — Playground の操作と出力の区切り記号
- [よくあるエラーと対処](errors.md) — 型エラー・未定義識別子・UNSATISFIABLE の読み方
- [定式化の7手順](modeling-steps.md) — 問題を変数・定義域・制約・目的へ分解する順序
- [グラフ彩色の3つの表現](graph-coloring.md) — 同じ問題を Prolog・MiniZinc・Z3 で書き比べる
- [用語集](glossary.md) — パラメータ・決定変数・大域制約などの定義
