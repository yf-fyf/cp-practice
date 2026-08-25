---
description: Prolog・MiniZinc・Z3でよく出るエラーと対処。メッセージの読み方、UNSAT・解が出ない場合の切り分け、共通のつまずき
---

# よくあるエラーと対処

道具ごとに、実際に出やすいものだけを挙げてある。
**メッセージの文言は版によって少しずつ変わる**ので、
完全に一致しなくても「型」が同じものを探す。

::: important
エラーが出たら、まず **1行目と行番号**を読む。
それ以降は原因を説明する詳細で、読まなくても直せることが多い。
:::

## どの道具でも起きること

### 記号が全角になっている

日本語入力のまま括弧・カンマ・ピリオドを打つと、必ず構文エラーになる。
画面では見分けが付きにくい。

| 全角（誤） | 半角（正） |
|---|---|
| `（` `）` `［` `］` | `(` `)` `[` `]` |
| `，` `．` `；` | `,` `.` `;` |
| 全角スペース | 半角スペース |

構文エラーが出て原因が分からないときは、
**その行を消してもう一度半角で打ち直す**のが早い。

### 解が出ない（UNSAT・`false.`）

条件を同時に満たすものが無い、という**答え**である。
モデルが壊れているとは限らない。切り分けは共通である。

1. 制約を1つずつコメントアウトして、**どれを外すと解が出るか**を探す。
2. 出たら、その制約が「書きたかった条件」と合っているかを読み直す。
3. 手掛かりを逆向きに書いていないか（「〜でない」を「〜である」と書いていないか）。
4. 定義域が狭すぎないか。値の範囲を1つ広げると解が出ないか。
5. **本当に解が無い問題**でないかを、小さな例で手で確かめる。

::: note
制約に番号を振ってコメントに書いておくと（[定式化の7手順](modeling-steps.md)）、
この切り分けが速くなる。
:::

### いつまでも終わらない

1. まず止める（Prolog 実行ページは「中断」、MiniZinc Playground と Python は
   実行を止めてから考える）。
2. **規模を小さくして**試す。地区5つ、盤面 4×4、職員4人、3日分など。
3. 小さくして解けるなら、規模の増え方に対して候補が急激に増えている。
   条件を書く順序（Prolog）や定義域の広さを見直す。
4. 小さくしても終わらないなら、条件の書き方そのものを疑う。

## Prolog

実行ページの操作は [Prolog 実行環境の使い方](setup-prolog.md)、
構文は [Prolog 早見表](prolog-cheatsheet.md)にある。

| 結果欄に出るもの | 原因 | 直しかた |
|---|---|---|
| `syntax_error(...)` と `line(N)` | N 行目の書き方が正しくない | 節の終わりのピリオド、条件のつなぎのカンマ、括弧と引用符の対応を見る |
| `existence_error(procedure, member/2)` | `member/2` が定義されていない | `:- use_module(library(lists)).` を先頭に書く。綴りと引数の個数も確かめる |
| `instantiation_error` | 値がまだ決まっていない変数を使った | 値が決まる条件を先に書く（生成してから絞り込む） |
| `type_error(...)` | 想定と違う種類の値を渡した | リストを渡すべきところにアトムを渡していないか |
| `false.` がすぐ出る | 条件が厳しすぎる／手掛かりの向きを間違えた | 手掛かりを1つずつコメントアウトして、どれが効きすぎているかを見る |
| 終わらない | 候補が多すぎる | 「中断」を押す。生成のたびに絞り込む形に書き直す |

### ピリオドの付け忘れ

もっとも多い。**節は必ずピリオドで終わる**。
最後の行にピリオドが無いと、次の節と1つにつながって別のエラーになる。

```{.prolog filename="誤り"}
drinks(aoi, cocoa)
drinks(hikaru, coffee).
```

```{.prolog filename="正しい"}
drinks(aoi, cocoa).
drinks(hikaru, coffee).
```

### アトムと変数の取り違え

小文字始まりがアトム、大文字始まりが変数である。
`Aoi` と書くと、`aoi` という名前ではなく**何にでも当てはまる変数**になる。

