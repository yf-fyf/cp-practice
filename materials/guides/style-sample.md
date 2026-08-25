---
description: 教材ページで使える表示部品を1ページに並べた見本。原稿を書くときの参照用
---

# 表示見本

このページは、教材原稿で使える表示部品を一覧にしたものである。
学習内容は含まない。**原稿を書く人が、書き方と見え方を突き合わせるため**に置いてある。

原稿の書き方の規約は [保守手順](../../design/maintaining.md) に、
各回の標準構成は同じ文書の「教材追加の手順」にある。

## この回の目標

`## この回の目標` という H2 は、`site/boxes.lua` が自動で枠に入れる。
検出する語は1か所（`boxes.lua` の `GOAL_HEADING`）で定義してあり、
`tools/check_docs.py` の `structure` 検査が各回にこの見出しがあることを確かめる。

- 目標は観察可能な行動で書く（「理解する」で終わらせない）
- 3〜4項目に収める

## 注釈のボックス

```markdown
::: {.note}
本筋ではないが理解を助ける情報。
:::
```

::: {.note}
**補足**。本筋ではないが理解を助ける情報を置く。
読み飛ばしても先へ進めるものだけをここに入れる。
:::

::: {.important}
**重要**。後の演習で必要になる要点を置く。
「あとで使う」ことが分かるように書く。
:::

::: {.warning}
**注意**。誤操作や誤解が起きやすい箇所を置く。
「こうすると壊れる」「これは別物である」といった内容。
:::

::: {.term}
**用語**。初出の専門用語をここで定義する。
用語集ができたら、ここから用語集の該当項目へリンクする。
:::

## 学習活動のボックス

::: {.predict}
**予想**。実行する前に結果を考えてもらう問い。
選択肢を並べて「どれになると思うか」を書き出させる形が使いやすい。
:::

::: {.check}
**チェックポイント**。途中段階の完了条件。

- ここまでで何が動いているはずか
- 動いていないならどこを見るか
:::

::: {.discuss}
**考察**。結果の理由を説明してもらう問い。
答えを本文に書かず、次の節や次回で回収する。
:::

::: {.done}
**完了チェック**。回末に置くチェックリスト。

- [ ] チェックボックスは pandoc のタスクリスト記法で書く
- [ ] 状態は保存しない（静的な表示のみ）
- [ ] 「〜を確認した」「〜を説明できる」の形で書く
:::

## 演習の3段階

演習は `::: {.exercise level=...}` で書く。`level` は `required` / `standard` / `advanced` の
3つで、見出し語（必須演習・標準演習・発展演習）と左罫の色が変わる。
**色が見えなくても見出し語で段階が分かる**ようにしてある。

```markdown
::: {.exercise level=required}
### 見出し

本文。完了条件をはっきり書く。
:::
```

::: {.exercise level=required}
### 必須演習の見本

次回の内容に必要な課題。授業後の自習を含めて必ず終える。
段階的ヒントを付け、最終段に解答を置いてよい。

**完了条件**: ここに「何ができたら終わりか」を観察可能な形で書く。
:::

::: {.exercise level=standard}
### 標準演習の見本

その回の中心となる課題。100分の授業と必要な自習で終えるのを目指す。
ヒントは置くが、**中心部分の完成コードは公開しない**
（非公開リポジトリの `teacher/answers/` に置く）。
:::

::: {.exercise level=advanced}
### 発展演習の見本

先へ進みたい学習者向け。方向づけだけを書き、**完成コードは公開しない**。
作業量を増やすのではなく、問題規模・制約・目的関数・検証方法のいずれかを発展させる。
:::

## 段階的ヒント

`::: {.hint summary="..."}` は `<details>` になる。
JavaScript を使わずに開閉できるので、JS が無い環境でも読める。
閉じている間は中身が本文に出ないので、答えを先に見てしまうことがない。

```markdown
::: {.hint summary="ヒント1: 見出し"}
本文。コードブロックも入れられる。
:::
```

::: {.hint summary="ヒント1: まず定義域を書き出す"}
各マスが取り得る値は 1..4 である。制約を書く前に、この範囲だけを宣言してみる。
:::

::: {.hint summary="ヒント2: 解答"}
```{.minizinc}
constraint forall(c in COLS)( all_different([ x[r, c] | r in ROWS ]) );
```
:::

## コードと実行結果

区分が見分けられるように、フェンスの綴りを次で統一する。
ファイル名を出したいときは `filename=` を付ける。

| 区分 | フェンスの綴り | 表示 |
|---|---|---|
| MiniZinc モデル | `` ```{.minizinc filename="sudoku4.mzn"} `` | ファイル名キャプション付き |
| MiniZinc データ | `` ```{.dzn filename="puzzle01.dzn"} `` | 同上 |
| Prolog | `` ```{.prolog filename="grid.pl"} `` | 構文着色あり |
| Z3Py | `` ```{.z3py filename="deps.py"} `` | Python として着色 |
| 実行コマンド | `` ```console `` | プロンプト付きで書く |
| ソルバーの解・統計 | `` ```solver `` | 着色なし・ラベル「ソルバー出力」 |
| エラー出力 | `` ```{.text .error} `` | 着色なし・警告色の左罫 |

MiniZinc は pandoc の構文定義に無いので着色されない。右上のラベルで区分を示す。

```{.minizinc filename="sudoku4.mzn（抜粋）"}
include "globals.mzn";

int: n = 4;
array[1..n, 1..n] of var 1..n: x;

constraint forall(r in 1..n)( all_different([ x[r, c] | c in 1..n ]) );

solve satisfy;
```

```{.dzn filename="puzzle01.dzn"}
n = 4;
b = 2;

