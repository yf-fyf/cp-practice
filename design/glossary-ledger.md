# 用語初出台帳

この文書は、**どの概念をどの回で初めて導入するか**の単一の出典である。
各回の原稿の frontmatter（`introduces:` / `requires:`）と
[用語集](../materials/references/glossary.md)は、いずれもこの台帳に従う。

`tools/check_docs.py` の `concepts` 検査と `glossary` 検査がこの文書を読む。
書式を変えると検査が読めなくなるので、下の様式のまま増減させる。

## 使い方

概念を1つ足すときの順序は次のとおりである。

1. **この台帳に1行足す。** 識別子（英語 slug）・用語（日本語の見出し）・意味の要点を書く。
2. その回の原稿の frontmatter `introduces:` に識別子を足す。
3. その概念を前提にする回の frontmatter `requires:` に識別子を足す。
   `requires:` は台帳の「前提」行からの導出値なので、台帳を先に直す。
4. [用語集](../materials/references/glossary.md)に
   `### <用語> {#<識別子>}` の項目を作り、初出回へ案内する。
5. `python3 tools/check_docs.py --only concepts,glossary` を通す。

## 様式

- 見出しは `## 第NN回 <回のタイトル>`。第01〜10回だけが概念を導入する。
- 各回の先頭に `**前提**:` の行を置き、その回が前提にする識別子を並べる。
  前提が無い回は `なし` と書く。
- 表の1列目が識別子、2列目が用語（用語集の見出しと**同じ文字列**にする）、
  3列目が意味の要点である。
- 識別子は小文字の英数字とアンダースコアだけで書く。
- **同じ識別子を2つの回で導入しない。**「初出」は1回だけである。
- 前提に書ける識別子は、**より前の回**で導入したものだけである。

第11〜15回（自由課題・発表会）は新しい概念を導入しない。
既習の概念を使うだけなので、この台帳に節を持たない。
それらの回の原稿は `introduces:` を空にし、`requires:` にはこの台帳の識別子だけを書く。

---

## 第01回 小型論理グリッド: 宣言的に関係を書く

**前提**: なし

| 識別子 | 用語 | 意味の要点 |
|---|---|---|
| `declarative_description` | 宣言的な記述 | 解を求める手順ではなく、成り立つ関係を書く書き方 |
| `knowledge_base` | 知識ベース | 事実と規則の集まり。問い合わせの対象になる |
| `fact` | 事実 | 無条件に成り立つと宣言した1行 |
| `query` | クエリ | 知識ベースへの問い合わせ。成功か失敗を返す |
| `predicate` | 述語 | 関係の名前と引数の個数の組 |
| `atom` | アトム | 小文字で始まる、それ自身を表す名前 |
| `prolog_variable` | 変数（Prolog） | 大文字か `_` で始まる、値がまだ決まっていない名前 |
| `rule` | 規則 | 条件が成り立てば頭部も成り立つ、と書いた節 |
| `conjunction` | 連言 | 「かつ」。条件をカンマで並べたもの |

## 第02回 論理グリッドの探索とモデル化: 候補生成からパズル完成まで

**前提**: `fact` / `rule` / `query` / `prolog_variable` / `conjunction`

| 識別子 | 用語 | 意味の要点 |
|---|---|---|
| `prolog_term` | 項 | Prolog が扱う値の単位。アトム・数・変数と、`p(a, B)` のようにそれらを括弧でまとめたもの |
| `list` | リスト | 値を順に並べたもの |
| `member` | member | リストから要素を1つ選ぶ述語 |
| `generate_and_test` | 生成とテスト | 候補を作ってから条件で落とす書き方 |
| `backtracking` | バックトラック | 失敗した地点まで戻って別の候補を試す動き |
| `unification` | 単一化 | 両辺が同じ形になるように、変数へ値を結びつける操作 |
| `disequality` | 非等号 | 「等しくない」を表す条件 |
| `multiple_solutions` | 複数解 | 条件を満たす答えが2つ以上あること |
| `graph` | グラフ | 頂点と、頂点を結ぶ辺の集まり |
| `graph_coloring` | 彩色問題 | 隣り合う頂点に異なる色を割り当てる問題 |
| `search_space` | 探索空間 | 試す可能性のある候補の全体 |

## 第03回 数独: MiniZincで盤面を解く

**前提**: `declarative_description` / `generate_and_test` / `graph_coloring`

