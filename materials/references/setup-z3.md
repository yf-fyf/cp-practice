---
description: Python から Z3 を呼び出せるようにする手順。Windows・macOS・Linux の導入、仮想環境、固定バージョンの確認、最小動作確認、代表的なエラーへの対処
---

# Z3 実行環境の使い方（Python + z3-solver）

第05〜06回で使う Z3 は、**自分の PC に入れる**唯一の道具である。
Prolog と MiniZinc はブラウザで足りるが、Z3 は Python から呼び出して使う。

::: important
**第05回に入る前に、このページの「最小動作確認」まで到達しておくこと。**
うまくいかない場合は、詰まった場所と画面に出た文字を控えて授業に持ってくる。
:::

## 用意するもの

| もの | 条件 |
|---|---|
| Python | 3.10 以上（3.12 以降を推奨） |
| `z3-solver` | 固定バージョン `5.1.0.0` |

`z3-solver` は Z3 本体を同梱した Python パッケージである。
Z3 を別に入れる必要はなく、C++ のコンパイルも起きない。

::: important
**この科目では `z3-solver` の版を `5.1.0.0` に固定する。**
版によって出力の書式や既定の挙動が変わることがあるため、
教材と演習ファイルはこの版で動作を確認している。
:::

## Python が入っているかを確かめる

先に Python の版を確かめる。

Windows（PowerShell またはコマンドプロンプト）:

```console
> py --version
```

macOS / Linux（ターミナル）:

```console
$ python3 --version
```

`Python 3.12.x` のように出れば足りている。
「認識されていません」「command not found」と出たら、先に Python を入れる。

