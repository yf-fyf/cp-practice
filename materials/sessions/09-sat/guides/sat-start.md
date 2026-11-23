# Z3の実行の手引き

[本文](../lesson.md)／[発展と選択演習](../advanced-exercises.md)で使うPython環境、ファイル、判定結果を確認する。準備は授業内で扱い、前の回の発展や授業外のインストール作業を前提にしない。

## PythonとZ3の確認

環境の用意は[Pythonの環境構築](python-start.md)にまとめた。pyproject.tomlのあるフォルダーで次を実行し、Z3のバージョンが表示されることを確かめる。

```sh
uv run python -c "import z3; print(z3.get_version_string())"
```

本文とこの手引きの`python3`は、`uv run python`へ読み替える。

## 本文のファイルと実行

必要なファイルを同じフォルダーへ保存し、そのフォルダーでコマンドを実行する。`sat_io.py`が判定・代入の表示を、`features_base.py`が必修1の完成した条件を提供する。

| 用途 | ファイル | 実行例 |
|---|---|---|
| 二変数の操作例 | [warmup.py](../../../../workbook/sessions/09-sat/warmup.py)、[sat_io.py](../../../../workbook/sessions/09-sat/sat_io.py) | `python3 warmup.py` |
| 四機能の解説例 | [features-demo.py](../../../../workbook/sessions/09-sat/features-demo.py)、sat_io.py | `python3 features-demo.py` |
| 必修1 | [features-start.py](../../../../workbook/sessions/09-sat/features-start.py)、sat_io.py | `python3 features-start.py` |
| 必修2 | [exclusive-start.py](../../../../workbook/sessions/09-sat/exclusive-start.py)、[features_base.py](../../../../workbook/sessions/09-sat/features_base.py)、sat_io.py | `python3 exclusive-start.py` |

解説例の`--case with-D`はD必須を加え、`--case without-A`は最初のA必須だけを外す。通常はA・B・CがTrue、DがFalse。Dも必須ならUNSAT、A必須を外すと全偽も選択肢に含まれる。

必修の出発ファイルは、TODO未記入でも実行できるが、必要な制約が足りない。実行できたことと、条件をすべて書けたことを区別する。保存せずに実行して古い内容を読んでいないかも確認しよう。

## 必修1の固定検査

