# MiniZincの実行の手引き

第02回で使うモデルの開き方、入力の交換、結果の読み方をまとめる。最初は小さな二変数モデルで操作を確かめ、数独では同じ手順を使う。[本文の解説例](../lesson.md#解説例)へ戻りながら利用しよう。

## 最初の実行

授業で案内するMiniZincの環境を開く。ブラウザでは[MiniZinc Playground](https://play.minizinc.org/)を使える。ローカルに用意されたMiniZinc IDEでも、同じモデルを実行できる。

1. [warmup.mzn](../../../../workbook/sessions/02-minizinc/warmup.mzn)を開くか、その内容をモデルの編集欄へ貼り付ける。別の例がある場合は、編集欄の内容を置き換える。
2. ソルバーにGecodeを選び、Runを押す。プログラムはモデルの編集欄へ入れ、結果欄は読むために使う。
3. `x = 1, y = 4` または `x = 2, y = 3` が出たら、`x < y`{.minizinc} と `x + y = 5`{.minizinc} を確かめる。
4. 和の5を6に変えて再実行する。今度は `x = 2, y = 4` になる。

画面操作で止まった場合は、その場で教員と一緒に確認する。ネットワークが使えない場合には、授業で用意したローカル環境へ切り替える。環境準備を授業外の必須作業にはしない。

## モデルと入力

数独の最初の実行には、[sudoku4-demo.mzn](../../../../workbook/sessions/02-minizinc/sudoku4-demo.mzn)が使える。モデルと入力を一つにまとめてあるので、そのファイルだけを開いてRunを押せばよい。

入力を交換する演習では、モデルの `.mzn` と入力の `.dzn` を分ける。MiniZinc IDEではモデルと入力の両ファイルを開き、モデルのタブでRunを押し、データを選ぶ画面で指定の `.dzn` を選ぶ。編集後は保存して実行する。データ選択の詳しい操作は[公式IDE手引き](https://docs.minizinc.dev/en/stable/minizinc_ide.html)も参照できる。

ブラウザで一ファイルとして扱う場合は、開始用 `.mzn` の内容に、指定の `.dzn` の内容を末尾へ追加して実行する。入力を交換するときは、末尾の `given = [| ... |];`{.minizinc} 全体を新しい入力で置き換える。新旧の `given` を二つ残さない。

| 作業 | モデル | 入力 |
|---|---|---|
| 解説例 | [sudoku4.mzn](../../../../workbook/sessions/02-minizinc/sudoku4.mzn) | [demo.dzn](../../../../workbook/sessions/02-minizinc/demo.dzn) |
| 必修1 | [practice-start.mzn](../../../../workbook/sessions/02-minizinc/practice-start.mzn)に追記 | [practice.dzn](../../../../workbook/sessions/02-minizinc/practice.dzn) |
| 必修2 | [diagonal-start.mzn](../../../../workbook/sessions/02-minizinc/diagonal-start.mzn)に追記 | [diagonal.dzn](../../../../workbook/sessions/02-minizinc/diagonal.dzn) |

必修1は `grid` の宣言が未完成なので、配布直後は実行できない。必修2は基本の数独までは実行できるが、追加すべき主対角線の条件はまだ入っていない。どちらも本文の `TODO(作業N)` を手掛かりに補う。

## コマンドでの実行

MiniZincを使える端末では、配布ファイルを置いたディレクトリで次のように実行できる。モデルと入力のファイル名を、今取り組んでいる組へ置き換える。

```sh
minizinc --solver gecode warmup.mzn
minizinc --solver gecode sudoku4.mzn demo.dzn
minizinc --solver gecode practice-start.mzn practice.dzn
minizinc --solver gecode diagonal-start.mzn diagonal.dzn
```

発展2は `given` と `first` の二つの入力を使う。この場合は `minizinc --solver gecode second-start.mzn empty.dzn first.dzn` と指定する。ブラウザの一ファイル方式では二つの `.dzn` の内容を両方追加する。代入先の名前が異なるので重複しない。

## 出力の読み分け

実行結果は、解があるかどうかだけでなく、処理が完了したかも見て判断する。次の表で、問題の条件による解なしと、コードや入力の不備を区別しよう。

| 表示 | 意味と次の確認 |
|---|---|
| 数字の組や盤面、`----------` | 一つの解。元の条件と照合する |
| `UNSATISFIABLE` | 指定した条件を同時に満たす解がない |
| `UNKNOWN`、時間切れ、途中停止 | 判定が完了していない。解なしとは言えない |
| syntax error、type error、未宣言の名前 | 記号・宣言・入力を直してから解き直す |

例えば操作例の和を9にすると、1〜4の二整数では届かず、解なしになる。コードを誤って壊した場合のエラーとは違う。全角記号、末尾の `;`{.minizinc}、二次元配列の `[|`{.minizinc}・`|]`{.minizinc}、`given` の重複指定を順に確かめるとよい。

## 全解と一意性

発展で解の個数を調べる場合は、一解で止める通常の実行から全解の列挙へ切り替える。コマンドでは `--all-solutions` を付ける。この回の小例はGecodeで確認できる。

```sh
minizinc --solver gecode --all-solutions sudoku4.mzn demo.dzn
```

各 `----------` が一つの解の区切りになる。この充足問題の全解列挙で最後に `==========` が出れば、探索が完了している。完了するまでに一盤面だけなら一意である。二盤面見つかれば、その時点で一意ではないと分かる。途中まで一つしか見えていない状態では、一意と判断しない。

画面から全解を指定する場所が分からなければ、教員が用意した端末で上のコマンドを使う。発展2のように既知の解だけを除外する方法でも別解を探せるが、「除外した盤面が元の問題の解である」という確認が先に必要になる。

モデル・入力・コマンドの基礎は[公式チュートリアル](https://docs.minizinc.dev/en/stable/modelling.html)で確認できる。この手引きでは、第02回に必要な操作だけを使っている。
