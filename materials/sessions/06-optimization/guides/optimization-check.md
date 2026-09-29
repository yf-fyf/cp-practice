# 第06回の最適化の実行と確認

[本文](../lesson.md)／[発展](../advanced-exercises.md)

モデルと入力を同じフォルダーに保存し、Gecodeで実行する。複数ファイルを読み込むモデルは、読み込むファイルも一緒に必要になる。入力が違う結果や、最適化の途中の解を取り違えないようにしよう。

## 配布物と入力

MiniZinc IDEで`.mzn`を開き、Gecodeを選んで実行する。データを尋ねられたら、対応する`.dzn`を指定する。環境が未準備なら授業内で教員と確認し、[公式ダウンロード](https://www.minizinc.org/downloads/)からIDEを含む環境を用意する。

| 作業 | モデル | 入力 |
|---|---|---|
| 4人の割当の復習 | [assignment-base.mzn](../../../../workbook/sessions/06-optimization/assignment-base.mzn) | [base.dzn](../../../../workbook/sessions/06-optimization/base.dzn) |
| 合計の最小化 | [cost-demo.mzn](../../../../workbook/sessions/06-optimization/cost-demo.mzn) | [cost-base.dzn](../../../../workbook/sessions/06-optimization/cost-base.dzn) |
| 必修1 | [cost-start.mzn](../../../../workbook/sessions/06-optimization/cost-start.mzn)を編集 | [cost-practice.dzn](../../../../workbook/sessions/06-optimization/cost-practice.dzn) |
| 個数の短い例 | [quantity-demo.mzn](../../../../workbook/sessions/06-optimization/quantity-demo.mzn) | 不要 |
| 必修2 | [kits-start.mzn](../../../../workbook/sessions/06-optimization/kits-start.mzn)を編集 | [kits.dzn](../../../../workbook/sessions/06-optimization/kits.dzn) |
| 発展用の完成キット | [kits-base.mzn](../../../../workbook/sessions/06-optimization/kits-base.mzn) | kits.dznまたは[kits-lex.dzn](../../../../workbook/sessions/06-optimization/kits-lex.dzn) |
| 全最適な割当 | [optimal-start.mzn](../../../../workbook/sessions/06-optimization/optimal-start.mzn)を編集 | cost-base.dznまたは[cost-zero.dzn](../../../../workbook/sessions/06-optimization/cost-zero.dzn)、[最適値](../../../../workbook/sessions/06-optimization/best-start.dzn) |
| 既知の一解の除外 | [exclude-start.mzn](../../../../workbook/sessions/06-optimization/exclude-start.mzn)を編集 | 不満度入力・最適値・[first.dzn](../../../../workbook/sessions/06-optimization/first.dzn) |
| 二段階法の第二段階 | [lex-start.mzn](../../../../workbook/sessions/06-optimization/lex-start.mzn)を編集 | kits-lex.dzn、最適値 |
| 重み付き法 | [weighted-start.mzn](../../../../workbook/sessions/06-optimization/weighted-start.mzn)を編集 | kits-lex.dzn、[重み](../../../../workbook/sessions/06-optimization/weight-start.dzn) |
| ナップサック | [knapsack-start.mzn](../../../../workbook/sessions/06-optimization/knapsack-start.mzn)を編集 | [容量7](../../../../workbook/sessions/06-optimization/knapsack-7.dzn)／[容量6](../../../../workbook/sessions/06-optimization/knapsack-6.dzn) |
| ケーキ | [cakes-start.mzn](../../../../workbook/sessions/06-optimization/cakes-start.mzn)を編集 | [cakes.dzn](../../../../workbook/sessions/06-optimization/cakes.dzn) |

読み込み用は[assignment-core.mzn](../../../../workbook/sessions/06-optimization/assignment-core.mzn)、[cost-core.mzn](../../../../workbook/sessions/06-optimization/cost-core.mzn)、[kits-core.mzn](../../../../workbook/sessions/06-optimization/kits-core.mzn)。モデル中のincludeが必要とするファイルを揃える。coreには`solve`{.minizinc}がなく、実行する側で問題の種類を指定する。

[MiniZinc Playground](https://play.minizinc.dev/)で一つの入力欄にまとめる場合は、自作ファイルのincludeを、そのファイルの内容で置き換える。さらに読み込むファイルがあれば同様に展開し、最後へ入力データを一度ずつ貼る。変数・入力・`solve`{.minizinc}の二重定義を避ける。

## 終了状態

最適化は「候補が出たこと」と「これよりよい解がないと確認したこと」を区別する。インストールしたMiniZincとGecodeでは、例えば次の実行で割当表・合計5・解の区切り・最適終了の区切りが出る。

```sh
minizinc --solver gecode cost-demo.mzn cost-base.dzn
```

| 表示・状態 | 読み方 |
|---|---|
| `----------` | 一つの解が表示された |
| 最適化の最後の`==========` | 最適性まで確認して終了した |
| `=====UNSATISFIABLE=====` | 条件を満たす解が存在しない |
| `UNKNOWN`・時間切れ・手動停止 | 最適性や解なしが確定したとは限らない |
| 構文エラー・未宣言の名前 | モデルが未完成か、記法・ファイルの組合せに誤りがある |

途中で候補が表示されていれば、その候補の実行可能性と目的値は確認できる。目的値が期待値と同じでも、入力を誤って固定した問題を解いていないかも確かめよう。最適化の途中の候補の列を、すべての最適解として数えない。

## 全最適解と二段階法

最適値を得たら、次のモデルでその値を等式として固定する。充足問題に戻して全解を求めるか、第一目的の値を保ったまま第二目的を最適化する。

```sh
minizinc --solver gecode --all-solutions optimal-start.mzn cost-base.dzn best-start.dzn
minizinc --solver gecode lex-start.mzn kits-lex.dzn best-start.dzn
```

`best-start.dzn`の値は、今扱っている問題の第一段階で確認した最適値へ変更する。不満度とキットでは同じ`best`という名前でも意味が異なる。入力を交換したら第一段階もやり直す。

全解列挙では最後の`==========`まで終了したことを確かめる。この場合の記号は、目的値を固定した充足問題の全解を列挙し終えたことを表す。

## 個数の検査

特定の個数を調べるには、編集したモデルへ一時的な固定制約を加える。例えばu=3、v=3の検査なら次を追加し、`solve`{.minizinc}を`solve satisfy;`{.minizinc}へ置き換える。検査後は元のモデルから再開する。

```minizinc
constraint u = 3;
constraint v = 3;
```

| 個数 | 元のキット条件での意味 |
|---|---|
| 2, 3 | 実行可能、材料7・時間8・得点18 |
| 3, 3 | 材料も時間も9で拒否 |
| 4, 1 | 材料9だけが超過し拒否 |
| 1, 4 | 時間9だけが超過し拒否 |
| 0, 0 | 実行可能だが、元の最適化では最適ではない |
| −1, 0など | 個数の非負性に違反し拒否 |

負数を変数のデータ代入で直接指定すると、定義域外の入力エラーになる場合もある。上のような固定制約で検査した解なしと区別する。端数は整数個数の値にはならない。

ケーキでは`b=3`{.minizinc}・`c=2`{.minizinc}の固定制約を加えると、バターだけが容量を超える。容量制約を削除して解が出るかを調べる場合は、検査用のコピーで行い、通常モデルへ誤った条件を残さない。

## 複数入力をPythonで比較

[lex-general-start.py](../../../../workbook/sessions/06-optimization/lex-general-start.py)と[solve_tools.py](../../../../workbook/sessions/06-optimization/solve_tools.py)を同じフォルダーへ置き、[lex-cases.json](../../../../workbook/sessions/06-optimization/lex-cases.json)を指定する。Python標準ライブラリと、コマンドとして実行できるMiniZincが必要である。

```sh
python3 lex-general-start.py lex-cases.json
```

この実行には同じ発展3で編集した`lex-start.mzn`・`weighted-start.mzn`と、完成した`kits-base.mzn`・`kits-core.mzn`が必要になる。`run`はMiniZincのJSON出力を読み、終了状態と解を返す。`optimum`は最適終了を確認できなければエラーにする。ここでの`_objective`はツールが付ける目的値の欄で、教材の新しい決定変数ではない。

不満度のJSONは[基本](../../../../workbook/sessions/06-optimization/cost-base.json)・[変更](../../../../workbook/sessions/06-optimization/cost-practice.json)・[全0](../../../../workbook/sessions/06-optimization/cost-zero.json)も用意している。各人の不満度をPythonで独立に足す場合に使える。通常のMiniZinc実行では対応する`.dzn`を指定する。
