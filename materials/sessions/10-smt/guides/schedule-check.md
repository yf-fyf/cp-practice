# 第10回の日程と実行の確認

[本文](../lesson.md)／[発展と選択演習](../advanced-exercises.md)で使うファイルと確認方法をまとめる。PythonからZ3を呼ぶ方法は第09回と同じで、今回は整数の開始時刻をモデルから読む。

## 環境と再開用の足場

第09回と同じ環境を使う。用意の手順は[Pythonの環境構築](../../09-sat/guides/python-start.md)にまとめた。第09回で作った環境はそのまま使える。環境準備は授業内に扱い、前の発展の完成を待つ必要はない。pyproject.tomlのあるフォルダーで次を実行し、Z3のバージョンが表示されることを確かめる。

```sh
uv run python -c "import z3; print(z3.get_version_string())"
```

本文とこの手引きの`python3`は、`uv run python`へ読み替える。

[Booleanの小例](../../../../workbook/sessions/10-smt/warmup.py)と[sat_io.py](../../../../workbook/sessions/10-smt/sat_io.py)は第09回と同じものを再配布する。整数のモデルは[integer_io.py](../../../../workbook/sessions/10-smt/integer_io.py)を使う。前者のboolの読み取りを、そのまま整数の値の読み取りに使わない。

## 本文の入力と実行

モデル、JSON入力、共通ファイルを同じフォルダーへ保存し、そこで実行する。所要時間は入力で、出力された開始へ足すと終了になる。モデル内に別の固定時間を残さない。

| 用途 | モデル | 入力 | 期待する判定 |
|---|---|---|---|
| 解説 | [schedule-demo.py](../../../../workbook/sessions/10-smt/schedule-demo.py) | [demo.json](../../../../workbook/sessions/10-smt/demo.json)：時間2,3,2、H=7 | SAT |
| 解説の厳しい期限 | schedule-demo.py | [demo-4.json](../../../../workbook/sessions/10-smt/demo-4.json)：H=4 | UNSAT |
| 最小期限の成立確認 | schedule-demo.py | [demo-5.json](../../../../workbook/sessions/10-smt/demo-5.json)：H=5 | SAT |
| 必修1 | [schedule-start.py](../../../../workbook/sessions/10-smt/schedule-start.py) | [practice.json](../../../../workbook/sessions/10-smt/practice.json)：時間3,2,2、H=7 | SAT |
| 必修2 | [wait-start.py](../../../../workbook/sessions/10-smt/wait-start.py) | [wait-6.json](../../../../workbook/sessions/10-smt/wait-6.json)、[wait-7.json](../../../../workbook/sessions/10-smt/wait-7.json) | H=6はUNSAT、7はSAT |

すべてinteger_io.pyが必要。必修2では、完成した[schedule_base.py](../../../../workbook/sessions/10-smt/schedule_base.py)も保存する。出発ファイルはTODOを記入してから問題の答えとして使う。未記入でもSATになる場合があるが、条件が足りない状態である。

```sh
python3 schedule-demo.py demo.json
python3 schedule-start.py practice.json
python3 wait-start.py wait-6.json
python3 wait-start.py wait-7.json
```

各実行は新しいソルバーを作る。期限6で作ったソルバーへ期限7の制約を継ぎ足すと、以前の厳しい期限が残るため比較にならない。JSONを変更した場合は保存してから再実行する。

## 区間と終了状態

SATの場合は、開始時刻と半開区間を表示する。例えば解説でA=0・B=2・C=2なら、Aは[0,2)、Bは[2,5)、Cは[2,4)。開始0以上、終了が期限以下、先行関係、同じ装置の非重複を順に確認する。

| 確認すること | 見る値・式 |
|---|---|
| 開始の下限 | 開始が0以上か |
| 終了期限 | 開始＋所要時間がH以下か |
| A→B | Aの終了がBの開始以下か |
| A・Cの共有装置 | どちらか一方の終了が他方の開始以下か |
| 必修2のC→B | Cの終了がBの開始以下か |

UNSATでは日程を表示せず、UNKNOWNでは理由を表示する。UNKNOWNや途中で止めた実行を、解なしや最適性の証明へ読み替えない。この回の通常モデルは充足問題なので、SATの表示自体は最短化を意味しない。

## 必修2の下限

自分で必要時間を説明してから、この確認例と照合する。式の実装と二つの期限の実行は、本文の作業を先に使う。

::: {.hint summary="確認例を開く：装置の時間と先行関係"}
AとCは同じ装置で合計5時間、その両方の後にBが2時間必要になる。開始が0以上なので、全体の完了を7より前にすることはできない。期限7の成立例と、この下限を合わせて期限6の解なしを説明できる。
:::

## 固定した開始の検査

[schedule-checks.json](../../../../workbook/sessions/10-smt/schedule-checks.json)には、端点での接触、途中の重なり、先行違反、期限超過、負の開始の確認例がある。`start`はA・B・Cの順で、`valid`はその入力と対応モデルについての期待である。

