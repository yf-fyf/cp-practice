# 第08回の発展　指標を検査し、選び方を比べる

[第08回の本文](lesson.md)で扱った勤務表を使い、出力の再計算、個人の最大違反、支配されない候補の列挙へ進む。各問題に入力と必要な完成部分を用意してあり、前の発展や第06回の発展の完成は不要である。

ファイルの組合せと実行方法は[確認手引き](guides/preferences-check.md)で確認できる。表が条件を満たすこと、指標の計算が合うこと、その目的について最適であることを分けて調べよう。

## 発展1　出力からの独立した再計算 {#recalculate}

ソルバーと別のPythonプログラムで日数・希望違反・日数差を求める。入力はすでに配列になっているので、最適化やMiniZincの出力文字列の解析ではなく、表を走査する計算に集中できる。

### 条件と確認用の表

5人A〜E、4日間の0/1勤務表を扱う。各日ちょうど2人、一人合計2日以下、勤務可能性0では勤務させない。各欄は1〜4日目の順で、希望1は休みたいこと、希望0は休み希望なしを表す。

| 人 | 勤務可能性 | 元の休み希望 | 比較する休み希望 |
|---|---|---|---|
| A | 1 1 0 1 | 0 0 0 0 | 0 0 0 0 |
| B | 1 0 1 1 | 0 0 0 0 | 0 0 0 0 |
| C | 0 1 1 1 | 0 0 0 0 | 0 0 0 0 |
| D | 1 1 1 0 | 0 0 0 0 | 0 0 0 0 |
| E | 1 1 1 1 | 1 1 1 1 | 0 0 0 1 |

[request-demo.json](../../../workbook/sessions/08-preferences/request-demo.json)と[request-practice.json](../../../workbook/sessions/08-preferences/request-practice.json)に二つの入力、[examples.json](../../../workbook/sessions/08-preferences/examples.json)に確認用の勤務表を配列で用意した。Pythonでは勤務の有無を `work[p][d]`{.python} と書き、勤務なら1、休みなら0とする。p・dとも0から数え、行0〜4がA〜E、列0〜3が日1〜4である。`data` は希望入力のJSONを読んだ辞書で、`available` が勤務可能性、`request` が休み希望の5行×4列表、`required` が各日2人、`max_days` が各人2日以下を表す。

| 名前 | 日ごとの担当者（1〜4日） | 日数A〜E |
|---|---|---|
| S0 | AB／AD／CD／BC | 2,2,2,2,0 |
| S1 | AB／AC／BD／CE | 2,2,2,1,1 |
| P1 | AB／AE／CD／BC | 2,2,2,1,1 |

各人の日数をL、希望位置で勤務した回数の合計をV、勤務0日の人も含む全員の日数の最大と最小の差をFとする。kを指定したときだけV≤kも確認する。これは指標と条件の検査で、最適化は行わない。

### 再計算する関数

[recalculate-start.py](../../../workbook/sessions/08-preferences/recalculate-start.py)と[roster_io.py](../../../workbook/sessions/08-preferences/roster_io.py)を使う。後者はJSONを読む処理と、表の大きさ・0/1・勤務可能性・各日人数・各人上限の基本検査を提供する。

1. **作業1：** `recalculate(work, data, k=None)`{.python}で全員の日数`load`を求め、希望と勤務からV、全員の日数からFを計算する。
2. **作業2：** kが指定され、V>kなら`errors`へ`'cap'`{.python}を追加する。`valid`、`errors`、`load`、`V`、`F`を持つ辞書を返す。
3. 二つの希望入力でS0・S1・P1を調べ、さらに元の希望でk=0とk=1を試す。基本検査に失敗した表は、提供済みの分岐で`valid=False`{.python}と原因を返す。

kの未指定は`None`{.python}である。`if k:`{.python}と書くとk=0の場合を飛ばしてしまうので、0という上限も検査の対象に含めよう。`valid` は `errors` が空のときだけ `True`{.python} にする。例えば元の希望・S0・k=0では、戻り値は次の形になる。

```python
{"valid": True, "errors": [], "load": [2,2,2,2,0], "V": 0, "F": 2}
```

```sh
python3 recalculate-start.py request-demo.json examples.json --k 0
python3 recalculate-start.py request-practice.json examples.json
```

::: {.hint summary="ヒントを開く：和と最大・最小の対象"}
日数は行ごとに足す。Vは全セルの`work[p][d]*data['request'][p][d]`{.python}を足す。Fは全員の日数に対する`max(load)-min(load)`{.python}で、勤務0日の行も残す。kが指定されたかは`k is not None`{.python}で調べる。
:::

元の希望ならS0は(V,F)=(0,2)、S1とP1は(1,1)。比較する希望ならS0は(0,2)、S1は(1,1)、P1は(0,1)になる。同じ勤務表の希望入力だけを変えても、日数とFは変わらない。

元の希望でS1はk=0を破り、k=1を満たす。S0はどちらも満たすが、k=1でFを最小にする問題では最適ではない。検査が通ることだけでは、よりよい別表がないことの証明にはならない。

