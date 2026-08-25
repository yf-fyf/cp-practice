# 第10回 勤務表: 検証と性能評価（演習ファイル）

考え方・手順・ヒントは教材ページにある。ここには実行方法だけを書く。

## ファイル

| ファイル | 使うところ |
|---|---|
| `verify_roster.py` | 必須演習・標準演習。`# TODO` が2か所ある |
| `samples/` | 検査にかける出力。正常例2本と反例6本 |
| `small_pref.dzn` | 基礎データ（4人・3日 + 希望休3件） |
| `week_pref.dzn` | 標準データ（8人・7日 + 希望休） |
| `week14_pref.dzn` | 規模拡大データ（8人・14日 + 希望休） |

`.dzn` はすべて架空のデータである。実在する職場の希望調査ではない。

`small_pref.dzn` と `week_pref.dzn` は第09回と**同じ内容**で、
重み `w_night` だけ第09回の標準演習を終えた状態（3項）に合わせて `1` にしてある。
`samples/` の出力はこの重みで作ったものなので、
検査するときは**この回の `.dzn`** を渡す。

## 検証器を動かす

Python 3 だけで動く。外部ライブラリも MiniZinc も要らない。

```console
$ python3 verify_roster.py samples/good-small.txt small_pref.dzn
```

同梱の例をまとめて判定する。

```console
$ python3 verify_roster.py --samples
```

引数を付けずに実行すると、使い方と読み取る行の書式が出る。

```console
$ python3 verify_roster.py
```

**終了コード**は合格で `0`、不合格で `1` である。
使い方の表示（引数なし）や読み取り失敗は `2` である。直後に確かめられる。
見る書き方は端末によって違う。

```console
$ echo $?
```

- macOS / Linux のシェル、Windows の Git Bash・WSL: `echo $?`
- Windows のコマンドプロンプト（`cmd`）: `echo %ERRORLEVEL%`
- Windows の PowerShell: `$LASTEXITCODE`（`$?` は `True` / `False` で番号ではない）

## `samples/` の中身

| ファイル | 中身 | 組にする `.dzn` | 期待 |
|---|---|---|---|
| `good-small.txt` | 4人・3日の最適解 | `small_pref.dzn` | 合格 |
| `good-week.txt` | 8人・7日の最適解 | `week_pref.dzn` | 合格 |
| `broken-coverage.txt` | 必要人数の違反 | `small_pref.dzn` | 不合格 |
| `broken-qualification.txt` | 資格の違反 | `small_pref.dzn` | 不合格 |
| `broken-rest.txt` | 休息の違反 | `small_pref.dzn` | 不合格 |
| `broken-value.txt` | `#value pref` の値が違う | `small_pref.dzn` | 不合格 |
| `dropped-qualification.txt` | 資格制約を外したモデルの出力 | `week_pref.dzn` | 不合格 |
| `dropped-rest.txt` | 休息制約を外したモデルの出力 | `week_pref.dzn` | 不合格 |

`broken-` の4本は、**1種類の違反だけ**を含む。

## 自分の出力を検査する

第09回の `roster_soft.mzn` を [MiniZinc Playground](https://play.minizinc.dev/) で
実行し、**出力欄の中身を全部**コピーしてファイルに保存する。

Playground に貼るデータも、**この回の `.dzn`** にすること。
`#value penalty` は重みから計算される値なので、
出力を作ったときと違う重みの `.dzn` で検査すると、
正しい表なのに「不合格」になる。**出力とデータは常に組で扱う。**

```console
$ python3 verify_roster.py 保存したファイル week_pref.dzn
```

検証器が読むのは `#` で始まる行だけである。
人が読む表の部分が混ざっていてもかまわないので、**出力全体をそのまま保存**してよい。

```text
#size <人数> <日数>
#shift <名前> <D/N/O の並び>
#value pref <整数>
#value unfair <整数>
#value night_unfair <整数>
#value penalty <整数>
```

`#value` の行は、第09回の TODO を埋めたモデルだけが出す。
無くても検査は動く（ハード制約の3項目だけを見る）。

解が何本出ていても、**最後の解**が検査の対象になる。

## 14日のデータを試す

`week14_pref.dzn` は `week_pref.dzn` を2週間に伸ばしたものである。
Playground で `roster_soft.mzn` のデータをこれに差し替えて実行する。

**`==========` が出ないまま止まらないことがある。**
異常ではない。時間を決めて実行を止め、そこまでに出た最後の解を使う。
理由と対処は教材ページの「速さを測る」にある。

操作の詳細は教材サイトの「MiniZinc 実行環境の使い方」にある。
