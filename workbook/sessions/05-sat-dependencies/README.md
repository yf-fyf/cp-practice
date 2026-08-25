# 第05回 SAT概説とパッケージ依存関係: Booleanモデル（演習ファイル）

考え方・手順・ヒントは教材ページにある。ここには実行方法だけを書く。

## ファイル

| ファイル | 使うところ |
|---|---|
| `deps.py` | 必須演習・標準演習。`# TODO` が4か所ある |
| `requirements.txt` | 使う Z3 の版 |

## 準備する

第05回に入る前に済ませておく。手順は教材サイトの「Z3 実行環境の使い方」にある。

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Windows は次のようにする。

```console
> py -m venv .venv
> .venv\Scripts\activate
> pip install -r requirements.txt
```

入ったかどうかを確かめる。

```console
$ python -c "import z3; print(z3.get_version_string())"
```

## 実行する

```console
$ python3 deps.py
```

`sat` と入れ方の一覧、または `unsat` が出る。