## 発展2　個人の最大違反と合計 {#individual}

希望違反の合計を小さくすると、一人へ違反が集中する場合がある。各人の違反を経由して、その中の最大を小さくする目的と比べる。今回は勤務日数の差ではなく、希望違反の分布を見る。

### 条件と比較用の希望

5人A〜E、4日間、各日ちょうど2人、一人合計2日以下、勤務可能性0では勤務させない。勤務するなら1、休むなら0で、以下の各欄は1〜4日目の順。希望1の位置で勤務すると、その人の違反を1回数える。

| 人 | 勤務可能性 | 比較用の休み希望 |
|---|---|---|
| A | 1 1 0 1 | 1 1 0 1 |
| B | 1 0 1 1 | 0 0 1 1 |
| C | 0 1 1 1 | 0 1 0 0 |
| D | 1 1 1 0 | 1 1 1 0 |
| E | 1 1 1 1 | 1 1 0 0 |

入力は[request-individual.dzn](../../../workbook/sessions/08-preferences/request-individual.dzn)。人pが日dに勤務するかを $x_{p,d}$、その位置に休み希望があるかを $r_{p,d}$ とし、それぞれ当てはまるなら1、当てはまらないなら0とする。個人の違反を $v_p=\sum_d r_{p,d}x_{p,d}$、合計を $V=\sum_p v_p$、一人の最大違反を $M=\max_p v_p$ とする。V最小化とM最小化を別々に行う。V≤k、日数差の最小化、重み付き目的は追加しない。

### 二つの最小化

[individual-start.mzn](../../../workbook/sessions/08-preferences/individual-start.mzn)、[metrics-core.mzn](../../../workbook/sessions/08-preferences/metrics-core.mzn)、[roster-core.mzn](../../../workbook/sessions/08-preferences/roster-core.mzn)を使う。モデルでは `work[p,d]`{.minizinc} が $x_{p,d}$、`request[p,d]`{.minizinc} が $r_{p,d}$、`available[p,d]`{.minizinc} が勤務可能性、`load[p]`{.minizinc} が勤務日数である。`PEOPLE=1..5`{.minizinc} がA〜E、`DAYS=1..4`{.minizinc} が日1〜4に対応する。Vと日数の計算は完成している。個人の違反配列と、何を最小化するかを追加する。

1. **作業1：** `personal[p]`{.minizinc}で個人の違反を定義し、`worst=max(personal)`{.minizinc}でMを定義する。最大を取る前に、人ごとの合計を作る。
2. **作業2：** Vを表す`violations`の最小化を実行し、次にMを表す`worst`の最小化へ`solve`{.minizinc}を切り替えて実行する。一つの実行に`solve`{.minizinc}は一つとする。
3. 表から各人の違反を再計算する。Mが同じ表は、合計Vも同じかを調べる。

`max(personal)`{.minizinc}は全員の個人違反の中から最大値を取る式である。個人の違反は勤務日数以下なので、0〜日数という範囲で宣言できる。出力の足場は`personal`と`worst`を表示する。

::: {.hint summary="ヒントを開く：集計を二段にする"}
人pを固定し、日について希望と勤務の積を足して`personal[p]`{.minizinc}へ結び付ける。これを全員分定義してから、配列全体へ`max`を適用する。合計VをそのままMの代わりにしない。
:::

Vの最小値は3で、その最適表ではM=2。例AB／AD／CE／CEでは、個人違反は(2,0,0,1,0)となる。Mの最小値は1で、例AB／CD／BE／CEの個人違反は(1,1,1,1,0)、合計V=4となる。

Mだけを最小にした最適表にはV=5のものもある。最大違反が1なら、V=4の表とV=5の表をこの目的だけでは区別しない。全表を比べたい場合は、[all-rosters.json](../../../workbook/sessions/08-preferences/all-rosters.json)と[request-individual.json](../../../workbook/sessions/08-preferences/request-individual.json)を[roster_io.py](../../../workbook/sessions/08-preferences/roster_io.py)の`read_json`で読める。

### 第一目的を維持する比較

最大違反を最小にした後、その値を保ったまま合計も小さくしたい場合は、二段階に分ける。第一段階の最適値を制約へ移せば、第二段階で目的を切り替えても、最初の改善を失わずに済む。

完成した[individual-core.mzn](../../../workbook/sessions/08-preferences/individual-core.mzn)と[second-stage-start.mzn](../../../workbook/sessions/08-preferences/second-stage-start.mzn)を使う。前者には個人の違反とMの定義まであり、`solve`{.minizinc}はない。[best-worst.dzn](../../../workbook/sessions/08-preferences/best-worst.dzn)に第一段階で確認した値1を入れてある。先に挙げた `metrics-core.mzn`・`roster-core.mzn` も同じフォルダに置き、次の組合せで実行する。

```sh
minizinc --solver gecode second-stage-start.mzn request-individual.dzn best-worst.dzn
```

- **作業1：** `worst`を入力`best_worst`へ固定する。
- **作業2：** 合計`violations`を最小化する。