必修1では、編集した`schedule-start.py`と配布の`schedule-checks.json`、`demo.json`、`practice.json`、`integer_io.py`を同じフォルダーへ置く。次のコマンドは自分のモデルに固定値を追加して7件を確認する。すべてPASS、最後に`7 checks, 0 failures`なら期待と一致する。FAILならその入力と条件を読み返す。

```sh
python3 schedule-start.py --check
```

検査ではJSONの`model`が`basic`の行を使う。`wait`の行はC→Bを含む必修2用なので除く。`--check`と入力ファイル名は同時に指定しない。UNKNOWNは期待したUNSATとは扱わず失敗として表示する。

個別に調べる場合、完成したモデルをコピーし、`build(data)`{.python}の後、判定前に次を追加すると、指定した日程が許されるかを調べられる。開始変数そのものをPythonの整数で上書きせず、追加制約で固定する。

```python
s, starts = build(data)
s.add(starts['A'] == 0, starts['B'] == 2, starts['C'] == 1)
report_schedule(s, starts, data)
```

この例は解説の時間2,3,2に対して、A・Cの途中の重なりだけを破りUNSATとなる。A=0・B=2・C=2へ変えるとSAT。必修2用の行はwait-start.pyの完成モデルで調べる。入力だけでなく、C→Bを含むモデルかどうかも対応させる。

## 発展1と発展2

発展1は[deadline-start.py](../../../../workbook/sessions/10-smt/deadline-start.py)、schedule_base.py、integer_io.pyを使う。期限を受ける`at_deadline`は完成しており、SATの辞書・UNSATのNone・判定未完了の例外を区別する。

発展2は[machines-start.py](../../../../workbook/sessions/10-smt/machines-start.py)、integer_io.py、[machines-5.json](../../../../workbook/sessions/10-smt/machines-5.json)・[machines-6.json](../../../../workbook/sessions/10-smt/machines-6.json)を使う。sAなどは開始、mAなどは装置番号で、開始値と装置番号を一つの尺度で比べない。

```sh
python3 deadline-start.py
python3 machines-start.py machines-5.json
python3 machines-start.py machines-6.json
```

実行結果を記録してから、次の確認例と照合する。

::: {.hint summary="確認例を開く：最小期限と装置の選択"}
発展1の最小期限は5で、開始(A,B,C)=(0,2,2)が成立する。期限4ではA→Bだけでも間に合わない。発展2は期限5でUNSAT、6でSATとなる。期限6では、開始(0,0,3)、装置(1,2,1)のように、別装置の作業を同時に始められる。
:::

## 一般の日程と比較器

発展3は[jobshop-start.py](../../../../workbook/sessions/10-smt/jobshop-start.py)、[jobshop_tools.py](../../../../workbook/sessions/10-smt/jobshop_tools.py)、integer_io.pyを使う。[jobshop.json](../../../../workbook/sessions/10-smt/jobshop.json)と[jobshop-long.json](../../../../workbook/sessions/10-smt/jobshop-long.json)でモデルと検査器を確認してから、[jobshop-compare.py](../../../../workbook/sessions/10-smt/jobshop-compare.py)と[jobshop-cases.json](../../../../workbook/sessions/10-smt/jobshop-cases.json)で全解集合を比較する。

```sh
python3 jobshop-start.py jobshop.json
python3 jobshop-start.py jobshop-long.json
python3 jobshop-compare.py jobshop-start.py
```

比較器は、自作のモデルと独立検査器を読み込む足場である。検査器は名前→整数開始の辞書を受け取り、範囲・先行・時刻ごとの使用数を確認する。入力八件の全解数は順に3・9・0・0・1・0・0・9。

作業が一つもない入力では、空の日程一つが成立する。先行の循環は形式エラーではなく、正の所要時間を持つ作業が互いに先に終わることを要求するためUNSATとなる。固定のA〜Dや装置1〜2しか扱えない実装になっていないかも確かめる。

両実装に同じ誤りがあれば一致することがあるので、既知の成立例・拒否例と解数も照合する。有限列挙の範囲外まで一般の正しさが確認できたという意味ではない。半開区間と整数の単位時間が対応する理由は、発展本文で説明する。

## 席順と覆面算

席順には[seats-start.py](../../../../workbook/sessions/10-smt/seats-start.py)とinteger_io.py、覆面算には[send-more-start.py](../../../../workbook/sessions/10-smt/send-more-start.py)とinteger_io.pyを使う。どちらも入力条件は出発ファイルと発展本文にある。

[seats-checks.json](../../../../workbook/sessions/10-smt/seats-checks.json)の`position`はA・B・C・Dの順、[send-checks.json](../../../../workbook/sessions/10-smt/send-checks.json)の`digits`はS・E・N・D・M・O・R・Yの順である。固定する場合は、各変数と確認値の等式を判定前に追加する。

席順ではA・Bの逆向きも許し、位置(4,2,1,3)は隣接していないので拒否する。覆面算では9567+1085=10652を受理し、先頭ゼロ・異なる文字の数字の重複をそれぞれ拒否する。判定後の整数の表示と、元の条件の照合を分けて行おう。