編集した`features-start.py`に`--case A-false`、`--case A-without-B`、`--case E-without-C`を付けて別々に実行する。期待は順にSAT、UNSAT、UNSAT。固定値と検査の意味は[本文の必修1](../lesson.md#演習)にある。自分の`build()`{.python}が作る条件を検査するので、完成した別モデルに切り替えない。

## 判定と出力の意味

SATの場合だけ、`model()`{.python}から得た代入を読む。配布の表示処理は、名前と真偽を一行ずつ出す。変数の順や、一つの解の選ばれ方が違っても、元の条件を満たせばよい。

| 表示 | 意味 | 次に読むもの |
|---|---|---|
| SAT | 充足代入がある | 表示された値と元の条件 |
| UNSAT | 全条件を満たす代入がない | 衝突している条件 |
| UNKNOWN | 判定できなかった | 表示された理由。解なしとは扱わない |

`check()`{.python}でSATを確認する前や、UNSAT・UNKNOWNの場合には、SATの代入として`model()`{.python}を読まない。Pythonの例外が出た場合は、判定結果ではなくプログラムや実行環境の問題としてメッセージを読む。

未定のBoolean式を`if A:`{.python}で分岐させず、式を`And`・`Or`・`Not`・`Implies`で作る。配布の`if result == sat:`{.python}は、判定済みの結果を区別する処理なので、この禁止とは異なる。

## 必修2の固定値の検査

二つの固定は別々の実行で行う。`fix_pair`は、通常の必修2モデルへAとFの値を追加する。`both-true`と`both-false`を同じソルバーへ続けて加えない。

```sh
python3 exclusive-start.py
python3 exclusive-start.py --case both-true
python3 exclusive-start.py --case both-false
```

| AとFに追加した条件 | 通常の解数 | 両方真に固定 | 両方偽に固定 |
|---|---:|---|---|
| 少なくとも一方、両方不可 | 3 | UNSAT | UNSAT |
| 少なくとも一方だけ | 4 | SAT | UNSAT |
| 両方不可だけ | 5 | UNSAT | SAT |

固定した真理値表の二行だけでなく、通常の問題がSATであることも確認する。矛盾する条件を誤って加えると、どんな固定でもUNSATになるからである。必修で全解数を数える必要はなく、この表は条件漏れを切り分けるために使える。

## 発展のファイル

発展1・2はZ3を使い、発展3はPython標準ライブラリだけで動く。新しい出発ファイルと必要な共通部分を保存し、前の発展を完成させずに選べる。

| 発展 | 出発ファイル | 共通部分 |
|---|---|---|
| 多数から一つ | [one-start.py](../../../../workbook/sessions/09-sat/one-start.py) | sat_io.py |
| 全代入の列挙 | [enumerate-start.py](../../../../workbook/sessions/09-sat/enumerate-start.py) | features_base.py、sat_io.py |
| 学習用SATソルバー | [dpll-start.py](../../../../workbook/sessions/09-sat/dpll-start.py) | [cnf_tools.py](../../../../workbook/sessions/09-sat/cnf_tools.py)、JSON入力 |
| 学習用ソルバーの比較 | [cnf-compare.py](../../../../workbook/sessions/09-sat/cnf-compare.py) | cnf_tools.py、自分で完成させたdpll-start.py |

`read_values`は、指定された全変数を`model.evaluate(..., model_completion=True)`{.python}で読む。モデルで省略されていた変数にも一例の値を与える処理であり、その値を新しい制約として追加したり、唯一の値と判定したりする操作ではない。

列挙では読み取った一代入だけを除き、UNSATになったときに全列挙完了とする。UNKNOWNなら途中の結果があっても、全解が揃ったと表示しない。

## 学習用SATソルバーの入力

JSONの`n`が変数数、`clauses`が節のリスト。正の整数はその変数、負は否定を表し、0は使わない。戻り値は全変数を含むboolの辞書か、UNSATの`None`である。

| 入力 | 主に確認すること | 期待 |
|---|---|---|
| [cnf-empty.json](../../../../workbook/sessions/09-sat/cnf-empty.json) | 0変数、節なし | SAT、空辞書 |
| [cnf-empty-clause.json](../../../../workbook/sessions/09-sat/cnf-empty-clause.json) | 空の節が一つ | UNSAT |
| [cnf-unit.json](../../../../workbook/sessions/09-sat/cnf-unit.json) | 単位伝播の連鎖 | SAT、1〜3が真 |
| [cnf-conflict.json](../../../../workbook/sessions/09-sat/cnf-conflict.json) | 相反する単位節 | UNSAT |
| [cnf-restore.json](../../../../workbook/sessions/09-sat/cnf-restore.json) | 最初の枝からの復元 | SAT、変数1が真、2はどちらでもよい |
| [cnf-branch-unsat.json](../../../../workbook/sessions/09-sat/cnf-branch-unsat.json) | 両枝の失敗 | UNSAT |
| [cnf-unused.json](../../../../workbook/sessions/09-sat/cnf-unused.json) | 式にない変数の補完 | SAT、変数1は真、2・3は任意 |
| [cnf-tautology.json](../../../../workbook/sessions/09-sat/cnf-tautology.json) | 恒真節と重複リテラル | SAT、変数2は真 |
| [cnf-free.json](../../../../workbook/sessions/09-sat/cnf-free.json) | 二変数だが条件なし | SAT、二変数を含む任意の代入 |

小例を確認してから`python3 cnf-compare.py dpll-start.py`を実行すると、独立した真理値表と比較する。二変数512式、三変数で三節以下3304式を通過すると`PASS {2: 512, 3: 3304}`を表示する。判定・返した代入・入力を壊していないことを確認する。

比較器の例外には、最初に不一致を見つけた変数数・節・返り値を表示する。無限ループしている場合は実行を中断し、伝播や分岐で未定変数が減っているか、同じ状態へ戻り続けていないかを調べる。

## 選択演習のファイル

配色には[color-start.py](../../../../workbook/sessions/09-sat/color-start.py)、[australia.json](../../../../workbook/sessions/09-sat/australia.json)、[color-checks.json](../../../../workbook/sessions/09-sat/color-checks.json)、sat_io.pyを使う。全色が偽の固定と、Tだけ赤・緑を選ぶ固定を別々に試す。

```sh
python3 color-start.py
python3 color-start.py --case all-false
python3 color-start.py --case T-two
```

正しいモデルでは通常がSAT、二つの固定がUNSATとなる。`--case valid`は有効な一配色の固定でSATになる。二色を試す場合はaustralia.jsonをコピーして`colors`を二色へ変更し、`python3 color-start.py コピーした入力.json`で実行する。

MaxSATは[maxsat-work.md](../../../../workbook/sessions/09-sat/maxsat-work.md)の表を手で埋めてもよい。Pythonで確認する場合は[maxsat-start.py](../../../../workbook/sessions/09-sat/maxsat-start.py)を使う。これは通常のboolに対する真理値表なのでZ3は不要で、記号式とPythonの真偽値を混ぜない。
