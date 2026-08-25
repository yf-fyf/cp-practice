---
description: 第01〜10回で導入する用語の一覧。それぞれの意味と初出回への案内をまとめた、この科目の用語集
---

# 用語集

この科目で使う用語を、**初出の回の順**に並べてある。
一覧と初出回の正本は [用語初出台帳](../../design/glossary-ledger.md)である。

::: note
用語の並びは五十音順ではなく**導入した順**である。
探すときはブラウザのページ内検索（`Ctrl` + `F` / `Cmd` + `F`）を使う。
:::

| 回 | 導入する用語 |
|---|---|
| 第01回 | [宣言的な記述](#declarative_description)・[知識ベース](#knowledge_base)・[事実](#fact)・[クエリ](#query)・[述語](#predicate)・[アトム](#atom)・[変数（Prolog）](#prolog_variable)・[規則](#rule)・[連言](#conjunction) |
| 第02回 | [リスト](#list)・[member](#member)・[生成とテスト](#generate_and_test)・[バックトラック](#backtracking)・[単一化](#unification)・[非等号](#disequality)・[複数解](#multiple_solutions)・[グラフ](#graph)・[彩色問題](#graph_coloring)・[探索空間](#search_space) |
| 第03回 | [制約プログラミング](#constraint_programming)・[CSP の基本語彙](#csp_vocabulary)・[パラメータと決定変数](#parameter_vs_decision_var)・[MiniZinc モデルの構造](#minizinc_model_structure)・[2次元配列と添字集合](#array_2d)・[forall と配列内包表記](#forall_comprehension)・[大域制約と all_different](#all_different) |
| 第04回 | [モデルとデータの分離](#model_data_separation)・[データファイル](#dzn_data)・[複数解の列挙](#multiple_solution_enumeration)・[解の一意性](#solution_uniqueness)・[既知例による検証](#known_example_validation) |
| 第05回 | [命題変数](#propositional_variable)・[論理演算](#logical_connectives)・[真理値表](#truth_table)・[充足可能性](#satisfiability)・[UNSAT](#unsat)・[CNF](#cnf)・[Boolean 符号化](#boolean_encoding)・[ちょうど一つ](#exactly_one)・[Z3Py の基本操作](#z3py_basics) |
| 第06回 | [SMT](#smt)・[背景理論](#background_theory)・[整数変数](#integer_variable)・[バージョン範囲](#version_range)・[unknown](#unknown_result)・[符号化の選択](#encoding_choice) |
| 第07回 | [最適化](#optimization)・[目的関数](#objective_function)・[ハード制約](#hard_constraint)・[実行可能解](#feasible_solution)・[最適解](#optimal_solution)・[合計の目的と最大の目的](#total_vs_max_objective)・[定員制約](#capacity_constraint)・[集計](#aggregation_sum_count) |
| 第08回 | [列挙型](#enum_type)・[シフトの表現](#shift_representation)・[必要人数制約](#coverage_constraint)・[資格制約](#qualification_constraint)・[休息制約](#rest_constraint)・[隣接する添字](#adjacent_index)・[表現が保証する性質](#representation_guarantees) |
| 第09回 | [ソフト制約](#soft_constraint)・[違反ペナルティ](#penalty)・[重み付き和](#weighted_sum)・[公平性の数値化](#fairness_metric)・[正規化](#normalization)・[辞書式最適化](#lexicographic_optimization) |
| 第10回 | [独立した検証](#independent_verification)・[正常例と反例](#positive_and_negative_cases)・[段階的テスト](#incremental_testing)・[機械可読な出力](#machine_readable_output)・[ソルバー統計](#solver_statistics)・[正しさと速さの分離](#correctness_vs_speed) |

---

## 道具ごとの記法対応

この科目では3つの道具を使う。**言いたいことは同じでも、書き方は道具ごとに違う。**
迷ったらこの表に戻る。

| 言いたいこと | Prolog（第01〜02回） | MiniZinc（第03〜04・07〜10回） | Z3Py（第05〜06回） | 数学の記号 |
|---|---|---|---|---|
| かつ | `,`（条件を並べる） | `/\`（`constraint` を並べても同じ） | `And(p, q)` | $p \land q$ |
| または | （この科目では使わない） | `\/` | `Or(p, q)` | $p \lor q$ |
| でない | （`\=` の形でだけ使う） | `not A` | `Not(p)` | $\neg p$ |
| ならば | `頭部 :- 条件`（**右から左**に読む） | `A -> B` | `Implies(p, q)` | $p \to q$ |
| 等しくない | `X \= Y` | `x != y` | `x != y` | $x \neq y$ |
| 相異なり（全部違う） | `permutation` で候補を作る | `all_different(配列)` | 2つずつ `!=` を並べる | — |
| 解が1つ見つかった | 変数の値が表示される | `----------` | `sat` | — |
| 解なし | `false.` | `=====UNSATISFIABLE=====` | `unsat` | — |
| 次の解を見る | 「次の解」を押す | 見つけた解を制約で除外して解き直す（第04回） | 同左 | — |

::: note
**「ならば」の向きだけは、道具によって書く順序が逆になる。**
Prolog の `teammate(X, Y) :- club(X, C), club(Y, C).` は
「`club(...)` が成り立つ**ならば** `teammate(X, Y)`」であり、
**結論を先に書く**。MiniZinc の `A -> B` と Z3Py の `Implies(p, q)` は
条件を先に書く。読む向きが逆になるので、Prolog から MiniZinc へ移るときに確かめる。
:::

::: note
**「1つのものに1つの値」を誰が保証するかも道具で変わる。**
Prolog の変数と MiniZinc の決定変数は値を1つしか取れないので自動で保証される。
Z3 の真偽変数で表すときだけ、[ちょうど一つ](#exactly_one)を自分で書く必要がある。
同じ問題を3通りで書き比べた例が
[グラフ彩色の3つの表現](graph-coloring.md)にある。
:::

::: note
この表が並べているのは**「かつ・または・でない・ならば」の段**である。
その上の段にあたる「すべての〜について」「ある〜が存在して」の道具別対応は、
番外の自習ページ[論理の入門(1)](logic-intro.md#tool-table)にある。
:::

書き方の詳しい一覧は各道具の早見表にある
（[Prolog](prolog-cheatsheet.md) / [MiniZinc](minizinc-cheatsheet.md) / [Z3Py](z3py-cheatsheet.md)）。

---

## 第01回の用語

### 宣言的な記述 {#declarative_description}

初出: [第01回](../sessions/01-prolog-intro.md)。
解を求める**手順**ではなく、成り立っている**関係**を書く書き方である。
「どう探すか」は処理系やソルバーに任せる。
手続き的な記述（Python のように手順を並べる書き方）と対になる。

### 知識ベース {#knowledge_base}

初出: [第01回](../sessions/01-prolog-intro.md)。
事実と規則を集めたもの。Prolog のプログラムは知識ベースそのものであり、
実行とはこれに問い合わせることである。

### 事実 {#fact}

初出: [第01回](../sessions/01-prolog-intro.md)。
無条件に成り立つと宣言した1行。`drinks(aoi, cocoa).` のように書き、
ピリオドで終わる。

### クエリ {#query}

初出: [第01回](../sessions/01-prolog-intro.md)。
知識ベースへの問い合わせ。成り立てば `true.` か変数の値が返り、
成り立たなければ `false.` が返る。

### 述語 {#predicate}

初出: [第01回](../sessions/01-prolog-intro.md)。
関係の名前と引数の個数の組。`drinks/2` のように「名前/引数の個数」で書く。
名前が同じでも引数の個数が違えば別の述語である。

### アトム {#atom}

初出: [第01回](../sessions/01-prolog-intro.md)。
小文字で始まる、それ自身を表す名前。`aoi` `cocoa` `brass_band` など。
記号や日本語を含めたいときは `'コーヒー'` のように引用符で囲む。

### 変数（Prolog） {#prolog_variable}

初出: [第01回](../sessions/01-prolog-intro.md)。
大文字か `_` で始まる、値がまだ決まっていない名前。
`_` 1文字は無名変数で、「何でもよい」を表す。
[CSP の変数](#csp_vocabulary)とは別の概念である。

### 規則 {#rule}

初出: [第01回](../sessions/01-prolog-intro.md)。
「条件が成り立てば頭部も成り立つ」と書いた**節**。
`teammate(X, Y) :- club(X, C), club(Y, C).` の形で書く。

Prolog では、事実も規則も**ピリオドで終わる1つのまとまり**を節と呼ぶ。
第05回に出てくる「[CNF](#cnf) の節」は**これとは別のもの**で、
名前が同じだけである（「または」で結んだ塊を指す）。

### 連言 {#conjunction}

初出: [第01回](../sessions/01-prolog-intro.md)。
「かつ」。規則の条件やクエリでカンマ `,` で並べたもの。
**並べた順に試される**ので、順序が探索の速さに効く。

---

## 第02回の用語

### 項 {#prolog_term}

初出: [第02回](../sessions/02-prolog-modeling.md)。
Prolog が扱う**値の単位**。[アトム](#atom)・数・[変数](#prolog_variable)と、
`p(aoi, D1, C1, T1)` のようにそれらを名前と括弧でまとめたものが項である。
まとめた項は「入れ物」として使え、[`member`](#member) の照合にそのまま渡せる。
引数の個数が違う項どうしは[単一化](#unification)しないので、
数を1つ間違えると条件が静かに `false.` になる。

### リスト {#list}

初出: [第02回](../sessions/02-prolog-modeling.md)。
値を順に並べたもの。`[coffee, tea, cocoa]` のように書く。

### member {#member}

初出: [第02回](../sessions/02-prolog-modeling.md)。
`member(X, リスト)` は、リストの要素を1つずつ `X` に入れて返す述語である。
候補の生成に使う。使う前に `:- use_module(library(lists)).` を書く。

### 生成とテスト {#generate_and_test}

初出: [第02回](../sessions/02-prolog-modeling.md)。
候補を作ってから条件で落とす2段構えの書き方。
候補の作り方と絞り込みの順序で、実行時間が大きく変わる。

### バックトラック {#backtracking}

初出: [第02回](../sessions/02-prolog-modeling.md)。
条件が満たせなかったとき、直前の選択まで戻って別の候補を試す動きである。
「次の解」を押したときにも同じことが起きる。

### 単一化 {#unification}

初出: [第02回](../sessions/02-prolog-modeling.md)。
両辺が同じ形になるように、変数へ値を結びつける操作。
`X = cocoa` は「代入」ではなく、両辺を等しくできるかを調べて
できるなら結びつける、という意味である。

### 非等号 {#disequality}

初出: [第02回](../sessions/02-prolog-modeling.md)。
`X \= Y` は「`X` と `Y` は等しくない」を表す。
手掛かりが「〜ではない」の形のときに使う。

### 複数解 {#multiple_solutions}

初出: [第02回](../sessions/02-prolog-modeling.md)。
条件を満たす答えが2つ以上あること。
実行ページでは「次の解」を押すたびに1つずつ出る。
全部を数え上げて一意性を判定するのは[第04回](#solution_uniqueness)である。

### グラフ {#graph}

初出: [第02回](../sessions/02-prolog-modeling.md)。
頂点と、頂点を結ぶ辺の集まり。地区と隣接関係、人と友人関係などを表す。

### 彩色問題 {#graph_coloring}

初出: [第02回](../sessions/02-prolog-modeling.md)。
辺で結ばれた2つの頂点が同じ色にならないように色を割り当てる問題。
この科目では第02回・第03回・第05回で表現を替えて再訪する
（[グラフ彩色の3つの表現](graph-coloring.md)）。

### 探索空間 {#search_space}

初出: [第02回](../sessions/02-prolog-modeling.md)。
試す可能性のある候補の全体。
属性が増えると掛け算で増えるので、絞り込みを早く入れるほど小さくなる。

第02回の論理グリッド（4人・3属性・各属性4値）で数えると、次のようになる。

| 候補の作り方 | 候補の数 |
|---|---|
| 1人ずつ独立に選ぶ（重なりを許す） | $4^{12}$（約1700万通り） |
| 属性ごとに4人への割り当て方を選ぶ（重ならない） | $(4!)^3 = 24^3 = 13824$ 通り |

**「同じ属性の値は重ならない」を候補の作り方に織り込むだけで、3桁小さくなる。**
`permutation` を使うと、この絞り込みが条件を1つも書かずに手に入る。

---

## 第03回の用語

### 制約プログラミング {#constraint_programming}

初出: [第03回](../sessions/03-minizinc-sudoku.md)。
解を求める手順ではなく、解が**満たすべき条件**を書き、
条件を満たすものを探す仕事はソルバーに任せる書き方である。

### 制約充足問題（CSP）の基本語彙 {#csp_vocabulary}

初出: [第03回](../sessions/03-minizinc-sudoku.md)。
この科目で最後まで使う6語である。

| 語 | 意味 |
|---|---|
| 変数 | ソルバーに値を決めてもらうもの |
| 定義域 | 各変数が取り得る値の範囲 |
| 制約 | 変数の値の組が満たさなければならない条件 |
| 割当て | すべての変数に値を1つずつ決めたもの |
| 解 | すべての制約を満たす割当て |
| 充足 | 制約をすべて満たしている状態 |

「解が1つでもあるか」を問う問題を**制約充足問題**（CSP）という。

### パラメータと決定変数 {#parameter_vs_decision_var}

初出: [第03回](../sessions/03-minizinc-sudoku.md)。
**パラメータ**はモデルを書く時点で値が決まっているもの、
**決定変数**はソルバーに決めてもらうものである。
MiniZinc では `var` が付くかどうかで区別する。

### MiniZinc モデルの構造 {#minizinc_model_structure}

初出: [第03回](../sessions/03-minizinc-sudoku.md)。
「宣言 → `constraint` → `solve` → `output`」の並びでできている。
`solve satisfy;` は「条件を満たす割当てを1つ見つけよ」という指示である。

### 2次元配列と添字集合 {#array_2d}

初出: [第03回](../sessions/03-minizinc-sudoku.md)。
行と列で位置が決まる変数の並びと、その添字の範囲。
`array[ROWS, COLS] of var 1..4: x;` の `ROWS`・`COLS` が添字集合である。

### forall と配列内包表記 {#forall_comprehension}

初出: [第03回](../sessions/03-minizinc-sudoku.md)。
`forall(r in ROWS)( 条件 )` は**条件**を作り、
`[ x[r, c] | c in COLS ]` は**配列**を作る。役割が違う。

### 大域制約と all_different {#all_different}

初出: [第03回](../sessions/03-minizinc-sudoku.md)。
よく使う条件にまとめて名前を付けたものを**大域制約**という。
`all_different(配列)` は「配列の要素が互いに異なる」を表す。
使うときは `include "globals.mzn";` を書く。

---

## 第04回の用語

### モデルとデータの分離 {#model_data_separation}

初出: [第04回](../sessions/04-sudoku-data-uniqueness.md)。
問題の**構造**（モデル）と、個々の**インスタンス**（データ）を別々に持つこと。
モデルを書き換えずに入力だけを差し替えられるようになる。

### データファイル {#dzn_data}

初出: [第04回](../sessions/04-sudoku-data-uniqueness.md)。
パラメータの値だけを書いた入力ファイル。MiniZinc では `.dzn` である。
モデル側は `int: n;` と宣言だけにしておく。

### 複数解の列挙 {#multiple_solution_enumeration}

初出: [第04回](../sessions/04-sudoku-data-uniqueness.md)。
1つ目の解で止めず、2つ目以降も出させること。

### 解の一意性 {#solution_uniqueness}

初出: [第04回](../sessions/04-sudoku-data-uniqueness.md)。
条件を満たす解がちょうど1つであること。
**2つ目の解があるかどうか**を見れば判定できる。全部を数える必要はない。

### 既知例による検証 {#known_example_validation}

初出: [第04回](../sessions/04-sudoku-data-uniqueness.md)。
答えが分かっている小さな例でモデルを走らせ、正しい答えが出るかを確かめること。

---

## 第05回の用語

### 命題変数 {#propositional_variable}

初出: [第05回](../sessions/05-sat-dependencies.md)。
真か偽のどちらかになる変数。
「このパッケージを導入する」のように、成り立つ・成り立たないが決まる文に対応させる。

### 論理演算 {#logical_connectives}

初出: [第05回](../sessions/05-sat-dependencies.md)。
否定 $\neg$・論理積 $\land$・論理和 $\lor$・含意 $\to$ の4つ。
Z3Py では `Not` / `And` / `Or` / `Implies` に対応する。
含意だけは論理回路に対応するものが無い（[SAT・SMT 概説](logic-sat-smt.md)）。

### 真理値表 {#truth_table}

初出: [第05回](../sessions/05-sat-dependencies.md)。
変数の値の組み合わせをすべて並べ、式の値を書き出した表である。
変数が $n$ 個なら $2^n$ 行になる。

### 充足可能性 {#satisfiability}

初出: [第05回](../sessions/05-sat-dependencies.md)。
すべての式を同時に真にする割り当てが存在すること。
存在すると分かった状態を **SAT** という。ソルバーは割り当ての例を返す。

### UNSAT {#unsat}

初出: [第05回](../sessions/05-sat-dependencies.md)。
どう値を選んでも同時には満たせないと分かった状態。
**答えの一種**であって、モデルが壊れているという意味ではない。

### CNF {#cnf}

初出: [第05回](../sessions/05-sat-dependencies.md)。
連言標準形。「または」で結んだ塊（**CNF の節**）を「かつ」で並べた形である。
SAT ソルバーが受け取る形式だが、Z3 を使うときに手で直す必要はない。
[Prolog の節](#rule)（ピリオドで終わる1行のまとまり）とは別のもので、名前が同じだけである。

### Boolean 符号化 {#boolean_encoding}

初出: [第05回](../sessions/05-sat-dependencies.md)。
選択肢を真偽変数の組で表すこと。
「地区 $d$ を色 $c$ で塗る」を1つの真偽変数にするのがその例である。

### ちょうど一つ {#exactly_one}

初出: [第05回](../sessions/05-sat-dependencies.md)。
選択肢のうち1つだけを選ぶ条件。
「少なくとも一つ」（$x_1 \lor \dots \lor x_n$）と
「高々一つ」（どの2つも同時に真でない）を並べて表す。

### Z3Py の基本操作 {#z3py_basics}

初出: [第05回](../sessions/05-sat-dependencies.md)。
変数を作り（`Bool`）、ソルバーに制約を足し（`add`）、
解けるかを調べ（`check`）、割り当てを読む（`model`）という一連の操作である。
判定は必ず `check() == sat` の形で書く（[Z3Py 早見表](z3py-cheatsheet.md)）。

---

## 第06回の用語

### SMT {#smt}

初出: [第06回](../sessions/06-smt-versions.md)。
命題論理の骨組みに**背景理論**を組み合わせた充足可能性のこと。
`v >= 2` のような式をそのまま書ける。

### 背景理論 {#background_theory}

初出: [第06回](../sessions/06-smt-versions.md)。
整数の大小、実数の四則のように、値の世界ごとの決まりごとを担当する部品である。

### 整数変数 {#integer_variable}

初出: [第06回](../sessions/06-smt-versions.md)。
大小の比較ができる値を取る決定変数。Z3Py では `Int` で作る。

### バージョン範囲 {#version_range}

初出: [第06回](../sessions/06-smt-versions.md)。
依存先が満たすべき版の区間。「2 以上 4 以下」のように上下限で表す。

### unknown {#unknown_result}

初出: [第06回](../sessions/06-smt-versions.md)。
解の有無を確かめきれなかったという結果。
`sat` でも `unsat` でもない第3の答えである。

### 符号化の選択 {#encoding_choice}

初出: [第06回](../sessions/06-smt-versions.md)。
同じ条件を真偽変数で書くか整数変数で書くかの判断。
**どちらか一方が常に正しいわけではない**（[SAT・SMT 概説](logic-sat-smt.md)）。

---

## 第07回の用語

### 最適化 {#optimization}

初出: [第07回](../sessions/07-theme-assignment.md)。
制約を満たす解のうち、目的の値が最も良いものを探すこと。
MiniZinc では `solve maximize` / `solve minimize` で指定する。

### 目的関数 {#objective_function}

初出: [第07回](../sessions/07-theme-assignment.md)。
最小化・最大化する量を表す式。**「良い解」の定義そのもの**である。

### ハード制約 {#hard_constraint}

初出: [第07回](../sessions/07-theme-assignment.md)。
**破ったら解として認められない**条件。
「なるべく守りたいが破ってもよい」[ソフト制約](#soft_constraint)と対になる。
全部をハード制約にすると [UNSAT](#unsat) になりやすい
（[定式化の7手順](modeling-steps.md)）。

### 実行可能解 {#feasible_solution}

初出: [第07回](../sessions/07-theme-assignment.md)。
すべての[ハード制約](#hard_constraint)を満たす解。良し悪しは問わない。

### 最適解 {#optimal_solution}

初出: [第07回](../sessions/07-theme-assignment.md)。
実行可能解のうち、目的関数の値が最も良いもの。複数あることもある。

### 合計の目的と最大の目的 {#total_vs_max_objective}

初出: [第07回](../sessions/07-theme-assignment.md)。
全体の合計を良くするか、最も悪い1つを良くするかの違いである。
合計を最大にすると、一部が極端に損をする解が選ばれることがある。

### 定員制約 {#capacity_constraint}

初出: [第07回](../sessions/07-theme-assignment.md)。
1つの選択肢に割り当てられる個数の上限を定める条件。

### 集計 {#aggregation_sum_count}

初出: [第07回](../sessions/07-theme-assignment.md)。
条件を満たす個数や値の合計を数えること。
MiniZinc では `count`、または `sum` と `bool2int` の組み合わせで書く
（第07回は `count`、第09回から後者）。

---

## 第08回の用語

### 列挙型 {#enum_type}

初出: [第08回](../sessions/08-roster-hard.md)。
取り得る値のそれぞれに名前を付けた型。
`enum SHIFTS = { day, night, off };` のように書く。

### シフトの表現 {#shift_representation}

初出: [第08回](../sessions/08-roster-hard.md)。
勤務表の各セルに勤務区分を1つ入れる表し方。
この取り方をすると「1人1日1勤務」が自動的に保証される。

### 必要人数制約 {#coverage_constraint}

初出: [第08回](../sessions/08-roster-hard.md)。
各日・各シフトに必要な人数を満たす条件。

### 資格制約 {#qualification_constraint}

初出: [第08回](../sessions/08-roster-hard.md)。
資格を持つ人を必ず配置する条件。

### 休息制約 {#rest_constraint}

初出: [第08回](../sessions/08-roster-hard.md)。
連続する日のあいだに置く条件。「夜勤の翌日は休み」など。

### 隣接する添字 {#adjacent_index}

初出: [第08回](../sessions/08-roster-hard.md)。
`roster[s, d]` と `roster[s, d + 1]` のように、隣り合う位置を同時に参照する書き方。
範囲外に出ないよう、繰り返しの範囲を1つ内側に刻む。

### 表現が保証する性質 {#representation_guarantees}

初出: [第08回](../sessions/08-roster-hard.md)。
変数の取り方そのものが自動的に満たす条件のこと。
**保証される性質は制約として書かない**。何が保証され、何を書くかを見分ける。

---

## 第09回の用語

### ソフト制約 {#soft_constraint}

初出: [第09回](../sessions/09-roster-soft.md)。
破ってもよいが、なるべく避けたい条件。
破った量を[違反ペナルティ](#penalty)として数え、目的関数に入れる。

### 違反ペナルティ {#penalty}

初出: [第09回](../sessions/09-roster-soft.md)。
ソフト制約を破ったときに加える値。破った量に比例させることが多い。

### 重み付き和 {#weighted_sum}

初出: [第09回](../sessions/09-roster-soft.md)。
複数のペナルティ項に重みを掛けて足した目的関数。
重みの決め方に唯一の正解は無く、**設計行為**である。

### 公平性の数値化 {#fairness_metric}

初出: [第09回](../sessions/09-roster-soft.md)。
偏りの大きさを式で表したもの。この教材では**勤務日数の偏り**（最大 − 最小）を主に使い、
夜勤回数の偏りを従に使う。**どの意味の公平を採るかを決めること**が数値化である。

### 正規化 {#normalization}

初出: [第09回](../sessions/09-roster-soft.md)。
値の範囲が違う項を、比較できるように揃えること。
桁が違う項をそのまま足すと、重みが意味を持たなくなる。

### 辞書式最適化 {#lexicographic_optimization}

初出: [第09回](../sessions/09-roster-soft.md)。
優先順位の高い目的から順に最適化し、
その値を固定してから次の目的を最適化する進め方である。

---

## 第10回の用語

### 独立した検証 {#independent_verification}

初出: [第10回](../sessions/10-roster-verification.md)。
モデルの外側で解の正しさを確かめること。
モデル自身に聞いても、モデルが間違っていれば間違った基準で答える。

### 正常例と反例 {#positive_and_negative_cases}

初出: [第10回](../sessions/10-roster-verification.md)。
通るはずの例と、違反を含んでいる例。
**反例で検査が反応すること**まで確かめて、はじめて検査が働いていると言える。

### 段階的テスト {#incremental_testing}

初出: [第10回](../sessions/10-roster-verification.md)。
制約を1つずつ足しながら、その都度期待どおりかを確かめる進め方。

### 機械可読な出力 {#machine_readable_output}

初出: [第10回](../sessions/10-roster-verification.md)。
別のプログラムが読める形で解を出すこと。
見た目の整形と、受け渡しのための形式は別に考える。

### ソルバー統計 {#solver_statistics}

初出: [第10回](../sessions/10-roster-verification.md)。
実行時間や探索の規模を示す数値。速さの評価に使う。

### 正しさと速さの分離 {#correctness_vs_speed}

初出: [第10回](../sessions/10-roster-verification.md)。
正しいかどうかと、速いかどうかを別々に評価すること。
**速いだけの間違ったモデルに価値は無い。**

---

## 関連ページ

- [用語初出台帳](../../design/glossary-ledger.md) — 初出回の正本（教材を書く人向け）
- [Prolog 早見表](prolog-cheatsheet.md) / [MiniZinc 早見表](minizinc-cheatsheet.md) / [Z3Py 早見表](z3py-cheatsheet.md)
- [SAT・SMT 概説](logic-sat-smt.md) — 命題論理まわりの用語の詳しい説明
- [定式化の7手順](modeling-steps.md) — 制約まわりの用語の使いどころ
