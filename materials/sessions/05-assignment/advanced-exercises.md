# 第05回の発展　割当の表現と不可能性

[第05回の本文](lesson.md)の0/1表から、別表現・二人の分離・不可能性の説明へ進む。各問題に出発点を用意しているので、前の発展を完成していなくても取り組める。選択M05は、条件が成り立つ個数を数える別の題材である。

実行操作と配布物は[確認手引き](guides/assignment-check.md)にまとめた。0/1表では1の位置を、一人一変数の表現では講座番号を読む。表現を変えても、元の問題で許される割当が変わっていないかを確認しよう。

| 問題 | 出発点 | 主に考えること |
|---|---|---|
| 発展1 | [value-start.mzn](../../../workbook/sessions/05-assignment/value-start.mzn) | 講座番号から人数を数え、許可を参照する |
| 発展2 | [separate-start.mzn](../../../workbook/sessions/05-assignment/separate-start.mzn) | 特定の二人の同時選択を禁止する |
| 発展3 | [obstruction-start.py](../../../workbook/sessions/05-assignment/obstruction-start.py) | 最少人数の障害集合を探す |
| 選択M05 | [series-start.mzn](../../../workbook/sessions/05-assignment/series-start.mzn) | 数字の出現回数を数える |

## 発展1　一人一変数の表現 {#value}

一人が選ぶ講座番号を、一つの決定変数で表す。変数の数を減らすだけでは完成しない。0/1表で行っていた人数の集計と許可の確認を、新しい表現に合わせて書こう。

### 条件と変数

5人A〜Eを講座1〜3へ一人ちょうど一つ割り当てる。各講座の人数は定員以下、許可が1の組合せだけを選ぶ。AとDの分離条件は置かない。人の番号1〜5はA〜Eに対応する。

| 人 | 講座1 | 講座2 | 講座3 |
|---|---:|---:|---:|
| A | 1 | 1 | 0 |
| B | 1 | 0 | 1 |
| C | 1 | 1 | 1 |
| D | 0 | 1 | 1 |
| E | 1 | 0 | 1 |
| 定員 | 2 | 2 | 1 |

入力は[practice.dzn](../../../workbook/sessions/05-assignment/practice.dzn)。変数 $y_p\in\{1,2,3\}$ を人pの参加先の講座番号とする。一人に一つの値を割り当てるので、行和=1に当たる条件を別に書く必要はない。

### 人数と許可の記述

[value-start.mzn](../../../workbook/sessions/05-assignment/value-start.mzn)には、講座番号を表す変数 `y[p]`{.minizinc}、入力と表示がある。`PEOPLE` は人の番号1〜5、`COURSES` は講座番号1〜3、`allowed[p,c]`{.minizinc} はこの問題の許可表、`cap[c]`{.minizinc} は定員である。`practice.dzn` と組み合わせ、次の二条件を補う。

`bool2int(条件)`{.minizinc}は、条件が真なら1、偽なら0を表す。例えば`y[1]=2`{.minizinc}のとき、`bool2int(y[1]=2)`{.minizinc}は1、`bool2int(y[1]=1)`{.minizinc}は0である。条件に決定変数を含むので、値は解が決まるのに応じて決まる。

また、`allowed[p,y[p]]`{.minizinc}は、人pの行で、選んだ講座番号の列を参照する。添字が決定変数でも、定義域が講座番号の範囲にあるため、その講座の許可を制約へ使える。

1. **作業1：** 各講座cについて、`y[p]=c`{.minizinc}となる人pを`bool2int`と`sum`で数え、定員以下にする。
2. **作業2：** 各人で、選んだ講座の許可が1である条件を書く。
3. 全解を求め、0/1表との変換で同じ割当集合になるか調べる。完成した[assignment-base.mzn](../../../workbook/sessions/05-assignment/assignment-base.mzn)を同じ入力で実行できる。

::: {.hint summary="ヒントを開く：一つの講座の人数"}
講座cを固定して `sum(p in PEOPLE)(bool2int(y[p] = c))`{.minizinc} を考える。講座番号そのものの合計ではなく、「この講座を選んだ」という真偽を0/1へ変えて足す。
:::

変換は、`y[p]=c`{.minizinc}のセルだけを1、それ以外を0にする。解は6通りで、0/1表と講座番号の表現は相互に変換できる。件数だけでなく、六つの割当を並べて同じものが揃っているか照合しよう。変数の少なさだけで処理速度の優劣を結論しない。

## 発展2　二人の参加先の分離 {#separate}

運営を手伝う二人が同じ講座に集まらないようにする。表全体の行や列だけでなく、同じ列にある特定の二人のセルを取り出して考えよう。基本の三条件は引き続き必要である。

