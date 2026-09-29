# 第04回の実行と確認

[本文](../lesson.md)／[発展](../advanced-exercises.md)／[配布ZIP](../../../../workbook/sessions/04-rules/session-04.zip)

モデルを直した後は、そのモデルと入力の組を確認して実行する。同じファイル名を別のフォルダーで編集していないかにも注意しよう。出発ファイルのTODOは未完成部分であり、そのまま実行できても必要な条件はまだ揃っていない。

## モデルと入力の指定

MiniZinc IDEではモデルの `.mzn` を開き、Gecodeを選んで実行する。入力を尋ねられたら対応する `.dzn` を選ぶ。ZIPを展開し、複数ファイルを同じフォルダーに置いておく。環境が未準備なら授業内で教員と確認し、[MiniZinc公式ダウンロード](https://www.minizinc.org/downloads/)からIDEを含む環境を用意する。

ブラウザで試す場合は[MiniZinc Playground](https://play.minizinc.dev/)を使える。最初は[一ファイルの解説例](../../../../workbook/sessions/04-rules/sum-demo-inline.mzn)を貼り付ける。標準ライブラリの `include "alldifferent.mzn";`{.minizinc} は残す。標準ライブラリ以外のファイルを読み込む発展2では、`include "multi-base.mzn";`{.minizinc}を配布の`multi-base.mzn`の中身へ置き換え、入力を末尾へ一度だけ貼る。

| 作業 | モデル | 入力 |
|---|---|---|
| 解説例 | sum-demo.mzn | demo.dzn、またはP-demo系の一つ |
| 必修1 | 編集したsum-start.mzn | practice.dzn、またはP-practice系の一つ |
| 必修2 | 編集したdesign-start.mzn | P.dzn／Q.dzn／empty.dznのいずれか |
| 発展1 | 編集したmulti-start.mzn | two-clues.dzn、またはM系の一つ |
| 発展2 | 編集したsecond-start.mzn | two-clues.dznとfirst.dzn、またはU系の一つ |
| 発展3 | multi-base.mzn | candidate-clues.dzn、または自作selected.dzn |
| 選択M04 | 編集したsend-more-start.mzn | 最初はなし。検査時はsend系の一つ |

必修2の`clue_total`{.minizinc}はモデル内で定義する。そこへ`practice.dzn`など合計値も含む入力を渡すと二重定義になる。発展2のU系入力は`first`も含むので、さらに`first.dzn`を指定しない。

コマンドを使う場合は、配布物のフォルダーで次のように実行する。複数の入力に分けてある発展2では、ヒントと`first`を一度ずつ指定する。

```sh
minizinc --solver gecode sum-demo.mzn demo.dzn
minizinc --solver gecode second-start.mzn two-clues.dzn first.dzn
```

## 結果と終了状態

盤面が出たら、その数字を問題文の条件と照合する。出力の区切り`----------`は一つの解の終わりであり、その時点では唯一の解とは限らない。解の出る順序は処理系により変わる。

全解を調べるときは`--all-solutions`を付ける。完全に列挙し終えた場合は最後に`==========`が出る。IDEでも全解を求める設定を選べる。固定した入力で解なしの場合は`=====UNSATISFIABLE=====`となる。

```sh
minizinc --solver gecode --all-solutions sum-demo.mzn demo.dzn
```

`UNKNOWN`、時間切れ、手動停止、構文エラーは、解なしの証拠ではない。一意性を調べる場合は、元の解を受理できたことに加え、その解だけを除いたモデルが解なしで終了したことを確認する。

## 固定盤面と指定合計

解説例と必修1では、Pを固定したまま指定合計を変える検査と、指定合計を固定して盤面を変える検査の両方を使える。いずれも同じモデルを調べ、別の問題を解く検査と混同しない。

| 問題 | Pを受理する入力 | 拒否する入力 |
|---|---|---|
| 解説例 | [合計6](../../../../workbook/sessions/04-rules/P-demo.dzn) | [合計5](../../../../workbook/sessions/04-rules/P-demo-low.dzn)、[合計7](../../../../workbook/sessions/04-rules/P-demo-high.dzn) |
| 必修1 | [合計9](../../../../workbook/sessions/04-rules/P-practice.dzn) | [合計8](../../../../workbook/sessions/04-rules/P-practice-low.dzn)、[合計10](../../../../workbook/sessions/04-rules/P-practice-high.dzn) |

次の表は、別の固定盤面や複数ヒントも含む確認入力である。0解は解なし、1解以上なら条件を満たす出力がある。期待出力のテキストは一例なので、複数解の入力ではその盤面との文字列一致を求めない。`checks/` の期待出力（`.expected.txt`）は盤面の数字だけを示し、MiniZincが表示する行末の空白と区切り線 `----------` は省いている。

| 入力 | 対応 | 解数 | 調べること |
|---|---|---:|---|
| [D-open](../../../../workbook/sessions/04-rules/checks/D-open.dzn) | demo | 48 | 空欄のある盤面を解く |
| [D-ok](../../../../workbook/sessions/04-rules/checks/D-ok.dzn) | demo | 1 | 通るべき完成盤面を受け入れる |
| [D-low](../../../../workbook/sessions/04-rules/checks/D-low.dzn) | demo | 0 | 指定合計より小さい完成盤面を拒否する |
| [D-high](../../../../workbook/sessions/04-rules/checks/D-high.dzn) | demo | 0 | 指定合計より大きい完成盤面を拒否する |
| [R-open](../../../../workbook/sessions/04-rules/checks/R-open.dzn) | required-1 | 60 | 空欄のある盤面を解く |
| [R-ok](../../../../workbook/sessions/04-rules/checks/R-ok.dzn) | required-1 | 1 | 通るべき完成盤面を受け入れる |
| [R-low](../../../../workbook/sessions/04-rules/checks/R-low.dzn) | required-1 | 0 | 指定合計より小さい完成盤面を拒否する |
| [R-high](../../../../workbook/sessions/04-rules/checks/R-high.dzn) | required-1 | 0 | 指定合計より大きい完成盤面を拒否する |
| [M-open](../../../../workbook/sessions/04-rules/checks/M-open.dzn) | multiple | 22 | 有効なヒントだけをすべて適用する |
| [M-ok](../../../../workbook/sessions/04-rules/checks/M-ok.dzn) | multiple | 1 | 有効なヒントだけをすべて適用する |
| [M-off](../../../../workbook/sessions/04-rules/checks/M-off.dzn) | multiple | 288 | 有効なヒントだけをすべて適用する |
| [M-bad](../../../../workbook/sessions/04-rules/checks/M-bad.dzn) | multiple | 0 | 有効なヒントだけをすべて適用する |
| [U-many](../../../../workbook/sessions/04-rules/checks/U-many.dzn) | second | 21 | Pが解であることを確認した後、別の解を探す |
| [U-none](../../../../workbook/sessions/04-rules/checks/U-none.dzn) | second | 0 | Pが解であることを確認した後、別の解を探す |
| [G-all](../../../../workbook/sessions/04-rules/checks/G-all.dzn) | generation | 1 | ヒントを選び、残る解の集合を確かめる |
| [G-three](../../../../workbook/sessions/04-rules/checks/G-three.dzn) | generation | 1 | ヒントを選び、残る解の集合を確かめる |
| [G-two](../../../../workbook/sessions/04-rules/checks/G-two.dzn) | generation | 8 | ヒントを選び、残る解の集合を確かめる |

Dは解説例、Rは必修1、Mは複数ヒント、Uは第二解、Gはヒント選択に対応する。D-low／R-lowは合計が指定値より一つ小さい固定盤面、D-high／R-highは一つ大きい固定盤面で、いずれも拒否する。基本条件に違反しているから解なしなのではなく、追加の合計が合わない例である。

## 必修2の確認

PとQの入力は別々に指定する。一つの入力でPとQを同時に固定すると、合計条件を調べる前に矛盾してしまう。Pを受理、Qを拒否、空盤面でも解あり、という三つの結果を確認する。

編集したモデルを保ったまま、配布フォルダーで次の三つを別々に実行する。選んだ三マスと合計値は途中で変更しない。

```sh
minizinc --solver gecode design-start.mzn P.dzn
minizinc --solver gecode design-start.mzn Q.dzn
minizinc --solver gecode design-start.mzn empty.dzn
```

期待する結果は順に「解あり」「UNSATISFIABLE」「解あり」。エラーやUNKNOWNを拒否成功と読まない。PとQの両方が通ったら、メモした三マスの合計と、モデルで実際に選んだ添字を照合する。

::: {.hint summary="確認例を開く：三マスと合計の一例"}
例えば(2,3),(3,3),(3,4)なら、Pの合計は1+4+3=8、Qの合計は2+4+3=9になる。ただし正しい選び方はこれだけではない。異なる三マスという範囲を守り、自分の式が同じ理由で区別できているか確かめる。
:::

## Pythonによるヒント選択

発展3の `clue-search-start.py` はPython標準ライブラリだけで動く。`clue-tools.py`・`boards.json`・入力盤面を同じフォルダーへ置く。最初はTODOを埋める必要があり、未実装なら `NotImplementedError` で止まる。

```sh
python3 clue-search-start.py P.json > selected.dzn
minizinc --solver gecode --all-solutions multi-base.mzn selected.dzn
```

候補番号は画面へ、生成した入力は `selected.dzn` へ出る。Pythonが失敗した場合はMiniZincへ進まず、エラーを確認する。実装を修正したら入力を再生成する。Qへ変える場合は `Q.json` を指定し、合計値もQから作り直す。
