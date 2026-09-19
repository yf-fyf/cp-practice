# 第06回の発展　最適性・優先順位・別題材

[第06回の本文](lesson.md)の最適化から、全最適解、上限による証明、目的の優先順位へ進む。各問題に必要な条件と完成した出発モデルを用意するので、前の発展の完成は不要である。選択M06a・M06bも、関心に合わせて選べる。

モデルと入力の組、終了状態、複数ファイルの操作は[実行手引き](guides/optimization-check.md)を参照する。一つの最適解を見つけたこと、全最適解を列挙したこと、最適性の別の根拠を得たことを区別しよう。

## 発展1　すべての最適な割当 {#all-optima}

まず最適値を求め、次にその値を達成するすべての割当を探す。最適化の途中で表示される候補は、すべて最適とは限らず、表示された候補だけで全最適解が揃ったとも限らない。

### 条件と入力

4人A〜Dを講座1〜3へ一人ちょうど一つ割り当てる。許可が1の組だけを選び、講座の人数を定員以下にする。空席を許し、選んだ四つの不満度の合計Tを最小化する。二人の分離などの追加条件はない。

| 人 | 講座1の許可 | 講座2の許可 | 講座3の許可 | 不満度（講座1,2,3） |
|---|---:|---:|---:|---|
| A | 1 | 1 | 0 | 0, 1, 0 |
| B | 1 | 0 | 1 | 2, 1, 3 |
| C | 1 | 1 | 1 | 1, 4, 0 |
| D | 0 | 1 | 1 | 3, 3, 2 |
| 定員 | 2 | 1 | 1 | — |

[cost-base.dzn](../../../workbook/sessions/06-optimization/cost-base.dzn)がこの入力、[cost-zero.dzn](../../../workbook/sessions/06-optimization/cost-zero.dzn)は許可と定員を保ち、不満度をすべて0にした比較入力である。完成した[cost-demo.mzn](../../../workbook/sessions/06-optimization/cost-demo.mzn)と[assignment-core.mzn](../../../workbook/sessions/06-optimization/assignment-core.mzn)で最初の最適化を行える。

### 二段階の実行

`x[p,c]`{.minizinc} は人pが講座cを選ぶなら1、選ばないなら0、`cost[p,c]`{.minizinc} はその不満度、`total` は選んだ四つの不満度の合計Tである。`PEOPLE` はA〜Dに対応する1〜4、`COURSES` は1〜3。`cost-core.mzn` も `assignment-core.mzn` を読み込むので、両方を作業モデルと同じフォルダに置く。Gecodeでは出力末尾の `==========` まで確認し、途中の候補や時間切れを最適終了とは扱わない。

`cost-demo.mzn`で最適終了を確認し、最適値を記録する。次に[optimal-start.mzn](../../../workbook/sessions/06-optimization/optimal-start.mzn)と[cost-core.mzn](../../../workbook/sessions/06-optimization/cost-core.mzn)を使う。後者には基本条件とTの定義が完成しており、`solve`{.minizinc}は含まない。

1. **作業1：** 合計`total`を入力`best`と等しくする条件を書く。[best-start.dzn](../../../workbook/sessions/06-optimization/best-start.dzn)の0を、確認した最適値へ変更する。
2. **作業2：** `solve satisfy;`{.minizinc}を指定し、目的値を固定した充足問題として全解を列挙する。
3. 基本不満度と全不満度0の両方で行う。入力を変えたら最適値も求め直し、以前の値を流用しない。

```sh
minizinc --solver gecode cost-demo.mzn cost-base.dzn
minizinc --solver gecode --all-solutions optimal-start.mzn cost-base.dzn best-start.dzn
```

::: {.hint summary="ヒントを開く：最適値を制約にする"}
最初の実行で最小値がbと分かれば、次は`total=b`{.minizinc}を満たす解をすべて探せばよい。元の条件は保持する。目的を最小化し続ける実行の候補を、そのまま全最適解として数えない。
:::

基本不満度では最適値5の解が一つ、全不満度0では最適値0の解が四つある。各解の許可・人数と、選んだ不満度の合計を別に確認する。全解列挙の最後まで終了したことも必要である。

### 既知の一解の除外

全解を一度に列挙する代わりに、一つずつ既知の解を除く方法もある。[exclude-start.mzn](../../../workbook/sessions/06-optimization/exclude-start.mzn)では合計の固定まで用意した。[first.dzn](../../../workbook/sessions/06-optimization/first.dzn)はA〜Dの参加先1・1・3・2を0/1表で与える。