| OS | Python の入れ方 |
|---|---|
| Windows | [python.org](https://www.python.org/downloads/) のインストーラを実行する。**「Add python.exe to PATH」に必ずチェックを入れる** |
| macOS | [python.org](https://www.python.org/downloads/) のインストーラ、または Homebrew（`brew install python`） |
| Linux | ディストリビューションのパッケージ（Debian・Ubuntu 系なら `sudo apt install python3 python3-venv python3-pip`） |

## 仮想環境を作る（推奨）

科目用のフォルダを作り、その中だけに `z3-solver` を入れると、
他の授業や作業で使っている Python を汚さずに済む。

Windows:

```console
> py -m venv .venv
> .venv\Scripts\activate
```

macOS / Linux:

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
```

うまくいくとプロンプトの先頭に `(.venv)` が付く。
以後この状態で作業する。次に開いたときは有効化のコマンドだけをもう一度実行する。

::: warning
**Windows の PowerShell で `.venv\Scripts\activate` が拒否されることがある。**

```text
このシステムではスクリプトの実行が無効になっているため、ファイル
… \.venv\Scripts\Activate.ps1 を読み込むことができません。
```

PowerShell の**実行ポリシー**が既定で `Restricted` になっているためである。
同じウィンドウで次を実行してから、もう一度 `.venv\Scripts\activate` を打つ。

```console
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

`-Scope Process` なので、**そのウィンドウを閉じれば元に戻る**。
PC の設定を恒久的に変えるものではない。
それでも通らないときは、PowerShell ではなく**コマンドプロンプト**を開いて
`.venv\Scripts\activate.bat` を使う。
:::

::: note
仮想環境を作らずに入れてもかまわない。その場合、Windows は `py -m pip`、
macOS・Linux は `python3 -m pip` の形で以下を読み替える。
:::

## z3-solver を入れる

仮想環境を有効にした状態で次を実行する。版を `==` で指定するところまで含めて写す。

```console
$ pip install z3-solver==5.1.0.0
```

数十メガバイトのダウンロードが走る。
`Successfully installed z3-solver-5.1.0.0` と出れば入っている。

## バージョン確認

入った版を2か所で確かめる。

```console
$ pip show z3-solver
$ python -c "import z3; print(z3.get_version_string())"
```

前者は `Version: 5.1.0.0`、後者は `5.1.0` と出る。
桁数が違うのは、**パッケージの版と Z3 本体の版で数え方が違う**ためである。
どちらも同じものを指しているので、この2つが出れば正しい。

## 最小動作確認

次のファイルを作って実行する。「`p` または `q` が真」かつ「`p` は偽」を満たす
真偽の割り当てを探す、というだけの問題である。

```{.z3py filename="hello_z3.py"}
from z3 import *

p, q = Bools("p q")

s = Solver()
s.add(Or(p, q))
s.add(Not(p))

print(s.check())
print(s.model())
```

```console
$ python hello_z3.py
```

```solver
sat
[q = True, p = False]
```

::: check
- `sat` が出た → 充足する割り当てが見つかった
- `[q = True, p = False]` が出た → その割り当ての中身
- ここまで出れば準備は完了である。第05回へ進んでよい
:::

解の並び順（`q` が先か `p` が先か）は環境によって変わることがある。
**中身が合っていれば問題ない。**

### 終了コードの見かた

Python が「正常に終わったか」は**終了コード**で分かる。正常なら `0` である。
第10回の検証器で使うので、ここで一度見ておく。
**見る書き方は端末によって違う。**

| 端末 | 直後に打つもの |
|---|---|
| macOS / Linux のシェル、Windows の Git Bash・WSL | `echo $?` |
| Windows のコマンドプロンプト（`cmd`） | `echo %ERRORLEVEL%` |
| Windows の PowerShell | `$LASTEXITCODE` |

```console
$ python hello_z3.py
$ echo $?
```

```text
0
```

PowerShell の `$?` は `True` / `False` を返すもので、**番号ではない**。
番号が要るときは `$LASTEXITCODE` を見る。

## 代表的なエラーと対処

| 画面に出るもの | 原因 | 直しかた |
|---|---|---|
| `ModuleNotFoundError: No module named 'z3'` | 入れた Python と実行した Python が違う | 仮想環境を有効化し直す。`pip` ではなく `python -m pip install z3-solver==5.1.0.0` で入れる |
| `'pip' は認識されていません` / `pip: command not found` | `pip` に PATH が通っていない | Windows は `py -m pip`、macOS・Linux は `python3 -m pip` を使う |
| `'python' は認識されていません` | Windows で PATH にない | `py` を使う。または Python を入れ直して「Add python.exe to PATH」にチェックを入れる |
| `ERROR: Could not find a version that satisfies the requirement` | 版の指定が届いていない／Python が古い | Python の版を確かめる。3.10 未満なら新しい Python を入れる |
| `SSLError` / `ProxyError` | ネットワークの制限 | 別の回線で試す。学内ネットワークの制限が疑わしいときは持ち込む |
| `Symbolic expressions cannot be cast to concrete Boolean values.` | Python の `and` / `or` / `not` を Z3 の式に使った | `And` / `Or` / `Not` を使う（[Z3Py 早見表](z3py-cheatsheet.md)） |
| `Activate.ps1 を読み込むことができません` / `PSSecurityException` | Windows の PowerShell の実行ポリシーが `Restricted` | 上の「仮想環境を作る」の警告を見る。`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` を先に実行する |

Z3 のプログラムを書き始めてから出るエラーは
[よくあるエラーと対処](errors.md)にまとめてある。

## 動かないときの逃げ道

**Z3 が動かないことは、授業に出られないことを意味しない。**
Prolog と MiniZinc にはブラウザで動く実行環境があるが、
**Z3 にはこの科目で使える Playground のようなものが無い**。
だから、その場で直らないときは次のどれかで進める。

| 逃げ道 | やること |
|---|---|
| **2人1組にする** | 隣の学習者と画面を1つ共有して進める。書く役と読む役を交代すれば、どちらの手も止まらない |
| **教員機で実行する** | 書き上げた `.py` を教員機で走らせて、`sat` か `unsat` かだけを確かめる |
| **先に書き切る** | 論理式と `s.add(...)` の行はエディタ（または紙）だけで書ける。実行は後回しにして、動く環境ができてから確かめる |

いずれの場合も、**詰まった場所と画面に出た文字を控えておく**。
次の回までに直すための手掛かりはそこにしかない。

## 演習ファイルとの対応

第05回以降の演習ファイルには、使う版を書いた `requirements.txt` が付いている。
仮想環境を有効にして次を実行すれば、同じ版が入る。

```console
$ pip install -r requirements.txt
```

自由課題（第11〜14回）で Z3 を使うときは、**使った版を成果物の README に書く**。
採点する側が同じ結果を再現できることが条件である。

## 扱わないこと

- **Z3 のソースからのビルド** → `z3-solver` で足りる
- **SMT-LIB 形式のファイルを直接 Z3 に渡す使い方** → この科目では Python からだけ呼ぶ
- **`Optimize`（最適化）の使い方** → 入口だけ [Z3Py 早見表](z3py-cheatsheet.md)に置いてある（第06回の発展演習）。最適化そのものは[第07回](../sessions/07-theme-assignment.md)以降に MiniZinc で扱う
- **Jupyter Notebook での実行** → 使ってもよいが、提出物は `.py` で出す
