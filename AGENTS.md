# AGENTS.md — AI コーディングエージェント向けガイド

このリポジトリは「実践・制約プログラミング」（2026年度）の公開教材である。短い規律は `CLAUDE.md` にある。ここには案内・文書間の関係・コマンドを書く。

> 状態: フェーズ P5（自由課題の支援物）完了。**全15回の原稿と支援物が揃い、公開（P6）のローカル作業も終わっている。残るのは GitHub 側の操作だけである。** サイトのビルド系（`site/` `tools/` `Makefile` `.github/workflows/`）と表示部品は動く。Tau Prolog 同梱の実行ページ（`web/prolog/`）、`materials/references/` の参考資料一式（環境構築・早見表・SAT/SMT 概説・グラフ彩色比較・定式化の7手順・エラー集・用語集・索引）、用語初出台帳 `design/glossary-ledger.md` がある。`tools/check_docs.py` は `concepts` / `glossary` を含む全種別が既定で走る。各回の原稿は**第01回から第15回まで**、進め方ガイドは `materials/guides/how-to-study.md`、演習ファイルは `workbook/sessions/01-prolog-intro/` 〜 `10-roster-verification/` と `workbook/projects/` がある。第11〜15回は自由課題・発表会で、演習3段階を持たない簡略形の H2 構成である（`check_docs.py` の `PROJECT_REQUIRED_H2`）。自由課題の支援物は `materials/projects/`（説明の正本）と `workbook/projects/`（記入用の実体）に分かれている。`site/nav.yaml` に未執筆のコメント行は残っていない。評価ルーブリックと発表練習会の案は非公開 `../cp-practice-design/teacher/rubric/` にある。

## 運用ルール

- コミット・ステージ・push は明示的な許可を得てから行う。コミットメッセージは英語。
- 図は `materials/figures/*.tex`（TikZ）を正本とし、生成した SVG もコミットする。
- 学習者の情報・授業ログ・氏名・ホスト名・IP アドレス・環境固有の識別子を書かない。
- 標準演習の中心部分の解答、発展演習の完成コード、評価ルーブリック、隠しテストは非公開リポジトリ `../cp-practice-design/teacher/` にだけ置く。公開側から参照してよいのは `../cp-practice-design/teacher/` だけで、`planning/` を指さない。
- 教材（原稿ページ）を追加したら `site/nav.yaml` に1行足す。
- 新しい概念・用語を導入するときは、**先に `design/glossary-ledger.md` に1行足してから**原稿の `introduces:` / `requires:` と `materials/references/glossary.md` を直す。順序を逆にすると `make check-docs` が差分を示してくれない。
- 表記は「第NN回」（2桁ゼロ埋め）と「学習者」に統一する。`make check-docs` が違反を検出する。
- 生成物（`.site/` `.pages/` `__pycache__/`）は通常の調査で探索しない。

## ドキュメント一覧

| 文書 | 役割 |
|---|---|
| `README.md` | プロジェクトの入口 |
| `design/curriculum-2026.md` | 全15回の回割り・目標・演習3段階・完了条件の**正本** |
| `design/site-design.md` | 教材サイトの方針（ページ構成・表示部品・公開範囲） |
| `design/prolog-environment.md` | Prolog 実行環境の選定と検証項目 |
| `design/maintaining.md` | 保守手順・表記規約・教材追加の手順・検査の種別・公開とリリース |
| `design/quality_guide.md` | 品質管理と AI レビューの手順 |
| `design/glossary-ledger.md` | 用語初出台帳。どの概念をどの回で導入するかの**正本**。`introduces:` / `requires:` と用語集はここからの導出値 |
| `site/nav.yaml` | サイト構成の単一の出典 |
| `materials/guides/style-sample.md` | 原稿で使える表示部品の見本（書き方と見え方） |
| `tools/doc_check_allowlist.yaml` | 文書検査の除外リスト（理由つき） |
| `THIRD_PARTY_NOTICES.md` | 同梱した第三者ソフトウェア（Tau Prolog）の版・ライセンス・入手元 |

