# 第04回 数独: データ分離、列挙、一意性（演習ファイル）

考え方・手順・ヒントは教材ページにある。ここには実行方法だけを書く。

## ファイル

| ファイル | 使うところ |
|---|---|
| `sudoku.mzn` | 必須演習・標準演習。`% TODO` が2か所ある |
| `puzzle-a.dzn` | 盤面A（9×9）。必須演習・標準演習で使う |
| `puzzle-b.dzn` | 盤面B（9×9）。盤面Aから初期値を1つ減らしたもの。標準演習で使う |
| `puzzle-solved.dzn` | 完成済みの盤面。既知例による検証に使う |

盤面の確認には第03回の `../03-minizinc-sudoku/check_sudoku.py` をそのまま使う。

## 実行する

手順は5行のカードに1か所だけまとめてある。
教材サイトの参考資料「MiniZinc 実行環境の使い方」の**手順カード（モデル + データ）**を見る。
Playground の画面が変わったときも、直すのはそのカード1か所である。

この回で使うのは次の組み合わせである。

- モデル: `sudoku.mzn`
- データ: `puzzle-a.dzn`（必須演習・標準演習）／ `puzzle-b.dzn`・`puzzle-solved.dzn`（標準演習）

インストールは要らない。

## 盤面を確かめる

出力の盤面の部分をファイルに保存して渡す。`--given` に使った盤面のデータを渡すと、
初期値が動いていないかまで調べる。

```console
$ python3 ../03-minizinc-sudoku/check_sudoku.py --given puzzle-a.dzn board.txt
```

貼り付けて渡すこともできる。Ctrl-D（Windows は Ctrl-Z のあと Enter）で確定する。

```console
$ python3 ../03-minizinc-sudoku/check_sudoku.py --given puzzle-a.dzn
```
