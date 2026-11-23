# AI作業の入口

2026年度の新版教材を、公開側のファイルを編集しながらレビューしている。まず [README.md](README.md)、[CLAUDE.md](CLAUDE.md)、[回割り](design/curriculum-2026.md) と実際の差分を確認する。移植は人手レビューや授業試行の完了を意味しない。

## 原稿と配布物

- 第01〜10回の本文は `materials/sessions/<URL名>/lesson.md`、発展は同じ場所の `advanced-exercises.md`。手引き・図も回ごとに置く。
- 配布物は `workbook/sessions/<URL名>/`、サイトへ出す一覧は `site/nav.yaml` の `handouts`。
- 回割り・前提・通常演習と自由課題の扱いは `design/curriculum-2026.md`。新しい指示を反映し、旧版の15講義ページや中間提出へ戻さない。
- 表示は `site/`、生成は `tools/build_site.py` と `tools/render_course.py`。ビルドはこのリポジトリだけで完結する。
- 教員用解答・隠しテスト・評価資料・品質記録は非公開の `../cp-practice-design/teacher/` に保持する。公開資料にコピーしない。
- `web/prolog/` のTau Prolog実行ページと `latex/` は旧版の資産を保存している。新版サイトは同梱せず、第01回の手引きに沿ってSWI-PrologまたはSWISHを使う。

## 作業と検査

コミット・ステージ・pushは明示的な許可を得てから行う。未コミット・未追跡の既存成果物を保護し、コミットメッセージは英語にする。第NN回・学習者の表記を使い、個人情報・環境固有情報を書かない。

```sh
make serve          # 保存時に再生成するローカル閲覧
make check          # 生成・参照・構造・表記・配布範囲・個人情報を検査
make check-publish  # 公開範囲と個人情報の検査
make figures        # 図のソースを変更した場合だけ
make pages VERSION=vX.Y.Z # ローカルにリリースを組み立てる
```

Python 3.11以上・PyYAML・Pandoc 3.14で検証する。Pandocの固定値は `.github/actions/setup-pandoc/action.yml` に集約する。
図を変更したらソースとSVGを揃える。具体的な手順は [保守手順](design/maintaining.md)。

モデル・ソルバーの実行と授業試行は静的検査とは別に記録する。レビューは [品質ガイド](design/quality_guide.md) に沿って行う。