```{.prolog filename="誤り: Aoi は変数なので、すべての人に当てはまってしまう"}
drinks(Aoi, cocoa).
```

## MiniZinc

操作は [MiniZinc 実行環境の使い方](setup-minizinc.md)、
構文は [MiniZinc 早見表](minizinc-cheatsheet.md)にある。

| 出るものの型 | 原因 | 直しかた |
|---|---|---|
| `type error: undefined identifier` | 名前の綴り違い、または宣言前に使った | 綴りを確かめる。大域制約なら `include "globals.mzn";` を書く |
| `syntax error` と行番号 | 記号の過不足 | 行末の `;`、括弧の対応、`endif` の書き忘れ、全角記号を見る |
| `type error` で型の名前が並ぶ | 型が合わない | `var` の有無、整数と真偽の取り違え、`bool2int` の付け忘れ |
| `variable 'n' must be defined (did you forget to specify a data file?)` | `.dzn` の値が届いていない | 実行時にデータファイルを選んだか。モデル側で値まで書いていないか |
| `multiple assignment to the same variable` | モデル側にも `.dzn` 側にも値が書いてある | モデル側を `int: n;` のように宣言だけにする |
| 配列の範囲外を指した旨のエラー | 添字が範囲を出た | `d + 1` を使う `forall` の範囲を1つ内側に刻む |
| `=====UNSATISFIABLE=====` | 条件を同時に満たせない | 上の「解が出ない」の手順で切り分ける |

```{.text .error}
MiniZinc: type error: undefined identifier `all_different'
```

上のエラーは `include "globals.mzn";` の書き忘れで出る。

### `var` の書き忘れ・書きすぎ

```{.minizinc filename="誤り: 決めてほしい値なのに var が無い"}
array[1..4] of 1..4: x;
```

```{.minizinc filename="正しい"}
array[1..4] of var 1..4: x;
```

逆にパラメータへ `var` を付けると、モデルは動くが探索空間が無駄に広がる。

### `.dzn` で上書きできない

```{.minizinc filename="誤り: モデル側で値まで書いている"}
int: n = 4;
```

```{.minizinc filename="正しい: 宣言だけにする"}
int: n;
```

### 隣の添字で範囲外

```{.minizinc filename="誤り: d = 7 のとき d + 1 が範囲外"}
constraint forall(s in STAFF, d in 1..7)(
  roster[s, d] = night -> roster[s, d + 1] = off
);
```

```{.minizinc filename="正しい: 最終日を除く"}
constraint forall(s in STAFF, d in 1..6)(
  roster[s, d] = night -> roster[s, d + 1] = off
);
```

## Z3（Python）

導入は [Z3 実行環境の使い方](setup-z3.md)、
API は [Z3Py 早見表](z3py-cheatsheet.md)にある。

| 出るもの | 原因 | 直しかた |
|---|---|---|
| `ModuleNotFoundError: No module named 'z3'` | 入れた Python と実行した Python が違う | 仮想環境を有効化する。`python -m pip install z3-solver==5.1.0.0` で入れ直す |
| `NameError: name 'Bool' is not defined` | `from z3 import *` を書いていない | ファイルの先頭に書く。`import z3` だけでは `Bool` は使えない |
| `Z3Exception: Symbolic expressions cannot be cast to concrete Boolean values.` | Python の `and` / `or` / `not` を Z3 の式に使った | `And` / `Or` / `Not` を使う |
| `Z3Exception: True, False or Z3 Boolean expression expected. Received 1 of type <class 'int'>` | 真偽の式でないものを `add` に渡した | `x == 1` ではなく `x`、または `x == True` の形にする |
| `Z3Exception: model is not available` | `unsat` なのに `model()` を呼んだ | `if s.check() == sat:` の中でだけ `model()` を呼ぶ |
| `TypeError: Solver.add() got an unexpected keyword argument 'n'` | `s.add(n = 3)` と書いた | 等号は2つ書く（`s.add(n == 3)`） |

### エラーが出ないのに間違っている書き方

**もっとも危ないのはこれである。**エラーが出ないので気付きにくい。

```{.z3py filename="誤り: unsat でも中に入ってしまう"}
if s.check():
    m = s.model()
