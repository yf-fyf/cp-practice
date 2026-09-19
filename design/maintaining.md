# 保守手順

## 原稿・配布物をレビューする

`make serve` を起動し、`materials/sessions/<slug>/lesson.md`、`advanced-exercises.md`、`guides/` と対応する `workbook/sessions/<slug>/` を編集する。保存時に全サイトを再生成する。失敗した場合はターミナルのエラーを修正する。`HOST`・`PORT` はMake変数、監視しない場合は `python3 tools/build_site.py --serve --no-watch` を使う。

配布物を追加・削除したら `site/nav.yaml` の該当回の `handouts` も更新する。本文からは実ファイルへの相対リンクを張る。通常回のURL名を変える場合は原稿と配布フォルダー、一覧の `slug`、案内文書を一緒に変更する。

第04回の `session-04.zip` は個別配布ファイルの束。中身を変えたら同じ相対パスでZIPも更新する。配布元との不一致は検査で失敗する。

## 検査

`make check` はサイト生成、全ページのローカルリンク・アンカー・原稿リンク・配布内容、本文/HTML/CSSの構造、コード言語・画像代替テキスト、表記、公開範囲、個人情報を検査する。外部URLの到達性と演習モデルの実行は対象外。

`python3 tools/check_docs.py --list-checks` で検査名を確認できる。`--only publish,privacy` などで限定する。構造検査は先に `make site` が必要。除外は `tools/doc_check_allowlist.yaml` にファイル・該当文字列・種別・理由を指定する。旧版専用のfrontmatter・用語台帳検査は新版では使わない。概念の導入順は原稿と回割りを照合してレビューする。

## 依存と図

サイト生成は Python 3.11以上、PyYAML、Pandoc 3.10.2で確認する。CIとリリースは `.github/actions/setup-pandoc/action.yml` に公式配布版・SHA-256を固定する。旧オプションの互換処理は入れず、`--syntax-highlighting=tango` に対応したPandocを使う。

図のソースとSVGは各回の `figures/` に置く。`make figures` で第04回・第07回のTeX図と第10回のPython図を生成する。第04回・第07回にはLuaLaTeX、TikZ、日本語用パッケージとNoto Sans CJK JP、poppler-utilsが必要。TeX/PythonソースがないSVGはSVG自体を編集する。通常のサイト生成では同梱SVGを使う。

## リリース

`make pages VERSION=vX.Y.Z` で `.pages/` に許可されたサイト・法的表示・配布ZIP・`.nojekyll` を組み立てる。`python3 tools/build_site.py --check-links --output .pages` で組立後も確認できる。ZIPには演習ファイルと参照先の教材原稿・図・ライセンスを同梱する。展開後の入口は `workbook/README.md`。これはローカル操作であり、公開しない。

GitHubのRelease Pagesワークフローは `dev` から手動実行し、確認済みの生成物を `main` へ公開する。ワークフローの実行・pushはメンテナの明示的な公開判断の後に行う。移植・機械検査の完了だけで教材のレビュー完了としない。