| 識別子 | 用語 | 意味の要点 |
|---|---|---|
| `constraint_programming` | 制約プログラミング | 手順ではなく満たすべき条件を書き、探索はソルバーに任せる書き方 |
| `csp_vocabulary` | 制約充足問題（CSP）の基本語彙 | 変数・定義域・制約・割当て・解・充足の6語 |
| `parameter_vs_decision_var` | パラメータと決定変数 | すでに決まっている値と、ソルバーに決めてもらう値 |
| `minizinc_model_structure` | MiniZinc モデルの構造 | 宣言・`constraint`・`solve`・`output` の並び |
| `array_2d` | 2次元配列と添字集合 | 行と列で位置が決まる変数の並びと、その添字の範囲 |
| `forall_comprehension` | forall と配列内包表記 | 同じ形の条件・要素を繰り返し作る2つの道具 |
| `all_different` | 大域制約と all_different | よく使う条件にまとめて名前を付けたもの |

## 第04回 数独: データ分離、列挙、一意性

**前提**: `csp_vocabulary` / `minizinc_model_structure` / `array_2d` / `forall_comprehension` / `all_different`

| 識別子 | 用語 | 意味の要点 |
|---|---|---|
| `model_data_separation` | モデルとデータの分離 | 問題の構造と、個々のインスタンスを別々に持つこと |
| `dzn_data` | データファイル | パラメータの値だけを書いた入力ファイル |
| `multiple_solution_enumeration` | 複数解の列挙 | 2つ目以降の解も出させること |
| `solution_uniqueness` | 解の一意性 | 条件を満たす解がちょうど1つであること |
| `known_example_validation` | 既知例による検証 | 答えの分かっている例でモデルの正しさを確かめること |

## 第05回 SAT概説とパッケージ依存関係: Booleanモデル

**前提**: `csp_vocabulary` / `graph_coloring` / `model_data_separation`

| 識別子 | 用語 | 意味の要点 |
|---|---|---|
| `propositional_variable` | 命題変数 | 真か偽のどちらかになる変数 |
| `logical_connectives` | 論理演算 | 否定・論理積・論理和・含意 |
| `truth_table` | 真理値表 | 値の組み合わせをすべて並べ、式の値を書き出した表 |
| `satisfiability` | 充足可能性 | すべての式を同時に真にする割り当てが存在すること |
| `unsat` | UNSAT | どう値を選んでも同時には満たせないと分かった状態 |
| `cnf` | CNF | 節を「かつ」で並べた形。SAT ソルバーが受け取る形式 |
| `boolean_encoding` | Boolean 符号化 | 選択肢を真偽変数の組で表すこと |
| `exactly_one` | ちょうど一つ | 「少なくとも一つ」と「高々一つ」を並べて表す条件 |
| `z3py_basics` | Z3Py の基本操作 | 変数の作成・制約の追加・求解・解の読み出し |

## 第06回 SMT概説とバージョン選択: 整数モデル

**前提**: `logical_connectives` / `satisfiability` / `unsat` / `boolean_encoding` / `z3py_basics`

| 識別子 | 用語 | 意味の要点 |
|---|---|---|
| `smt` | SMT | 命題論理の骨組みに背景理論を組み合わせた充足可能性 |
| `background_theory` | 背景理論 | 整数や実数など、値の世界ごとの決まりを担当する部品 |
| `integer_variable` | 整数変数 | 大小の比較ができる値を取る決定変数 |
| `version_range` | バージョン範囲 | 依存先が満たすべき版の区間 |
| `unknown_result` | unknown | 解の有無を確かめきれなかったという結果 |
| `encoding_choice` | 符号化の選択 | 同じ条件を真偽変数で書くか整数変数で書くかの判断 |

## 第07回 学生と研究テーマの割当

**前提**: `csp_vocabulary` / `minizinc_model_structure` / `array_2d` / `forall_comprehension` / `model_data_separation`

| 識別子 | 用語 | 意味の要点 |
|---|---|---|
| `optimization` | 最適化 | 制約を満たす解のうち、目的の値が最も良いものを探すこと |
| `objective_function` | 目的関数 | 最小化・最大化する量を表す式 |
| `hard_constraint` | ハード制約 | 破ったら解として認められない条件 |
| `feasible_solution` | 実行可能解 | すべてのハード制約を満たす解 |
| `optimal_solution` | 最適解 | 実行可能解のうち目的の値が最も良いもの |
| `total_vs_max_objective` | 合計の目的と最大の目的 | 全体の合計を良くするか、最も悪い1つを良くするか |
| `capacity_constraint` | 定員制約 | 割り当てられる個数の上限を定める条件 |
| `aggregation_sum_count` | 集計 | 条件を満たす個数や値の合計を数えること |

