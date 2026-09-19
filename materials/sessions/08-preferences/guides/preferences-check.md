# 第08回の入力と結果の確認

[本文](../lesson.md)／[発展](../advanced-exercises.md)で使うファイルの組をまとめる。基本条件、希望、上限、目的を一つずつ確認してから実行する。入力を切り替える場合は、古い入力を同時に残さない。

## 本文のモデルと入力

ファイルを同じ作業フォルダーへ保存する。MiniZinc IDEではモデルを開き、表の入力ファイルを選び、ソルバーをGecodeにする。コマンドを使う場合は、そのフォルダーで次のように実行できる。

| 用途 | モデル | データ | 希望・上限・目的 |
|---|---|---|---|
| 第07回からの再開 | [roster-basic.mzn](../../../../workbook/sessions/08-preferences/roster-basic.mzn) | [practice.dzn](../../../../workbook/sessions/08-preferences/practice.dzn) | 技能なし、希望なし、充足 |
| 解説 | [weighted-demo.mzn](../../../../workbook/sessions/08-preferences/weighted-demo.mzn) | [request-demo.dzn](../../../../workbook/sessions/08-preferences/request-demo.dzn)と重み一つ | E全日、上限なし、J最小 |
| 必修1 | [weighted-start.mzn](../../../../workbook/sessions/08-preferences/weighted-start.mzn) | [request-practice.dzn](../../../../workbook/sessions/08-preferences/request-practice.dzn)と[weights-12.dzn](../../../../workbook/sessions/08-preferences/weights-12.dzn) | Eの4日目、上限なし、J最小 |
| 必修2 | [capped-start.mzn](../../../../workbook/sessions/08-preferences/capped-start.mzn) | request-demo.dznと上限一つ | E全日、V≤k、F最小 |

重みは[weights-10.dzn](../../../../workbook/sessions/08-preferences/weights-10.dzn)が(1,0)、[weights-11.dzn](../../../../workbook/sessions/08-preferences/weights-11.dzn)が(1,1)、weights-12.dznが(1,2)。上限は[cap-0.dzn](../../../../workbook/sessions/08-preferences/cap-0.dzn)がk=0、[cap-1.dzn](../../../../workbook/sessions/08-preferences/cap-1.dzn)がk=1である。

共通ファイルの[roster-core.mzn](../../../../workbook/sessions/08-preferences/roster-core.mzn)には基本勤務条件、[metrics-core.mzn](../../../../workbook/sessions/08-preferences/metrics-core.mzn)にはその読み込みとV・日数・Fがある。解説と必修2では両方、必修1ではroster-core.mznを同じ場所へ置く。共通ファイル単体を実行するのではなく、用途欄のモデルを実行する。

```sh
minizinc --solver gecode weighted-demo.mzn request-demo.dzn weights-12.dzn
minizinc --solver gecode weighted-start.mzn request-practice.dzn weights-12.dzn
minizinc --solver gecode capped-start.mzn request-demo.dzn cap-0.dzn
minizinc --solver gecode capped-start.mzn request-demo.dzn cap-1.dzn
```

`start`はTODOを記入してから実行する。必修1は出力で使う変数も未定義なので、入力を選ぶだけでは実行できない。`request-*.dzn`には基本勤務データも入っており、practice.dznを重ねて指定する必要はない。

## 表と目的値の照合

出力には人名付きの勤務表、日数配列`load`、V・F、重み付きの場合はJが出る。まず各日の人数と勤務可能性、一人の日数上限を確かめる。次に希望1の位置で勤務した数と、全員の日数の差を再計算する。

| 入力・目的 | 最適値 | 最適な(V,F) |
|---|---:|---|
| E全日、重み(1,0) | J=0 | (0,2) |
| E全日、重み(1,1) | J=2 | (0,2)または(1,1) |
| E全日、重み(1,2) | J=3 | (1,1) |
| Eの4日目、重み(1,2) | J=2 | (0,1) |
| E全日、k=0でF最小 | F=2 | (0,2) |
| E全日、k=1でF最小 | F=1 | (1,1) |

別の勤務表でも条件と最適値が合えばよい。解の区切り`----------`だけで判断せず、最適化では最後の`==========`まで確認する。`UNSATISFIABLE`は解なしで、停止や`UNKNOWN`は判定未完了である。途中に候補が出ていても最適性を確認済みとは扱わない。

上限だけの受理・拒否を試すときは、必修2の完成モデルをコピーし、`solve`{.minizinc}を`solve satisfy;`{.minizinc}に切り替える。次の制約でS1（AB／AC／BD／CE）を固定すると、k=0では解なし、k=1では受理される。表の値をデータとして二重定義せず、追加制約として固定する。

```minizinc
constraint work = [| 1,1,0,0
                  | 1,0,1,0
                  | 0,1,0,1
                  | 0,0,1,0
                  | 0,0,0,1 |];
```