given = [| 1, 0, 3, 0
         | 0, 0, 0, 2
         | 2, 0, 0, 0
         | 0, 3, 0, 1 |];
```

```{.prolog filename="coloring.pl"}
% 隣接する地区は違う色に塗る（第02回の書き方）
color(red). color(green). color(blue).

different(X, Y) :- color(X), color(Y), X \= Y.

paint(A, B, C) :-
    different(A, B),
    different(A, C),
    different(B, C).
```

```{.python filename="check_sudoku.py（抜粋）"}
def problems(board: list[list[int]], n: int) -> list[str]:
    values = set(range(1, n + 1))
    found = []
    for r in range(n):
        if set(board[r]) != values:
            found.append(f"{r + 1} 行目に重複か範囲外がある: {board[r]}")
    return found
```

実行コマンドと期待出力は**別のブロックに分ける**。同じブロックに混ぜない。

```console
$ python3 check_sudoku.py board.txt
```

```solver
1 2 3 4
3 4 1 2
2 1 4 3
4 3 2 1
----------
```

```{.text .error}
MiniZinc: type error: undefined identifier `all_different'
```

## 数式

数式は MathML で出力する。命題論理・量化子・集合・制約式・目的関数を書ける。

インライン数式は、変数 $x_{r,c}$ や $\neg p \lor q$ のように本文に混ぜて書く。

独立した数式はブロックで書く。長い制約式は狭い画面で横スクロールする。

$$\forall r \in \mathrm{ROWS}: \quad \operatorname{alldifferent}\bigl(\{\, x_{r,c} \mid c \in \mathrm{COLS} \,\}\bigr)$$

$$\text{最小化}\quad \sum_{i=1}^{n} \sum_{j=1}^{m} w_{ij} \, y_{ij}
\quad \text{ただし} \quad \sum_{j=1}^{m} y_{ij} = 1 \;\; (i = 1, \dots, n)$$

命題論理の記号も同じように書ける: $(p \to q) \land (\neg q \to \neg p)$

## 図

図は `materials/figures/*.tex`（TikZ）を正本とし、`make figures` で SVG を生成する。
生成した SVG はコミットする。**代替テキストは必須**である。
図をクリックすると拡大表示になる（`site/lightbox.js`）。

```markdown
![代替テキスト。図が見えない読者にも内容が伝わるように書く。](figures/graph-5districts.svg)
```

![架空の5地区（北区・南区・東区・西区・中央区）の隣接関係と、3色で塗り分けた解の一例。中央区は他の4地区すべてと隣り合い、外側は北・東・南・西の順に環になっていて、辺は全部で8本ある。左は問題で、辺で結ばれた2地区が隣り合っていることを表す。右は解の一例で、どの辺の両端も異なる色になっている。](figures/graph-5districts.svg)

## 表

表は自動的に横スクロールする容器に入るので、列が多くても本文が押し出されない。

| 回 | 中心題材 | 主な学習内容 | 実行環境 | 演習ファイル | 縦断題材 |
|---|---|---|---|---|---|
| 01 | 小型論理グリッド | Prolog の事実・規則・変数・クエリ | Prolog | `grid.pl` | — |
| 02 | 論理グリッドの探索 | 単一化・リスト・候補生成・バックトラック | Prolog | `grid2.pl` | グラフ彩色（Prolog 版） |
| 03 | 数独: 求解 | CSP の基本語彙・変数・定義域・配列・大域制約 | MiniZinc | `sudoku4.mzn` | グラフ彩色（MiniZinc 版） |
| 04 | 数独: 検証 | 9×9 盤面・モデルとデータの分離・複数解・一意性 | MiniZinc | `sudoku9.mzn` / `*.dzn` | — |
| 05 | パッケージ依存関係 | SAT/UNSAT・CNF の位置付け・Boolean 符号化 | Python+Z3 | `deps.py` | グラフ彩色（SAT 符号化） |

## リンク

原稿の中では、**サイト内のページは `.md` への相対パスで書く**。
`site/boxes.lua` がサイト内 URL へ書き換えるので、GitHub 上で原稿を読んでも
サイト上で読んでもリンクが切れない。サイトに載せていない `.md` は
GitHub の該当ファイルへ自動で逃げる。

```markdown
[演習ファイルの使い方](../../workbook/README.md)     ← サイト内 URL に変換される
[MiniZinc Playground](https://play.minizinc.dev/)    ← 外部リンクはそのまま
```

- サイト内: [第03回 数独: MiniZincで盤面を解く](../sessions/03-minizinc-sudoku.md)
- サイト内: [演習ファイルの使い方](../../workbook/README.md)
- サイト外に置いた原稿: [カリキュラム設計書](../../design/curriculum-2026.md)
- 外部: [MiniZinc Playground](https://play.minizinc.dev/)
- 外部: [MiniZinc 公式ドキュメント](https://docs.minizinc.dev/)

外部リンクは CI では検査しない。切れていないかは定期的に手で確かめる。

## 表記の統一

`tools/check_docs.py` の `style` 検査が次を見る。

| 対象 | 正 | 誤（避ける） |
|---|---|---|
| 回の呼称 | `第03回`（2桁ゼロ埋め） | `第3回`・`3回目` |
| 学ぶ人の呼称 | `学習者` | `受講者`・`学生` |
| 派生する数値 | 書かない（「対応する演習ファイルで確認できる」等に言い換える） | `演習ファイルは全12本` |

例外は `tools/doc_check_allowlist.yaml` に理由つきで書く。
一度も一致しなかった除外は「死んだ除外」として検査自身が違反にする。
