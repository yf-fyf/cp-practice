# Pythonの環境構築

[第09回](../lesson.md)と[第10回](../../10-smt/lesson.md)では、PythonからZ3を使う。ここでは、uvでその実行環境を用意する。準備は授業内で扱い、授業外のインストール作業を前提にしない。教材の配布実装はPython 3.13・3.14とZ3 5.1.0で確認している。第03回などの発展で使う、標準ライブラリだけで動くPythonファイルも、同じ環境で実行できる。

uvが条件に合うPythonも用意するので、Pythonを先に入れておく必要はない。uvを入れた後のコマンドは、WindowsとmacOSで共通である。

## uvを入れる

uvがなければ、[uvの導入手順](https://docs.astral.sh/uv/getting-started/installation/)に従って入れる。WindowsではPowerShellで次を実行する。

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOSではターミナルで次を実行する。

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

導入後は、PowerShellやターミナルを開き直してから`uv --version`で確認する。

## 環境を作る

作業フォルダーへ[pyproject.toml](../../../../workbook/pyproject.toml)と[uv.lock](../../../../workbook/uv.lock)を保存する。教材一式のZIPを展開した場合は、`workbook`フォルダーに入っている。そのフォルダーで次を実行する。

```sh
uv sync
uv run python -c "import z3; print(z3.get_version_string())"
```

Z3のバージョンが表示されれば準備できている。`uv sync`は同じフォルダーに`.venv`を作り、uv.lockで固定した版のZ3を入れる。macOSは13以降が対象である。配布済みのZ3がない環境では、ソースからの構築を始めずにエラーで止まる。

## 演習で使う

本文や手引きの`python3`は`uv run python`へ読み替える。例えば`python3 warmup.py`は`uv run python warmup.py`になる。各回のファイルは、pyproject.tomlのあるフォルダーか、その下のフォルダーに置いて実行する。ZIPを展開した場合は、`workbook/sessions/09-sat`などの中でそのまま実行できる。エディタでは、pyproject.tomlと同じ場所の`.venv`を実行環境に選ぶ。

## つまずきやすい点

- `No module named 'z3'`と出たら、pyproject.tomlのあるフォルダーか、その下で実行しているかを確かめる。別の場所では、Z3の入っていないPythonで実行される。
- ファイル名を`z3.py`にするとライブラリと衝突する。配布名のまま使う。
- 参照先は[uvの説明](https://docs.astral.sh/uv/)と[Z3の公式リポジトリ](https://github.com/Z3Prover/z3#python)。