## 資料への導線

| 場所 | 内容 |
|---|---|
| `materials/sessions/` | 各回の原稿（`01-prolog-intro.md` 〜 `15-presentation.md`） |
| `materials/references/` | 参考資料（環境構築・早見表・SAT/SMT 概説・グラフ彩色比較・用語集） |
| `materials/projects/` | 自由課題の案内・企画書 / README / 検証 / 提出 / 発表のテンプレートの**説明**（サイトが正本） |
| `materials/guides/` | 科目の進め方・表示見本 |
| `materials/figures/` | 図の TikZ ソースと生成 SVG（両方コミットする） |
| `workbook/sessions/` | 学習者向け演習ファイル（回ごと） |
| `workbook/projects/` | 自由課題の記入用テンプレート（`proposal.md` `README.md` `experiments.md` `verify.py`）と最小雛形（`minizinc/` `z3/`）。説明は `materials/projects/` 側に置き、ここには記入欄だけを置く |
| `web/prolog/` | Tau Prolog 同梱のブラウザ実行ページ。`index.html` / `app.js` / `style.css` はビルド不要の素の静的ファイル、`vendor/tau-prolog/` は同梱した処理系（触らない）。`app.js` の `SAMPLES` が第01〜02回の題材データの正本で、原稿はここから写す。教材ページからは `../../tools/prolog/?example=<id>` で導線を張る |
| `../cp-practice-design/teacher/` | 非公開: 解答・隠しテスト・ルーブリック・品質記録・教員メモ |

## 目的別の参照順

- ある回の教材を扱う: `design/curriculum-2026.md` の該当回 → `materials/sessions/NN-*.md` → `workbook/sessions/NN-*/`
- 参考資料を扱う: `design/site-design.md` §4 → `materials/references/README.md`（索引）→ 該当ページ
- 用語を足す・直す: `design/glossary-ledger.md` → 該当回の frontmatter → `materials/references/glossary.md`
- レビューする: `design/quality_guide.md` → 非公開 `../cp-practice-design/teacher/quality/`

- 表示部品の書き方を調べる: `materials/guides/style-sample.md` → `site/boxes.lua`
- 検査に落ちた: `design/maintaining.md` の「文書検査」 → `python3 tools/check_docs.py --list-checks`

## ビルドとテスト

依存はサイト生成が Pandoc（検証版 3.10.2）+ PyYAML + Python 3.11 以上、図の生成が
LuaLaTeX + poppler-utils だけである。opam・node・qemu の類は要らない。
CI とリリース処理の Pandoc 版・SHA-256 は `.github/actions/setup-pandoc/action.yml` に固定する。
構文強調には `--syntax-highlighting=tango` を使い、未対応の旧版は更新する。

```bash
make site          # .site/ にサイトを生成
make serve         # 生成して http://127.0.0.1:8000/ で配信（保存で自動再生成）
make check-links   # 内部リンクの検査（先に make site が要る）
make check-docs    # 原稿・配布物の整合検査（frontmatter/nav/structure/codeblock/
                   # figure/style/publish/privacy/numbers/concepts/glossary）
make check         # site → check-links → check-docs をまとめて
make check-publish # 公開範囲と個人情報だけを検査
make figures       # materials/figures/*.tex → SVG（図を変えたときだけ）
make pages VERSION=vX.Y.Z   # 公開物を .pages/ に組み立てて確認
make clean         # .site/ と .pages/ を消す（SVG は消さない）
```

一部の検査だけ動かすときは `python3 tools/check_docs.py --only nav,style` のようにする。
ページ間のリンクはディレクトリ形式なので、`file://` では辿れない。
表示確認は必ず `make serve` を使う。

演習モデル（MiniZinc）と演習コード（Z3）は CI では走らせない。
動作確認はローカルで行い、結果を非公開側の品質記録に残す。