## 第08回 ナーススケジューリング: ハード制約

**前提**: `csp_vocabulary` / `minizinc_model_structure` / `array_2d` / `forall_comprehension` / `all_different` / `model_data_separation` / `aggregation_sum_count` / `hard_constraint`

| 識別子 | 用語 | 意味の要点 |
|---|---|---|
| `enum_type` | 列挙型 | 取り得る値のそれぞれに名前を付けた型 |
| `shift_representation` | シフトの表現 | 各セルに勤務区分を1つ入れる表し方 |
| `coverage_constraint` | 必要人数制約 | 各日・各シフトに必要な人数を満たす条件 |
| `qualification_constraint` | 資格制約 | 資格を持つ人を必ず配置する条件 |
| `rest_constraint` | 休息制約 | 連続する日のあいだに置く条件 |
| `adjacent_index` | 隣接する添字 | 隣り合う日や位置を同時に参照する書き方 |
| `representation_guarantees` | 表現が保証する性質 | 変数の取り方そのものが自動的に満たす条件 |

## 第09回 ナーススケジューリング: ソフト制約と最適化

**前提**: `optimization` / `objective_function` / `aggregation_sum_count` / `hard_constraint` / `shift_representation` / `coverage_constraint`

| 識別子 | 用語 | 意味の要点 |
|---|---|---|
| `soft_constraint` | ソフト制約 | 破ってもよいが、なるべく避けたい条件 |
| `penalty` | 違反ペナルティ | ソフト制約を破ったときに加える値 |
| `weighted_sum` | 重み付き和 | 複数のペナルティ項に重みを掛けて足した目的関数 |
| `fairness_metric` | 公平性の数値化 | 偏りの大きさを式で表したもの。勤務日数の偏り（最大 − 最小）など |
| `normalization` | 正規化 | 値の範囲が違う項を、比較できるように揃えること |
| `lexicographic_optimization` | 辞書式最適化 | 優先順位の高い目的から順に最適化すること |

## 第10回 ナーススケジューリング: 検証と性能評価

**前提**: `known_example_validation` / `hard_constraint` / `soft_constraint` / `shift_representation` / `representation_guarantees`

| 識別子 | 用語 | 意味の要点 |
|---|---|---|
| `independent_verification` | 独立した検証 | モデルの外側で解の正しさを確かめること |
| `positive_and_negative_cases` | 正常例と反例 | 通るはずの例と、違反を含んでいる例 |
| `incremental_testing` | 段階的テスト | 制約を1つずつ足しながら確かめる進め方 |
| `machine_readable_output` | 機械可読な出力 | 別のプログラムが読める形で解を出すこと |
| `solver_statistics` | ソルバー統計 | 実行時間や探索の規模を示す数値 |
| `correctness_vs_speed` | 正しさと速さの分離 | 正しいかどうかと、速いかどうかを別々に評価すること |

---

## 用語の粒度について

いくつかの識別子は、関係の深い語をまとめて1項目にしてある。

| 識別子 | まとめている語 | 理由 |
|---|---|---|
| `csp_vocabulary` | 変数・定義域・制約・割当て・解・充足 | 6語を1つの語彙として同時に導入し、以後まとめて使うため |
| `logical_connectives` | 否定・論理積・論理和・含意 | 真理値表で一度に導入するため |
| `exactly_one` | 少なくとも一つ・高々一つ・ちょうど一つ | 前2つは後1つを作るための部品であるため |
| `z3py_basics` | `Bool` / `Solver` / `add` / `check` / `model` | 個別の API ではなく、ひとまとまりの操作として導入するため |
| `all_different` | 大域制約・`all_different` | この科目で使う大域制約が1つだけであるため |
| `aggregation_sum_count` | `sum` / `count` / `bool2int` による数え上げ | 同じ「数える」操作の別表現であるため |

分けたほうがよいと判断したら、台帳を分割してから原稿と用語集を直す。
順序を逆にすると、検査が差分を示してくれない。