`exists(p in PEOPLE, c in COURSES)(x[p,c] != first[p,c])`{.minizinc}は、少なくとも一セルが違うことを表す。`exists`は指定した組のどれか一つで条件が成り立つ指定であり、全セルを違わせる`forall`ではない。

`first[p,c]`{.minizinc} は既知の割当を表す0/1入力であり、解の変数 `x` をその値に固定するものではない。`exclude-start.mzn` に不満度の入力・その入力の最適値を記した `best-start.dzn`・`first.dzn` を合わせて渡す。この一行で既知の一つだけを除き、別の最適解があるか調べる。基本入力では残らず、全不満度0では三つ残る。さらに列挙を続けるなら、見つけた各解について除外条件を残していく必要がある。

## 発展2　上限による最適性の説明 {#bound}

ソルバーが最適終了した結果に加え、不等式から目的値の上限を導く。達成できる解と、それを超えられない理由の両方が揃えば、最適性を別の方法でも説明できる。

### 問題と容量式

キット1をu個、キット2をv個作る。いずれも非負整数で、キット1は材料2・時間1・得点3、キット2は材料1・時間2・得点4を持つ。材料・時間の容量はいずれも8。使い切る義務はなく、得点を最大化する。

$$2u+v\le8,\qquad u+2v\le8,\qquad \text{得点}=3u+4v.$$

完成した[kits-base.mzn](../../../workbook/sessions/06-optimization/kits-base.mzn)・[kits-core.mzn](../../../workbook/sessions/06-optimization/kits-core.mzn)と[kits.dzn](../../../workbook/sessions/06-optimization/kits.dzn)から確認できる。必修2を自分で実装していなくてもよい。u=2、v=3なら材料7、時間8、得点18を達成する。

配布モデルの`div`{.minizinc}は整数除算で、非負の値なら割り算の小数部分を切り捨てる。材料容量の入力 `material_capacity` と時間容量の入力 `time_capacity` を使い、`material_capacity div 2`{.minizinc}と`time_capacity div 2`{.minizinc}をそれぞれu・vの安全な上限に使い、入力を変えても範囲が追従する。

### 不等式を足す方法

不等式の両辺へ非負の数を掛け、二つの式を足すと、新しい上限を得られる。例えば容量式をそのまま足すと $3u+3v\le16$ になるが、これはまだ得点の式とは係数が異なる。

1. 材料式と時間式に掛ける非負の係数を探し、左辺を得点式の定数倍にする。
2. 得点が整数であることを使い、小数部分を切り捨てた上限を求める。
3. 得点18を達成する解と上限を比較し、それよりよい整数解がない理由を説明する。

::: {.hint summary="ヒントを開く：得点式の三倍"}
材料式を2倍、時間式を5倍して足すと、左辺は`9*u+12*v`{.minizinc}、右辺は56となる。左辺を`3*(3*u+4*v)`{.minizinc}として読めるか確認しよう。
:::

得点は $56/3$ 以下で整数なので、上限は18である。u=2、v=3が18を達成するため、最適と結論できる。この説明では、連続量として割り切れないことを整数の性質で補っている。

比較として、個数の範囲を理由なく0/1へ狭めた場合を調べよう。その問題の最大得点は7となり、元の問題の解を失う。容量から導く上限4と、人為的な上限1の違いを説明する。一般の最適化アルゴリズムや双対理論の習得は求めない。

## 発展3　目的に優先順位を付ける {#priority}

最初に第一目的を最適化し、その最適値を保ったまま第二目的を良くする。順序が入れ替わると別の結果になり得るため、単に二つの量を足し引きする方法との違いも確かめよう。

### 条件と二つの目的

キット1をu個、キット2をv個作る。非負整数の個数とし、キット1は材料2・時間1、キット2は材料1・時間2を使う。材料・時間の容量はいずれも8で、使用量は容量以下とする。

両キットの1個当たりの得点を1とする。第一目的は個数合計 $S=u+v$ の最大化、第二目的は使用時間 $R=u+2v$ の最小化とする。第一目的を悪くして時間を減らすことは許さない。

[kits-lex.dzn](../../../workbook/sessions/06-optimization/kits-lex.dzn)と完成した[kits-base.mzn](../../../workbook/sessions/06-optimization/kits-base.mzn)・[kits-core.mzn](../../../workbook/sessions/06-optimization/kits-core.mzn)を使う。ここではモデル内の`score`がS、`time_used`がRを表す。前の発展の完成は不要である。

### 二段階法

