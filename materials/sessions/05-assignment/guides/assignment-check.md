# 第05回の実行と割当の確認

[本文](../lesson.md)／[発展](../advanced-exercises.md)

配布モデルと入力を同じフォルダーへ保存し、編集したモデルを実行する。入力は一度に一組を指定する。普通の入力と、特定の割当表を固定する確認入力の違いを先に確かめよう。

## モデルと入力

MiniZinc IDEではモデルの`.mzn`を開き、Gecodeを選んで実行する。入力を求められたら対応する`.dzn`を指定する。未準備なら授業内で教員と確認し、[公式ダウンロード](https://www.minizinc.org/downloads/)からIDEを含む環境を用意する。

| 作業 | モデル | 通常入力 |
|---|---|---|
| 解説例 | [assignment-base.mzn](../../../../workbook/sessions/05-assignment/assignment-base.mzn) | [base.dzn](../../../../workbook/sessions/05-assignment/base.dzn) |
| 空席の確認 | 同上 | [roomy.dzn](../../../../workbook/sessions/05-assignment/roomy.dzn) |
| 必修1 | [practice-start.mzn](../../../../workbook/sessions/05-assignment/practice-start.mzn)を編集 | [practice.dzn](../../../../workbook/sessions/05-assignment/practice.dzn) |
| 必修2 | [open-start.mzn](../../../../workbook/sessions/05-assignment/open-start.mzn)を編集 | [open.dzn](../../../../workbook/sessions/05-assignment/open.dzn) |
| 発展1 | [value-start.mzn](../../../../workbook/sessions/05-assignment/value-start.mzn)を編集 | practice.dzn |
| 発展2 | [separate-start.mzn](../../../../workbook/sessions/05-assignment/separate-start.mzn)を編集 | practice.dzn |
| 発展3の割当検査 | assignment-base.mzn | [impossible.dzn](../../../../workbook/sessions/05-assignment/impossible.dzn)／[repaired.dzn](../../../../workbook/sessions/05-assignment/repaired.dzn) |
| 選択M05 | [series-start.mzn](../../../../workbook/sessions/05-assignment/series-start.mzn)を編集 | [series.dzn](../../../../workbook/sessions/05-assignment/series.dzn) |

必修2・発展2は`assignment-base.mzn`を読み込むため、このファイルも同じフォルダーへ保存する。基本モデルは完成済みなので、前の演習の完成を待つ必要はない。`solve`{.minizinc}の指定を追加して二重にしない。

コマンドを使う場合は、配布物のフォルダーで次のように実行する。入力が変わったら、古い結果を見ていないかも確認しよう。

```sh
minizinc --solver gecode assignment-base.mzn base.dzn
minizinc --solver gecode open-start.mzn open.dzn
```

[MiniZinc Playground](https://play.minizinc.dev/)でも試せる。モデルの後へ入力を一度だけ貼り、自作ファイルの`include "assignment-base.mzn";`{.minizinc}は、そのファイルの本文へ置き換える。標準ライブラリのincludeを使う問題では、その行は残す。

## 全解と終了状態

解が一つ表示されたら、その割当を条件と照合する。`----------`は一解の区切りであり、唯一の答えだとは限らない。全解を求める場合は`--all-solutions`を付ける。

```sh
minizinc --solver gecode --all-solutions assignment-base.mzn practice.dzn
```

完全に列挙した場合は最後に`==========`が出る。解が存在しない場合は`=====UNSATISFIABLE=====`になる。時間切れ・手動停止・`UNKNOWN`・構文エラーは解なしと区別する。

## 表を固定する確認入力

次の入力には許可・定員に加えて`x`の値も入っている。参加先を自由に選ぶ代わりに、その表が条件を満たすかを検査する。通常入力へ足すのではなく、入力全体を交換する。

| 入力 | 使うモデル | 正しい結果・検査の狙い |
|---|---|---|
| [正しい5人の表](../../../../workbook/sessions/05-assignment/check-valid.dzn) | 必修1・発展2 | 受理。参加先1・1・2・2・3 |
| [未割当](../../../../workbook/sessions/05-assignment/check-unassigned.dzn) | 必修1 | 拒否。一人の行がすべて0 |
| [二重割当](../../../../workbook/sessions/05-assignment/check-double.dzn) | 基本・必修1 | 拒否。一人の行に1が二つ。定員は別の入力 |
| [定員超過](../../../../workbook/sessions/05-assignment/check-capacity.dzn) | 必修1 | 拒否。講座1が3人で定員2を超える |
| [禁止選択](../../../../workbook/sessions/05-assignment/check-forbidden.dzn) | 必修1 | 拒否。Eが許可されない講座2へ参加 |
| [空席あり](../../../../workbook/sessions/05-assignment/check-empty-seat.dzn) | 基本・必修1 | 受理。4人・定員3・2・1の入力 |
| [AとDが同じ](../../../../workbook/sessions/05-assignment/check-same.dzn) | 発展2 | 拒否。基本モデルなら受理する |
| [開催の正例](../../../../workbook/sessions/05-assignment/check-open-valid.dzn) | 必修2 | 受理。人数3・0・2、開催1・0・1 |
| [1人だけの講座](../../../../workbook/sessions/05-assignment/check-open-single.dzn) | 必修2 | 拒否。人数3・1・1 |
| [非開催に人がいる](../../../../workbook/sessions/05-assignment/check-open-missing.dzn) | 必修2 | 拒否。割当と開催フラグの不整合 |
| [空なのに開催](../../../../workbook/sessions/05-assignment/check-open-empty.dzn) | 必修2 | 拒否。開催講座の人数不足 |
| [数列の反例](../../../../workbook/sessions/05-assignment/series-wrong.dzn) | 選択M05 | 拒否。(1,1,1,1)は出現回数と一致しない |

発展1は変数が`y`なので、`x`を固定する確認入力をそのまま使わない。同じ参加先を講座番号へ変換し、`y`のリストとして固定するか、全解を求めて0/1表へ変換して比べる。

## 障害集合のPython

[obstruction-start.py](../../../../workbook/sessions/05-assignment/obstruction-start.py)は標準ライブラリだけを使う。TODOを埋め、[impossible.json](../../../../workbook/sessions/05-assignment/impossible.json)または[repaired.json](../../../../workbook/sessions/05-assignment/repaired.json)を指定する。未実装なら`NotImplementedError`で止まる。

```sh
python3 obstruction-start.py impossible.json
```

表示される人・講座番号は1始まり、コード内の添字は0始まりである。人の集合・利用できる講座・人数・定員総和を確認する。同じ内容の`.dzn`を基本モデルで解き、説明した不可能性と結果を比べられる。

別入力として[4人基本](../../../../workbook/sessions/05-assignment/base.json)、[空席あり](../../../../workbook/sessions/05-assignment/roomy.json)、[5人](../../../../workbook/sessions/05-assignment/practice.json)、[各定員3人](../../../../workbook/sessions/05-assignment/open.json)のJSONも使える。障害集合の検査が対象とするのは一人一講座・許可・定員であり、開催や分離の追加条件はJSONに含めていない。