### 条件と入力

::: {.given label="条件と入力"}
5人A〜Eを講座1〜3へ一人ちょうど一つ割り当てる。許可が1の組合せだけを選び、各講座の人数は定員以下とする。空席を残してもよい。

| 人 | 講座1 | 講座2 | 講座3 |
|---|---:|---:|---:|
| A | 1 | 1 | 0 |
| B | 1 | 0 | 1 |
| C | 1 | 1 | 1 |
| D | 0 | 1 | 1 |
| E | 1 | 0 | 1 |
| 定員 | 2 | 2 | 1 |

さらに、運営補助員AとDは異なる講座へ入る。人の番号はA=1、B=2、C=3、D=4、E=5。これらを満たす割当を一つ求める。
:::

### 作業と自己確認

[separate-start.mzn](../../../workbook/sessions/05-assignment/separate-start.mzn)を使う。同じフォルダーに置く[assignment-base.mzn](../../../workbook/sessions/05-assignment/assignment-base.mzn)には一人一講座・定員以下・許可された参加先だけを選ぶ条件が完成している。`x[p,c]`{.minizinc} は人pが講座cを選ぶなら1、選ばなければ0を表す。`PEOPLE` は1〜5、`COURSES` は1〜3である。入力は、この問題の許可・定員表を収めた[practice.dzn](../../../workbook/sessions/05-assignment/practice.dzn)を使う。必修の作業が途中でも、この出発点から追加条件を考えられる。

```{.minizinc filename="separate-start.mzn"}
% TODO(作業1): 各講座でAとDが同時に選ばれない条件を書く。
% TODO(作業2): 通る表と、A・Dが同じ講座の表を固定して確かめる。
```

1. **作業1：** 講座cを一つ固定し、AとDの二つの0/1値が同時に1にならない条件を考える。それをすべての講座へ広げ、`practice.dzn`で実行する。
2. **作業2：** [check-valid.dzn](../../../workbook/sessions/05-assignment/check-valid.dzn)と[check-same.dzn](../../../workbook/sessions/05-assignment/check-same.dzn)を別々に指定し、追加条件の効果を確かめる。

A〜Eが1・1・2・2・3を選ぶ表は、Aが1、Dが2なので受理する。2・1・1・2・3を選ぶ表は、基本の三条件には違反しないがAとDがともに2なので拒否する。追加条件を消すと後者が通る理由も説明しよう。

全員を異なる講座にする条件へ強めないことにも注意する。講座は3種類で人は5人なので、全員別では解がなくなる。今回分けるのはAとDだけで、ほかの人が同じ講座へ入ることは許される。全列挙する場合は3解になる。

::: {.hint summary="ヒントを開く：二つの0/1値の合計"}
同じ講座cでAとDがともに選ばれると、`x[1,c] + x[4,c]`{.minizinc}は2になる。どちらも選ばない0と、片方だけ選ぶ1は許してよい。各講座でこの和の上限を定める。
:::

## 発展3　割当できない理由 {#obstruction}

定員の総和が人数以上でも、許可の偏りによって割当できない場合がある。ある人たちが参加できる講座だけを集め、そこに十分な枠があるかを調べると、不可能性を短く説明できる。

### 条件と障害集合

5人A〜Eを講座1〜3へ一人ちょうど一つ割り当て、各講座は定員以下とする。許可が1の組合せだけを選ぶ。開催有無や二人の分離などの追加条件はない。

| 人 | 講座1 | 講座2 | 講座3 |
|---|---:|---:|---:|
| A | 1 | 1 | 0 |
| B | 1 | 1 | 0 |
| C | 1 | 1 | 0 |
| D | 0 | 0 | 1 |
| E | 0 | 0 | 1 |
| 定員 | 1 | 1 | 3 |

[impossible.dzn](../../../workbook/sessions/05-assignment/impossible.dzn)と完成した[assignment-base.mzn](../../../workbook/sessions/05-assignment/assignment-base.mzn)を実行すると解なしになる。総定員は5なので、総数だけでは原因を説明できない。人の集合Uに対し、その中の誰かに許可された講座の集合を $C(U)$ とする。

$$\sum_{c\in C(U)}\mathrm{cap}_c < |U|$$

なら、Uの人たちは利用できる枠に入りきらない。この不等式を満たすUを、ここでは**障害集合**と呼ぶ。同じ講座を複数の人が利用できても、定員は一度だけ数える。

### 探索と一般化