まず`kits-base.mzn`でSを最大化し、最適終了を確認する。次に[lex-start.mzn](../../../workbook/sessions/06-optimization/lex-start.mzn)の二つのTODOを埋める。第一段階で得た値は`best`として入力する。

1. **作業1：** `score`を確認した最適値`best`へ固定する。
2. **作業2：** `time_used`を最小化する。
3. 第一目的の最適値を満たす個数を列挙し、第二目的で何が選ばれたか比較する。[best-start.dzn](../../../workbook/sessions/06-optimization/best-start.dzn)はこの問題の最適値へ変更して使う。

```sh
minizinc --solver gecode kits-base.mzn kits-lex.dzn
minizinc --solver gecode lex-start.mzn kits-lex.dzn best-start.dzn
```

第一目的の最大Sは5で、u・vが2・3または3・2の二組が残る。使用時間はそれぞれ8と7なので、第二目的は3・2を選ぶ。時間を先に最小化すると0・0になることも確認し、優先順位の意味を説明する。

別の解を一つずつ探すなら、既知のu・vをa・bとして `u != a \/ v != b`{.minizinc} を追加する。`\/`{.minizinc}は「または」であり、どちらかが違えば別解となる。全列挙する場合は、目的値を最適値へ固定した充足問題で`--all-solutions`を使う。

### 重みで優先する方法

[weighted-start.mzn](../../../workbook/sessions/06-optimization/weighted-start.mzn)では、重みWを使った $W S-R$ の最大化を実装する。[weight-start.dzn](../../../workbook/sessions/06-optimization/weight-start.dzn)のWを変えて、二段階法と比較しよう。作業モデルに `kits-lex.dzn` と `weight-start.dzn` を合わせて渡し、共通の `kits-core.mzn` も同じフォルダへ置く。

Sは整数、Rは0〜8なので、W>8ならSが1増えた効果が、Rの変化による損失を必ず上回る。同じSではRが小さいほどよくなるため、W=9は今回の優先順位を守る十分な重みである。

::: {.hint summary="ヒントを開く：小さい重みの反例"}
W=1では`S-R`が`-v`{.minizinc}となる。v=0ならuにかかわらず同じ評価になり、個数合計を5にできない解も選ばれる。目的の単位と取り得る範囲を使わず、重みを適当に決めてはいけない。
:::

W=9なら二段階法と同じ3・2を選ぶ。W=1ではv=0、u=0〜4の五つが同じ最適値0となり、第一目的を守れない。最初に出た一組だけでなく、重み付き目的値を固定した全解も調べよう。

### 小さい入力群への一般化

[lex-cases.json](../../../workbook/sessions/06-optimization/lex-cases.json)は、材料容量・時間容量・各キットの正の整数得点を変えた七入力である。最初の入力は上の問題で、ほかは第一目的を $S=\mathrm{score\_u}u+\mathrm{score\_v}v$ とする。第二目的は使用時間Rのままにする。

七入力の値を次に示す。列は順に `material_capacity`、`time_capacity`、`score_u`、`score_v` に対応する。キット1個当たりの使用量は、キット1が材料2・時間1、キット2が材料1・時間2のままとする。

| 材料容量 | 時間容量 | uの得点 | vの得点 |
|---:|---:|---:|---:|
| 8 | 8 | 1 | 1 |
| 4 | 5 | 2 | 1 |
| 5 | 3 | 1 | 3 |
| 7 | 9 | 2 | 3 |
| 3 | 8 | 3 | 1 |
| 0 | 4 | 1 | 2 |
| 8 | 8 | 1 | 2 |

[lex-general-start.py](../../../workbook/sessions/06-optimization/lex-general-start.py)と[solve_tools.py](../../../workbook/sessions/06-optimization/solve_tools.py)を使い、完成させた`lex-start.mzn`・`weighted-start.mzn`を同じフォルダに置く。`run`は終了状態と解、`optimum`は最適終了した結果の目的値を返す。MiniZinc CLIをPythonから呼ぶ部分は用意してある。

1. **作業1：** 第一目的の最適値を得て、その値を固定した第二段階を実行する。
2. **作業2：** 各入力の時間容量からRの上限を読み、十分なWを導き直す。重み付き法の結果と二段階法を比較する。
3. 容量内の非負整数u・vを独立に列挙し、第一目的最大・その中で時間最小の集合を求める。二段階法と重み付き法でも最終目的値を固定し、全最適解の集合が一致するか調べる。

```sh
python3 lex-general-start.py lex-cases.json
```

入力ごとにRは0以上・時間容量以下なので、Wを時間容量+1にすれば十分である。0の容量を含む入力でも、0個ずつは実行可能な出発点になる。返された一解だけの一致で終えず、最適値と最適解の集合まで確かめよう。