最適値はM=1を保ったV=4になる。まず合計Vを最小化する順序とは異なることを、各人の違反で説明しよう。第一段階と第二段階では同じ希望入力を使い、入力を変えた場合は最初から最適値を求め直す。

さらに[request-all.dzn](../../../workbook/sessions/08-preferences/request-all.dzn)と[JSON版](../../../workbook/sessions/08-preferences/request-all.json)は、全員が全4日を休み希望にした比較入力である。このときV=8、M=2で一定となる。日数(2,2,2,2,0)と(2,2,2,1,1)を、最大違反だけでは区別できない理由も考えよう。

## 発展3　支配されない候補と重みの限界 {#frontier}

一つの重みで選ぶ前に、二つの指標でどんな選択肢があるかを整理する。同じ指標対の勤務表をまとめ、別の候補に両指標で劣るものを除く。指標の再計算は提供するので、発展1の完成は不要である。

### 条件と列挙結果

5人A〜E、4日間、各日ちょうど2人、一人合計2日以下、勤務可能性0では勤務させない。勤務するなら1、休むなら0で、各欄は1〜4日目の順。希望1の位置で勤務した回数の合計Vと、勤務0日の人も含む全員の日数の最大・最小の差Fを比べる。

| 人 | 勤務可能性 | 休み希望 |
|---|---|---|
| A | 1 1 0 1 | 0 0 0 0 |
| B | 1 0 1 1 | 0 0 0 0 |
| C | 0 1 1 1 | 0 0 0 0 |
| D | 1 1 1 0 | 0 0 0 0 |
| E | 1 1 1 1 | 1 1 1 1 |

[request-demo.json](../../../workbook/sessions/08-preferences/request-demo.json)を使い、V≤kは加えない。[all-rosters.json](../../../workbook/sessions/08-preferences/all-rosters.json)には基本条件を満たすすべての393表を用意した。各表は5行×4列の配列で、行がA〜E、列が日1〜4、各セルは勤務なら1、休みなら0である。再生成方法は手引きにあり、列挙のプログラムを書くことは今回の作業に含めない。

### 同じ値の統合と支配

指標はどちらも小さいほどよい。候補bが候補aに**支配される**とは、aの両指標がb以下で、少なくとも一方が厳密に小さいことである。同じ指標対の別表どうしは、この定義では支配にならない。

[frontier-start.py](../../../workbook/sessions/08-preferences/frontier-start.py)、[metric_values.py](../../../workbook/sessions/08-preferences/metric_values.py)、[roster_io.py](../../../workbook/sessions/08-preferences/roster_io.py)を使う。`values(work, data)`{.python}は基本条件を確認して(V,F)を返す完成関数であり、`work` は勤務表の配列、`data` は `request-demo.json` を読んだ辞書である。Pythonの添字は0から数える。ここでは完成関数の結果を使って候補を整理する。

1. **作業1：** 同じ(V,F)を持つ表をまとめ、指標対ごとに代表表を一つ残す。
2. **作業2：** 他の指標対に支配されるものを除き、`(指標対, 代表表)`のリストを返す。
3. 代表表が元の基本条件を満たし、再計算した指標対と一致することを確かめる。

```sh
python3 frontier-start.py request-demo.json all-rosters.json
```

::: {.hint summary="ヒントを開く：同点と厳密な改善"}
辞書のキーを(V,F)にすれば同じ値をまとめられる。支配の判定には「両方以下」に加え「どちらかが小さい」が必要である。後者を省くと、同点の候補が互いに消えてしまう。
:::

残る指標対は(0,2)と(1,1)である。代表表そのものは複数から選べるので、特定の表との完全一致は求めない。このような支配されない候補をPareto最適な候補と呼ぶ。

### 重みで選べない候補

重みを変えれば支配されない候補をすべて選べるか、別の小例で考える。次の三点は抽象的な二指標の候補であり、上の勤務表から得られた値ではない。この区別を保って比較しよう。

| 候補 | 第一指標 | 第二指標 |
|---|---:|---:|
| X | 0 | 3 |
| Y | 2 | 2 |
| Z | 3 | 0 |

どちらも小さいほどよく、三点とも互いに支配されない。正の重みα・βで第一指標×α+第二指標×βを最小化する。中央YがXとZの両方以下になるための不等式を作り、同時に満たせるか調べる。

::: {.hint summary="ヒントを開く：中央と両端の比較"}
YがX以下なら2α+2β≤3β、YがZ以下なら2α+2β≤3α。整理すると2α≤βかつ2β≤αが必要になる。両方の式とα>0を使うと、どこに矛盾が生じるだろうか。
:::

作った二つの不等式から、正の重みでYを選べるか結論しよう。何通りかの重みを試した結果と、すべての正の重みに対する根拠を区別する。結論を書いてから次の確認例を開く。

::: {.hint summary="確認例を開く：二つの不等式の帰結"}
二つを合わせると4α≤αとなり、α>0に反する。したがってYは支配されていないのに、どの正の重みでも最小にならない。
:::