[obstruction-start.py](../../../workbook/sessions/05-assignment/obstruction-start.py)にはJSONの入力読込みと表示を用意した。実装する `minimum_obstruction` の返り値は、障害集合に含む人の内部番号の組である。`allowed`は人×講座の0/1表、`cap`は非負整数の定員リストである。内部の人・講座番号は0始まり、画面への表示は1始まりにしている。

1. **作業1：** 人の集合を少ない人数から試す。`combinations(range(len(allowed)), size)`{.python}で、size人の組を重複なく列挙できる。
2. **作業2：** その人たちに許された講座の集合を作り、定員総和と人数を比べる。足りなければ人の集合を返し、すべて調べてなければ`None`を返す。
3. [impossible.json](../../../workbook/sessions/05-assignment/impossible.json)と[repaired.json](../../../workbook/sessions/05-assignment/repaired.json)で実行する。後者は許可を変えず、定員を2・1・3に増やした入力である。

```sh
python3 obstruction-start.py impossible.json
python3 obstruction-start.py repaired.json
```

::: {.hint summary="ヒントを開く：共有する枠は一度だけ"}
A・B・Cの誰もが講座1・2を利用できるが、枠は1+1の2席だけである。人ごとに2席を足して6席と数えてはいけない。先に利用できる講座を集合へまとめ、その集合について定員を足す。
:::

最初の入力ではA・B・Cの3人に対して利用できる枠が2であり、最少人数の障害集合になる。修正入力では障害集合が見つからず、MiniZincでも3通りの割当が得られる。[repaired.dzn](../../../workbook/sessions/05-assignment/repaired.dzn)で照合しよう。

最後に、小さい別入力にも使えるようにする。人数・講座数・許可・定員を変え、返された集合が不等式を満たすことと、より少ない障害集合がないことを確認する。`product(range(n_courses), repeat=n_people)`{.python}で全参加先を列挙し、許可と定員を検査する方法とも比較できる。追加の分離や開催条件まで含む問題では、それらによる不可能性をこの不等式だけで検出できるとは限らない。

## 選択M05　出現回数を表す数列 {#series}

講座への割当から離れ、条件が成り立つ回数を数える別の問題を扱う。目安は15〜25分。`bool2int`と0始まりの添字はここで説明するので、発展1の完成は不要である。

### 問題と添字

長さ4の整数列 $s[0],s[1],s[2],s[3]$ を求める。各要素は0以上4以下とし、s[i]は「この数列の中に数iが現れる回数」と等しくする。講座の定員や許可の条件は使わない。

| 位置 | その位置の値が表すもの |
|---|---|
| s[0] | 0が現れる個数 |
| s[1] | 1が現れる個数 |
| s[2] | 2が現れる個数 |
| s[3] | 3が現れる個数 |

位置の番号と、その位置に入っている値を区別しよう。[series-start.mzn](../../../workbook/sessions/05-assignment/series-start.mzn)には変数の宣言・入力と表示があり、添字を`0..n-1`{.minizinc}、値を`0..n`{.minizinc}とし、[series.dzn](../../../workbook/sessions/05-assignment/series.dzn)でn=4を与える。0は正しい数列の値でもある。

### 作業と自己確認

`bool2int(s[j] = i)`{.minizinc}は、位置jの値がiなら1、それ以外なら0を表す。数列が未知なので、この0/1もまだ決まっていない。すべての位置jについて足すと、数iの出現回数になる。

1. **作業1：** iを一つ固定し、位置jを`0..n-1`{.minizinc}で動かして出現回数を表す。
2. **作業2：** 各iについて、その出現回数と`s[i]`{.minizinc}が等しいことを`forall`で課す。
3. 得られた数列で0・1・2・3を実際に数え直す。全解を求める場合は、異なる二つの数列が得られる。

::: {.hint summary="ヒントを開く：数える値と探す位置"}
iは数える数字、jは数列の位置である。例えばi=0なら、四つの位置で`s[j]=0`{.minizinc}が成り立つ個数を足し、その値を`s[0]`{.minizinc}と等しくする。外側ではiを0〜3のすべてへ広げる。
:::

解は(1,2,1,0)と(2,0,2,0)で、どちらも正しい。例えば前者には0が1個、1が2個、2が1個、3が0個ある。[series-wrong.dzn](../../../workbook/sessions/05-assignment/series-wrong.dzn)の(1,1,1,1)は、和が4でも出現回数の条件に違反する。和だけに置き換えず、各数字の個数を指定しよう。

記法は[MiniZinc公式教材のBoolean式と出現回数](https://docs.minizinc.dev/en/stable/modelling2.html#complex-constraints)でも確認できる。この選択演習の完成や`bool2int`の構文を、次の必修の前提にはしない。
