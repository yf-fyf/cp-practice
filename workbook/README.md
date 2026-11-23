# 演習ファイル

[科目の進め方](../materials/sessions/01-prolog/guides/course-start.md)を読み、各回の本文から指定されたファイルを使います。本文には実行手順・必修演習・自己確認、発展ページには発展・選択演習があります。

| 回 | 本文 | 配布物 |
|---|---|---|
| 第01回 | [第01回　Prologで関係を書く](../materials/sessions/01-prolog/lesson.md) | [演習ファイル](sessions/01-prolog/) |
| 第02回 | [第02回　MiniZincで小さな数独を解く](../materials/sessions/02-minizinc/lesson.md) | [演習ファイル](sessions/02-minizinc/) |
| 第03回 | [第03回　候補を減らし、場合分けして解く](../materials/sessions/03-search/lesson.md) | [演習ファイル](sessions/03-search/) |
| 第04回 | [第04回　ルールを制約にして、パズルを作る](../materials/sessions/04-rules/lesson.md) | [演習ファイル](sessions/04-rules/) |
| 第05回 | [第05回　講座の割当を0/1の表で表す](../materials/sessions/05-assignment/lesson.md) | [演習ファイル](sessions/05-assignment/) |
| 第06回 | [第06回　目的関数で良さを比べる](../materials/sessions/06-optimization/lesson.md) | [演習ファイル](sessions/06-optimization/) |
| 第07回 | [第07回　勤務表を数理モデルとして解く](../materials/sessions/07-schedule/lesson.md) | [演習ファイル](sessions/07-schedule/) |
| 第08回 | [第08回　希望の上限と、最小化する指標](../materials/sessions/08-preferences/lesson.md) | [演習ファイル](sessions/08-preferences/) |
| 第09回 | [第09回　SATで依存・排他・選択を扱う](../materials/sessions/09-sat/lesson.md) | [演習ファイル](sessions/09-sat/) |
| 第10回 | [第10回　SMTで作業の日程を組む](../materials/sessions/10-smt/lesson.md) | [演習ファイル](sessions/10-smt/) |

ファイル間の相対参照を保って使ってください。通常演習の提出や宿題はありません。第11〜15回の自由課題の提出方法は、決まり次第案内します。

## Pythonの環境

第09回・第10回はPythonからZ3を使います。このフォルダーの[pyproject.toml](pyproject.toml)と[uv.lock](uv.lock)は、[uv](https://docs.astral.sh/uv/)で使う全回共通の環境です。WindowsでもmacOSでも、このフォルダーで次を実行すれば同じ版のZ3が入ります。

```sh
uv sync
uv run python -c "import z3; print(z3.get_version_string())"
```

演習では、本文の`python3`を`uv run python`へ読み替えて、`sessions/09-sat`などの中で実行します。uvの入れ方は、[Pythonの環境構築](../materials/sessions/09-sat/guides/python-start.md)にあります。
