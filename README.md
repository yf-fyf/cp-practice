# 実践・制約プログラミング

[![code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](./LICENSE)
[![materials: CC BY-NC-SA 4.0](https://img.shields.io/badge/materials-CC%20BY--NC--SA%204.0-lightgrey.svg)](./LICENSE-MATERIALS)

問題を「変数・定義域・制約・目的」へ分解し、ソルバーに解かせる考え方を、Prolog → MiniZinc → SAT/SMT（Z3）の順に身につける演習教材（全15回・各100分）。

> **状態**: 初版準備中（v1.0.0 リリース前）。全15回の原稿・演習ファイル・参考資料・
> 用語集・自由課題の支援物と、サイトのビルド系・Prolog 実行ページは揃っている。
> 残っているのは GitHub 上での公開作業だけである。
> 公開サイトは <https://yf-fyf.github.io/cp-practice/> を予定しており、
> 最初のリリース（`v1.0.0`）以降に閲覧できるようになる。

## 特徴

- **同じ手順を題材を変えて繰り返す。** 論理グリッドパズル・数独・パッケージ依存関係・
  テーマ割当・勤務表と題材を変えながら、「定式化 → 実行 → 検証」を毎回通す。
  後半は各自の問題を定式化する自由課題に充てる
- **道具の違いを縦断して見る。** グラフ彩色を Prolog・MiniZinc・SAT 符号化の3通りで
  書き比べ、同じ問題が道具ごとにどう見えるかを扱う
- **環境構築で授業を止めない。** Prolog と MiniZinc はブラウザ上で実行する
  （Tau Prolog を同梱した実行ページ／MiniZinc Playground）。SAT/SMT だけ Python + Z3 を使う
- **演習は必須・標準・発展の3段階。** 必須演習には完了条件と段階的ヒントを付け、
  欠席時・復習時にも自力で再現できるようにしてある
- **対象**: Python の経験があれば履修できる。論理回路（AND/OR/NOT）程度の知識を前提とし、
  命題論理・Prolog・MiniZinc の経験は仮定しない

回割り・各回の目標・演習3段階・完了条件の**正本**は
[`design/curriculum-2026.md`](./design/curriculum-2026.md) である。

## はじめかた

**学習者**は、演習ファイルの入手と実行を [`workbook/README.md`](./workbook/README.md) から
始める。本文はすべて公開サイト（<https://yf-fyf.github.io/cp-practice/>）にあり、
そちらが正本である。演習ファイルはサイトの `downloads/` から ZIP でも取得できる。

**教える側・教材を改変する人**は、次の順で読む。

1. [`design/curriculum-2026.md`](./design/curriculum-2026.md) — 回割りと各回の目標
2. [`design/site-design.md`](./design/site-design.md) — サイトが何を満たすか
3. [`design/maintaining.md`](./design/maintaining.md) — どう作り、どう公開するか

## リポジトリ構成

| パス | 内容 | 読む人 |
|------|------|--------|
| [`workbook/`](./workbook/README.md) | 演習の配布物（演習ファイル・実行環境の案内） | 学習者 |
| `materials/` | 資料の Markdown 原稿と図の TikZ ソース | 教材を書く人 |
| [`design/`](./design/curriculum-2026.md) | カリキュラム設計書・サイト方針・環境選定・保守手順・品質管理 | 教える側・改変する人 |
| `site/` / `tools/` / `latex/` | 資料サイトと図のビルドシステム | 教材を書く人 |
| `web/prolog/` | ブラウザで動く Prolog 実行ページ（Tau Prolog 同梱） | 学習者 |
| [`AGENTS.md`](./AGENTS.md) | AI コーディングエージェント向けガイド | — |

完成解答・隠しテスト・評価ルーブリック・品質記録は、このリポジトリには置かない。
非公開リポジトリ `cp-practice-design` で管理する。

## 資料サイトを自前でビルドする場合

サイトの生成に要るのは pandoc・PyYAML・Python 3.11 以上だけである。

```bash
make site     # .site/ にサイトを生成
make serve    # 生成して http://127.0.0.1:8000/ で配信
make check    # 生成 → 内部リンク検査 → 文書検査
```

ページ間のリンクはディレクトリ形式なので `file://` では辿れない。
ローカルで見るときは `make serve` を使う。

図を作り直すときだけ LuaLaTeX と poppler-utils が要る（`make figures`）。
生成した SVG はコミットしてあるので、図を触らないなら不要である。
手順の詳細は [`design/maintaining.md`](./design/maintaining.md) にある。

## 公開とリリース

開発は既定ブランチの `dev` で行う。GitHub Pages 用の `main` は手動リリースで
生成する公開専用ブランチであり、直接編集しない。Pages には資料サイト、
Prolog 実行ページ、`workbook/` 全体の ZIP を置く。

GitHub Actions の **Release Pages** を `dev` から手動実行し、`v1.0.0` のような
リリース番号を指定する。ローカルで公開物を確認する場合は、リポジトリルートから次を実行する。

```bash
make pages VERSION=v1.0.0
# .pages/index.html を開く。配信するのは .pages/ の内容だけ
```

公開物は許可リスト方式で組み立て、教員用資産や個人情報が混ざっていないかを
実行時に検査する。公開前チェックリストは
[`design/maintaining.md`](./design/maintaining.md) にある。

## ライセンス

プログラムコードは [MIT](./LICENSE)、講義資料（本文・図・設計文書）は [CC BY-NC-SA 4.0](./LICENSE-MATERIALS)。

Prolog 実行ページには第三者ソフトウェア **Tau Prolog 0.3.4（BSD 3-Clause）** を `web/prolog/vendor/` へ同梱している。版・ライセンス・原著作権表記・入手元は [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md) に記載してある。
