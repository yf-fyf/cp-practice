---
description: 参考資料の索引。最初に読む環境構築3本と、必要なときに引く早見表・概説・用語集への入口
---

# 参考資料

参考資料は2種類ある。**最初に読むもの**（環境構築）と、
**必要なときに引くもの**（早見表・概説・用語集）である。

## 最初に読むもの: 環境構築

使う道具は3つで、そのうち導入が要るのは Z3 だけである。

| ページ | いつ使うか | 導入 |
|---|---|---|
| [Prolog 実行環境の使い方](setup-prolog.md) | 第01〜02回 | 不要（ブラウザ） |
| [MiniZinc 実行環境の使い方](setup-minizinc.md) | 第03〜04回、第07〜10回 | 不要（ブラウザ） |
| [Z3 実行環境の使い方](setup-z3.md) | 第05〜06回 | **必要**（Python + z3-solver） |

::: important
**第05回に入る前に、[Z3 実行環境の使い方](setup-z3.md)の「最小動作確認」まで
到達しておくこと。**授業時間内での導入は想定していない。

同じ時期に読むとよい番外の自習ページとして[論理の入門(1) 読み方](logic-intro.md)がある。
必須の到達点ではないが、**第05回より前に上から一括で読む**使い方を想定している。
続編の[論理の入門(2) 述語論理の意味論](logic-semantics.md)は一括読みの対象ではない。
**もっと深く知りたくなったときに読む**ページである。
:::

## 必要なときに引くもの

### 書き方を忘れたとき

| ページ | 内容 |
|---|---|
| [Prolog 早見表](prolog-cheatsheet.md) | 事実・規則・クエリ・リスト・`member`・`permutation`・`\=` |
| [MiniZinc 早見表](minizinc-cheatsheet.md) | パラメータ・決定変数・配列・`forall`・`all_different`・最適化・`enum`・集計 |
| [Z3Py 早見表](z3py-cheatsheet.md) | `Bool`・`Int`・論理演算・`Solver` の操作・解の読み方 |

早見表には**この科目で実際に使う書き方だけ**が載っている。
それ以外を知りたいときは、各ページの末尾から公式ドキュメントへ進む。

### 問題の解きかたに詰まったとき

| ページ | 内容 |
|---|---|
| [定式化の7手順](modeling-steps.md) | 問題を入力・変数・定義域・制約・目的・検証へ分解する順序と、書き出し用のひな形 |
| [グラフ彩色の3つの表現](graph-coloring.md) | 同じ問題を Prolog・MiniZinc・Z3 で書き比べた比較リファレンス |
| [SAT・SMT 概説](logic-sat-smt.md) | 真理値表・CNF・代表的な Boolean 符号化・SAT と SMT の処理イメージ・型の選び方 |
| [論理の入門(1) 読み方](logic-intro.md) | 番外の自習ページ。述語と引数・変数・「すべて」と「ある」が、規則・`forall`・`Implies` のどこに現れるか |
| [論理の入門(2) 述語論理の意味論](logic-semantics.md) | 番外の自習ページ。構造・付値・充足関係・モデルの定義と、ソルバーが探しているものの正体 |

### エラーが出たとき・言葉が分からないとき

| ページ | 内容 |
|---|---|
| [よくあるエラーと対処](errors.md) | Prolog・MiniZinc・Z3 の代表的なエラーと、解が出ないときの切り分け |
| [用語集](glossary.md) | 第01〜10回で導入する用語の意味と初出回 |

## 知りたいことから引く

| 知りたいこと | 行き先 |
|---|---|
| Prolog をどう動かすか | [Prolog 実行環境の使い方](setup-prolog.md) |
| MiniZinc をどう動かすか | [MiniZinc 実行環境の使い方](setup-minizinc.md) |
| Z3 が入らない・動かない | [Z3 実行環境の使い方](setup-z3.md) |
| `member` を使うのに何を書くのか | [Prolog 早見表](prolog-cheatsheet.md) |
| `forall` と配列内包表記の違い | [MiniZinc 早見表](minizinc-cheatsheet.md) |
| `check()` の結果をどう判定するか | [Z3Py 早見表](z3py-cheatsheet.md) |
| 含意（ならば）の真理値表 | [SAT・SMT 概説](logic-sat-smt.md) |
| 「ちょうど一つ」の書き方 | [SAT・SMT 概説](logic-sat-smt.md) |
| `Bool` と `Int` のどちらを使うか | [SAT・SMT 概説](logic-sat-smt.md) |
| 何から手を付けたらよいか分からない | [定式化の7手順](modeling-steps.md) |
| ハード制約とソフト制約の分け方 | [定式化の7手順](modeling-steps.md) |
| 解が出ない・UNSAT になる | [よくあるエラーと対処](errors.md) |
| いつまでも終わらない | [よくあるエラーと対処](errors.md) |
| 同じ問題を別の道具で書くとどうなるか | [グラフ彩色の3つの表現](graph-coloring.md) |
| Prolog の規則の変数は何を指しているのか | [論理の入門(1)](logic-intro.md#prolog-rules) |
| 「すべて」と「ある」の違い・`forall` と量化子 | [論理の入門(1)](logic-intro.md#quantifiers) |
| 「すべての〜について、ある〜が」の順序で意味が変わる理由 | [論理の入門(1)](logic-intro.md#nested-quantifiers) |
| 論理式が「真である」とはどういうことか | [論理の入門(2)](logic-semantics.md#satisfaction) |
| ソルバーが探している「解」は論理では何にあたるか | [論理の入門(2)](logic-semantics.md#solvers) |
| 用語の意味と、それを習った回 | [用語集](glossary.md) |

## 自由課題を進めるとき

進め方・成果物・テンプレートは [自由課題の案内](../projects/README.md)にある。
この参考資料のうち第11〜14回で使うのは、主に次の3本である。

1. [定式化の7手順](modeling-steps.md) — 企画書の中身はこの7項目で書く
2. [グラフ彩色の3つの表現](graph-coloring.md) — 表現を選ぶときの比較材料
3. [MiniZinc 実行環境の使い方](setup-minizinc.md) / [Z3 実行環境の使い方](setup-z3.md) — 使った版を成果物に書く

## この資料の直し方

内容がおかしい、書いていないことで詰まった、という箇所を見つけたら教えてほしい。
参考資料は授業中にも直す。

用語を足すときの手順は
[用語初出台帳](../../design/glossary-ledger.md)にある。