```

`check()` が返す `sat` / `unsat` / `unknown` は真偽値ではないが、
Python はどれも「真」と見なす。**必ず `== sat` で比べる。**

```{.z3py filename="正しい"}
if s.check() == sat:
    m = s.model()
```

もう1つは、モデルから取り出した値をそのまま計算に使うことである。

```{.z3py filename="誤り: 計算されず、式が表示されるだけ"}
print(m[n] + 1)
```

```{.z3py filename="正しい"}
print(m[n].as_long() + 1)
```

### `m[x]` が `None` になる

制約に一度も現れない変数を引くと `None` が返る。
その変数を制約に入れ忘れていないか、変数名を作り直していないかを確かめる。

```{.z3py filename="誤り: 名前は同じでも、毎回作り直すと別の変数になる"}
s.add(Bool("p"))
m = s.model()
print(is_true(m[Bool("q")]))       # m[...] は None。is_true(None) は False になる
```

## モデルの出力を Python の検証器へ渡すとき

[第10回](../sessions/10-roster-verification.md)では、MiniZinc の出力をファイルに
保存して Python のプログラムに読ませる。**2つのプログラムのあいだ**で起きる誤りは、
どちらか片方だけを見ていても分からない。

| 症状 | 原因 | 直し方 |
|---|---|---|
| `#size の行が無い` | 出力の一部しかコピーしていない。区切り記号より下を取りこぼしやすい | 出力欄を全部選んでコピーし直す |
| 行数や長さが合わない | 途中経過の解と最適解の境目で貼り付けが切れた | 出力全体をそのまま保存する。検証器は最後の解だけを見る |
| 正常なはずの解が「不合格」になる | 出力を作ったときと違うデータファイルを渡した（重みや入力が違う） | **出力とデータは組で扱う**。片方だけ差し替えない |
| `IndexError: string index out of range` | 出力の日数とデータファイルの日数が食い違っている | 大きいほうの出力を小さいほうのデータで検査していないか確かめる |
| 文字化けする | 保存したファイルの文字コードが UTF-8 でない | エディタの保存設定を UTF-8 にする |
| `echo $?` が `$?` とそのまま表示される | Windows のコマンドプロンプトや PowerShell で打った | 端末に合う書き方にする（下の表） |

### 終了コードが見られない

検証器が合格したかどうかは**終了コード**で分かる（合格 `0`、不合格 `1`）。
見る書き方は端末によって違う。

| 端末 | 直後に打つもの |
|---|---|
| macOS / Linux のシェル、Windows の Git Bash・WSL | `echo $?` |
| Windows のコマンドプロンプト（`cmd`） | `echo %ERRORLEVEL%` |
| Windows の PowerShell | `$LASTEXITCODE` |

PowerShell の `$?` は `True` / `False` を返すもので、**番号ではない**。
別のコマンドを1つでも挟むと値が入れ替わるので、**実行した直後に**見る。

::: important
**整形した表を読ませようとしない。**

人が読むための行は、全角スペースの数や記号の位置が変わりやすい。
別のプログラムに渡す値は、`output` に**受け渡し専用の行**を足して出す。

```{.minizinc filename="受け渡し専用の行を足す"}
output
  [ "（人が読む表）\n" ]
  ++ [ "#value total " ++ show(total) ++ "\n" ];
```

`#` で始めておくと、人が読む部分と目で見分けられる。
自由課題でも同じ手が使える。
:::

## それでも直らないとき

次の3つを控えて持ってくる。この3点があれば、たいていその場で切り分けられる。

::: {.check}
- [ ] **何をしたか**（どのファイルを、どのボタンで実行したか）
- [ ] **画面に出た文字**（省略せず、1行目と行番号を含めて）
- [ ] **期待していたこと**（どうなるはずだったか）
:::

## 関連ページ

- [定式化の7手順](modeling-steps.md) — 制約に番号を振っておくと切り分けが速い
- [用語集](glossary.md) — UNSAT・定義域・大域制約などの定義
- [参考資料の索引](README.md) — 知りたいことから引く
