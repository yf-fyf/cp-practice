# 実践・制約プログラミング

2026年度の教材です。公開サイト：<https://yf-fyf.github.io/cp-practice/>

新版の第01〜10回を移植し、**このリポジトリの原稿と配布物を編集してレビューする段階**です。内容の人手レビュー・授業試行は完了していません。

通常回は Prolog → MiniZinc → SAT・SMT の順で進み、第11〜15回は個別の自由課題です。各回100分。通常演習の提出・宿題は設けません。

## レビューするファイル

- `materials/sessions/<URL名>/lesson.md`：本文と必修演習
- 同じフォルダーの `advanced-exercises.md`：発展・選択演習
- 同じフォルダーの `guides/` と `figures/`：手引きと図
- `workbook/sessions/<URL名>/`：配布するモデル・入力・確認用ファイル
- `site/nav.yaml`：URL、原稿の対応、配布するファイルの一覧

例えば第07回は `materials/sessions/07-schedule/lesson.md` を編集します。サイトのURLは `/sessions/07-schedule/` です。

| 回 | 本文 | 配布物 |
|---|---|---|
| 第01回 | [第01回　Prologで関係を書く](materials/sessions/01-prolog/lesson.md) | [演習ファイル](workbook/sessions/01-prolog/) |
| 第02回 | [第02回　MiniZincで小さな数独を解く](materials/sessions/02-minizinc/lesson.md) | [演習ファイル](workbook/sessions/02-minizinc/) |
| 第03回 | [第03回　候補を減らし、場合分けして解く](materials/sessions/03-search/lesson.md) | [演習ファイル](workbook/sessions/03-search/) |
| 第04回 | [第04回　ルールを制約にして、パズルを作る](materials/sessions/04-rules/lesson.md) | [演習ファイル](workbook/sessions/04-rules/) |
| 第05回 | [第05回　講座の割当を0/1の表で表す](materials/sessions/05-assignment/lesson.md) | [演習ファイル](workbook/sessions/05-assignment/) |
| 第06回 | [第06回　目的関数で良さを比べる](materials/sessions/06-optimization/lesson.md) | [演習ファイル](workbook/sessions/06-optimization/) |
| 第07回 | [第07回　勤務表を数理モデルとして解く](materials/sessions/07-schedule/lesson.md) | [演習ファイル](workbook/sessions/07-schedule/) |
| 第08回 | [第08回　希望の上限と、最小化する指標](materials/sessions/08-preferences/lesson.md) | [演習ファイル](workbook/sessions/08-preferences/) |
| 第09回 | [第09回　SATで依存・排他・選択を扱う](materials/sessions/09-sat/lesson.md) | [演習ファイル](workbook/sessions/09-sat/) |
| 第10回 | [第10回　SMTで作業の日程を組む](materials/sessions/10-smt/lesson.md) | [演習ファイル](workbook/sessions/10-smt/) |

## ローカルで読む・確認する

依存は Python 3.11以上、PyYAML、Pandoc（検証版3.10.2）です。図のSVGは同梱済みなので、通常のサイト生成にTeXは不要です。

```sh
make serve                         # http://127.0.0.1:8000/ を開く
make serve PORT=9000               # 別ポート
make serve HOST=0.0.0.0            # 別端末からも閲覧する場合
make check                        # 生成・リンク・原稿・配布範囲の検査
make pages VERSION=v0.1.0-preview # ローカルに .pages/ と配布ZIPを組み立てる
```

`make serve` は原稿・配布物・表示資産・生成コードの保存を検知して再生成し、ブラウザを更新します。失敗時は直前の生成物を表示し、修正後に再生成します。終了は Ctrl-C です。

プログラムや入力・出力例のリンクは、本文の上に読み取り専用のプレビューを開きます。全文コピーと元ファイルのダウンロードができ、「閉じる」またはEscで元の位置に戻ります。ZIPは直接ダウンロードします。

CIとリリース処理は `.github/actions/setup-pandoc/action.yml` でPandoc 3.10.2とSHA-256を固定しています。構文強調は `--syntax-highlighting=tango` を使います。

[回割りと方針](design/curriculum-2026.md)、[保守手順](design/maintaining.md)、[レビュー手順](design/quality_guide.md)も参照してください。旧版教材はGit履歴から確認できます。

## ライセンス

教材は [LICENSE-MATERIALS](LICENSE-MATERIALS)、コードは [LICENSE](LICENSE) を参照してください。同梱ソフトウェアは [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) に記載しています。