S0（AB／AD／CD／BC）を同じ方法で固定すれば、k=0でもk=1でも実行可能である。k=1におけるS0のF=2は最適ではないが、表を固定して解があるかだけを調べる検査では受理する。

## Pythonの配列を使う発展

Python 3の標準ライブラリで実行でき、追加パッケージは不要である。[roster_io.py](../../../../workbook/sessions/08-preferences/roster_io.py)がJSONの読み込みと基本条件の確認を提供する。`available`と`request`は人×日、`required`は日ごとの人数、`max_days`は人ごとの上限である。

| 用途 | 出発ファイルと共通部分 | 入力 |
|---|---|---|
| 発展1 | [recalculate-start.py](../../../../workbook/sessions/08-preferences/recalculate-start.py)、roster_io.py | [request-demo.json](../../../../workbook/sessions/08-preferences/request-demo.json)または[request-practice.json](../../../../workbook/sessions/08-preferences/request-practice.json)、[examples.json](../../../../workbook/sessions/08-preferences/examples.json) |
| 発展3 | [frontier-start.py](../../../../workbook/sessions/08-preferences/frontier-start.py)、[metric_values.py](../../../../workbook/sessions/08-preferences/metric_values.py)、roster_io.py | request-demo.json、[all-rosters.json](../../../../workbook/sessions/08-preferences/all-rosters.json) |

examples.jsonは`name`と`work`を持つ項目のリスト。S0・S1・P1に加え、発展2のI-sum・I-maxも含む。all-rosters.jsonは勤務表そのもののリストで、形式が異なる。出発ファイルは用途に合う方を読み込む。

発展1の戻り値は、例えば元の希望のS0、k=0なら次の形になる。`valid`は基本条件と指定された上限の成否であり、最適性の判定結果ではない。基本検査に失敗した場合は`valid`と`errors`のみを返す。

```python
{'valid': True, 'errors': [], 'load': [2, 2, 2, 2, 0], 'V': 0, 'F': 2}
```

Pythonの添字は0からで、Aは行0、1日目は列0に当たる。各人の日数を求める際に、値が0の行を除外しない。上限k=0も検査するため、未指定の`None`と0を区別する。

## 個人の違反を比較する発展

発展2では[individual-start.mzn](../../../../workbook/sessions/08-preferences/individual-start.mzn)へ個人の違反とMを定義し、合計Vと最大Mの最小化を別々に実行する。metrics-core.mznとroster-core.mznも同じ場所へ置く。

[request-individual.dzn](../../../../workbook/sessions/08-preferences/request-individual.dzn)が比較用の希望、[request-all.dzn](../../../../workbook/sessions/08-preferences/request-all.dzn)が全員全日の希望である。独立な配列計算には[request-individual.json](../../../../workbook/sessions/08-preferences/request-individual.json)と[request-all.json](../../../../workbook/sessions/08-preferences/request-all.json)を使える。

第一目的を保って合計を小さくする段階では、完成した[individual-core.mzn](../../../../workbook/sessions/08-preferences/individual-core.mzn)、[second-stage-start.mzn](../../../../workbook/sessions/08-preferences/second-stage-start.mzn)、[best-worst.dzn](../../../../workbook/sessions/08-preferences/best-worst.dzn)を使う。共通ファイルには`solve`{.minizinc}を置かず、実行モデルへ一つだけ書く。

```sh
minizinc --solver gecode individual-start.mzn request-individual.dzn
minizinc --solver gecode second-stage-start.mzn request-individual.dzn best-worst.dzn
```

比較用の希望では最小V=3、その場合のMは2。最小M=1の表にはV=4とV=5の両方があり、M=1を固定してVを最小にするとV=4となる。全員全日希望ならV=8・M=2で一定になる。

## 全勤務表の出所

all-rosters.jsonは、[enumerate.mzn](../../../../workbook/sessions/08-preferences/enumerate.mzn)・roster-core.mzn・practice.dznによる基本条件の全解を、日ごとの組合せ列挙とも照合した393表である。希望、V≤k、技能、周期の条件を含まない。発展2・3ではこのファイルをそのまま読めばよい。

MiniZinc側の列挙を自分で確認する場合は、次を使う。JSON streamには解だけでなく終了状態などの行も出るため、これをそのままall-rosters.jsonへ名前変更して読み込まない。

```sh
minizinc --solver gecode --all-solutions --json-stream --output-mode json enumerate.mzn practice.dzn
```

再生成する場合は、`type`が`solution`の各行から`output.json.work`を集め、最後が`ALL_SOLUTIONS`であることを確認して、勤務表のリストをJSONとして保存する。途中で止めた列挙結果だけで、候補がすべて揃ったとはしない。