## 選択M06a　各一つだけの持ち物 {#knapsack}

製作個数から、各品物を持っていくかどうかへ変数の意味を変える。目安は10〜20分。数量モデルの変数をそのまま使ってよいかを考え、容量と目的を組み合わせる。

### 条件と入力

四つの品物は各一つずつしかなく、分割も複製もできない。重さの合計を容量以下とし、価値の合計を最大にする。容量を使い切る必要はなく、最初は7、次に6で解く。

| 品物 | 重さ | 価値 |
|---|---:|---:|
| A | 2 | 3 |
| B | 3 | 4 |
| C | 4 | 5 |
| D | 5 | 8 |

[knapsack-start.mzn](../../../workbook/sessions/06-optimization/knapsack-start.mzn)には重さ・価値の入力と、合計の式・出力を用意した。品物番号 `i=1〜4` はA〜Dに対応し、`weight[i]`{.minizinc} が重さ、`value[i]`{.minizinc} が価値、`capacity` が容量である。変数`take[i]`{.minizinc}の定義域を決め、各品物を選ぶかどうかを表す。キットの資源や一人一講座の条件は使わない。

### 作業と自己確認

**作業1**で選択変数を宣言し、**作業2**で重さの容量制約と価値の最大化を書く。[容量7](../../../workbook/sessions/06-optimization/knapsack-7.dzn)と[容量6](../../../workbook/sessions/06-optimization/knapsack-6.dzn)を交換し、選んだ品物・重さ・価値を再計算する。

::: {.hint summary="ヒントを開く：個数ではなく選択"}
各品物は一つだけなので、`take[i]`{.minizinc}は0か1である。重さの和も価値の和も同じ選択変数を使い、掛ける係数だけを変える。容量は上限であって満杯にする条件ではない。
:::

容量7の最適はAとDで、重さ7・価値11。容量6の最適値は8で、AとCの組、Dだけの二つを許す。後者は重さ5で空き容量1があるので、容量を等号にする実装では正しい最適解を落とす。変数を0〜4の製作個数にすると、同じ品物を複製する別の問題になる。

## 選択M06b　二種類のケーキ {#cakes}

二つの製作個数を決める構造を、五つの資源へ広げる。目安は10〜20分。各資源の行を一つの容量式に対応させ、個数の境界を入力から導こう。

### 条件と入力

バナナケーキb個、チョコケーキc個を作る。個数は非負整数、すべての材料使用量を容量以下とする。材料を使い切る必要はなく、売上を最大にする。原価は与えないので、目的は利益ではなく売上である。

| 資源 | バナナ1個 | チョコ1個 | 容量 |
|---|---:|---:|---:|
| 小麦粉（g） | 250 | 200 | 4000 |
| バナナ（本） | 2 | 0 | 6 |
| 砂糖（g） | 75 | 150 | 2000 |
| バター（g） | 100 | 150 | 500 |
| ココア（g） | 0 | 75 | 500 |
| 売上（整数単位） | 400 | 450 | — |

計算用の数値であり、料理の実用レシピではない。[cakes-start.mzn](../../../workbook/sessions/06-optimization/cakes-start.mzn)に入力宣言・売上の式・各資源の使用量表示、[cakes.dzn](../../../workbook/sessions/06-optimization/cakes.dzn)に容量を用意している。

### 作業と自己確認

**作業1**でb・cの意味と安全な整数範囲を定める。**作業2**で五つの容量制約と売上の最大化を書く。式の係数は、各資源の行を横に読んで個数へ掛ける。

::: {.hint summary="ヒントを開く：二つの個数の上限"}
バナナの容量から`2*b <= 6`{.minizinc}なのでb≤3。bが非負ならバターの条件から`150*c <= 500`{.minizinc}なので、整数cは3以下になる。例えば小麦粉の条件は`250*b+200*c <= 4000`{.minizinc}で、ほかの資源も別々に制約する。
:::

最適はb=c=2で売上1700。使用量は小麦粉900g、バナナ4本、砂糖450g、バター500g、ココア150gである。すべての容量と個数の非負性を確認し、余った材料があっても正しいことを説明する。

b=3、c=2を固定すると、バター600gだけが容量を超えるので拒否する。小麦粉・バナナ・砂糖・ココアの条件を満たすことも確かめ、一つの資源の制約漏れを見分けよう。題材の原典は[MiniZinc公式教材の算術最適化](https://docs.minizinc.dev/en/stable/modelling.html#an-arithmetic-optimisation-example)である。
