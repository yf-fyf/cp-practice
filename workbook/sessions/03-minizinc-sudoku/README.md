# 第03回 数独: MiniZincで盤面を解く（演習ファイル）

考え方・手順・ヒントは教材ページにある。ここには実行方法だけを書く。

## ファイル

| ファイル | 使うところ |
|---|---|
| `coloring5.mzn` | 小さな実行例。穴埋めは無い。そのまま実行する |
| `sudoku4.mzn` | 必須演習・標準演習。`% TODO` が4か所ある |
| `check_sudoku.py` | 完了チェック。出力された盤面を独立に検査する |
| `puzzle01.dzn` | 発展演習の動作確認用（4×4）。第03回の本編では使わない |
| `puzzle09.dzn` | 発展演習の動作確認用（9×9）。第03回の本編では使わない |

## 実行する

1. [MiniZinc Playground](https://play.minizinc.dev/) をブラウザで開く。
2. `.mzn` の中身を貼り付けるか、ファイルとして読み込ませる。
3. 実行する。解が見つかると盤面が出る。

インストールは要らない。データファイル（`.dzn`）を併せて使うのは第04回からで、
その手順は教材サイトの「MiniZinc 実行環境の使い方」の**手順カード**に1か所だけ置いてある。

## 盤面を確かめる

Playground の出力を貼り付けて Ctrl-D（Windows は Ctrl-Z のあと Enter）を押す。

```console
$ python3 check_sudoku.py
```

ファイルに保存してあるなら引数で渡す。

```console
$ python3 check_sudoku.py board.txt
```

`sudoku4.mzn` 以外の盤面を調べるときは、その盤面のデータを `--given` に渡す。

```console
$ python3 check_sudoku.py --given ../04-sudoku-data-uniqueness/puzzle-a.dzn board.txt
```

初期値の照合そのものを省くなら `--no-given` を付ける。
