# 保守手順（メンテナ用）

教材の開発・保守を行うときの規約・手順・参考情報。
回割り・各回の目標・演習3段階・完了条件の**正本**は
[`curriculum-2026.md`](./curriculum-2026.md)、サイトの方針は
[`site-design.md`](./site-design.md) である。この文書は「どう作るか」を書く。

---

## ディレクトリ構成

```text
.
├── README.md              プロジェクト入口
├── AGENTS.md              AI エージェント向けガイド
├── CLAUDE.md              短い規律
├── LICENSE                MIT（プログラムコード）
├── LICENSE-MATERIALS      CC BY-NC-SA 4.0（講義資料）
├── THIRD_PARTY_NOTICES.md 同梱した第三者ソフトウェアの版・ライセンス・入手元
├── Makefile               サイト・図・公開物のビルド
├── design/                設計・運用文書（教える側・改変する側向け）
│   ├── curriculum-2026.md 回割り・目標・演習3段階・完了条件の正本
│   ├── site-design.md     教材サイトの方針
│   ├── prolog-environment.md  Prolog 実行環境の選定と検証項目
│   ├── glossary-ledger.md 用語初出台帳（どの概念をどの回で導入するかの正本）
│   ├── maintaining.md     このファイル
│   └── quality_guide.md   教材品質管理・AI レビュー手順
├── materials/             資料の Markdown 原稿（サイトの元）
│   ├── sessions/          各回の原稿 NN-xxx.md
│   ├── references/        参考資料（環境構築・早見表・概説・エラー集・用語集）
│   ├── projects/          自由課題の案内とテンプレートの説明
│   ├── guides/            進め方・表示見本
│   └── figures/           図の TikZ ソースと生成 SVG（両方コミット）
├── latex/                 図の共通プリアンブル（figure-preamble.tex のみ）
├── site/                  資料サイトの構成・テンプレート・スタイル
│   ├── nav.yaml           サイト構成の単一の出典
│   ├── template.html      pandoc の HTML テンプレート
│   ├── boxes.lua          ::: の変換・コードブロック・図と .md リンクの書き換え
│   ├── style.css          配色は latex/figure-preamble.tex と揃える
│   └── lightbox.js        図の拡大表示
├── tools/                 生成・検査スクリプト
│   ├── build_site.py      資料サイトの生成・配信・内部リンク検査
│   ├── build_figures.py   TikZ → SVG
│   ├── build_pages.py     公開物の組み立てと許可リスト検査
│   ├── check_docs.py      原稿・配布物の整合検査
│   └── doc_check_allowlist.yaml   検査の除外リスト（理由つき）
├── web/                   ブラウザ補助ツール（ビルド工程を持たない静的ファイル）
│   └── prolog/            Tau Prolog 実行ページ
│       ├── index.html     画面（プログラム欄・クエリ欄・ボタン・結果欄）
│       ├── app.js         実行の制御（サンプル・スライス実行・中断・エラー表示）
│       ├── style.css      site/style.css と同じ配色を写した単体完結の CSS
│       └── vendor/        同梱した第三者ソフトウェア（触らない）
├── workbook/              学習者向け配布物。この中だけで演習が完結する
│   ├── README.md          入手・実行・演習3段階の案内
│   ├── sessions/          各回の演習ファイル NN-xxx/
│   └── projects/          自由課題の記入用テンプレートと最小雛形
└── .github/workflows/
    ├── ci.yml             サイト生成 + 文書検査
    └── release-pages.yml  公開物を組み立てて main を更新する
```

トップレベルは役割で分割している。

| ディレクトリ | 役割 | 読む人 |
|---|---|---|
| `design/` | 設計思想・保守手順・品質管理 | 教える側・教材を改変する人 |
| `materials/` | 資料の原稿（サイトの元） | 教材を書く人 |
| `workbook/` | 演習の配布物 | 学習者 |
| `site/` + `latex/` + `tools/` | サイトと図のビルドシステム | 教材を書く人 |
| `web/` | ブラウザで動く実行環境 | 学習者 |
| `../cp-practice-design/teacher/` | 非公開リポジトリの解答・隠しテスト・ルーブリック・品質記録 | メンテナ |

### 命名規則

原稿 `materials/sessions/03-minizinc-sudoku.md` と配布物
`workbook/sessions/03-minizinc-sudoku/` は**同じ綴りで対応する**。
`site/nav.yaml` はこの対応をそのまま使うので、写像表は要らない。

- 回番号は2桁ゼロ埋め、区切りはハイフン（`03-minizinc-sudoku`）
- 出力 URL は `/sessions/03-minizinc-sudoku/` になる
- 本文中の回の呼称は「第03回」（2桁ゼロ埋め）

### 設計資料と配布物の書き分け

同じ事実を両方に置かない。`design/` には**なぜそうしたか**だけを書き、
事実の一覧（各回の目標・演習3段階・完了条件・実行手順）は正本を1つに決める。

| 情報 | 正規の置き場所 |
|---|---|
| 回割り・各回の目標・演習3段階・完了条件 | `design/curriculum-2026.md` |
| サイトの章立てとページの並び | `site/nav.yaml` |
| 各回の説明本文・ヒント・完了チェック | `materials/sessions/NN-xxx.md`（サイトが正本） |
| 演習ファイルの実行方法 | `workbook/README.md` と各回の `workbook/sessions/NN-xxx/README.md` |
| 実行環境の使い方 | `materials/references/setup-*.md` |
| 用語の定義と初出位置 | `design/glossary-ledger.md`（台帳）と `materials/references/glossary.md` |

`materials/` は資料の原稿、`workbook/` は学習者向け配布物として扱う。
学習者経路を確認するときは、原則として `workbook/` 内だけを参照する。
演習ファイル内の README には**実行方法と教材ページへのリンクだけ**を書き、
考え方・手順・ヒントは教材ページに置く（`curriculum-2026.md` §11）。

### 用語と表記の統一

同一概念の呼び方を1つに決め、ここだけに書く。他文書に再掲しない
（`tools/check_docs.py` の `style` 検査が違反を検出する）。

| 対象 | 正 | 誤（避ける） | 備考 |
|---|---|---|---|
| 回の呼称 | `第03回`（2桁ゼロ埋め） | `第3回`・`3回目` | ディレクトリ名・ファイル名も2桁ゼロ埋め |
| 学ぶ人の呼称 | `学習者` | `受講者`・`学生` | 非公開側 `teacher/quality/` の記録も対象 |
| 演習の段階 | `必須演習` / `標準演習` / `発展演習` | `基礎`・`応用`・`チャレンジ` | `boxes.lua` の `level` 属性と一致させる |

例外は `tools/doc_check_allowlist.yaml` に理由つきで書く。第07回の題材名
`学生と研究テーマの割当` のように、架空データの登場人物の区分として
その語が正当に現れる箇所がこれにあたる。
一度も一致しなかった除外は「死んだ除外」として検査自身が違反にする。

### 派生する数値を書かない

演習ファイルの本数・コード行数など、修正のたびに増減しうる派生的な数値は、
教材本文（`materials/`・`workbook/`）に新たに書き込まない。数量に触れたいときは
「対応する演習ファイルで確認できる」のように、実測し直さなくても正しさが
保たれる表現へ言い換える。

対象外: 回番号・全15回など教材の骨格を表す数値（書いてよい）。

---

## 資料サイト

`materials/` の原稿と `workbook/README.md` を pandoc で HTML にして
GitHub Pages へ出す。構成は `site/nav.yaml` が単一の出典で、
ページのタイトルは原稿の先頭 H1 から取る。

| 依存 | 何に要るか |
|---|---|
| Pandoc（検証版 3.10.2）、PyYAML、Python 3.11+ | サイトの生成（`make site` / `make serve`） |
| LuaLaTeX（Noto Sans CJK JP / Inconsolata）、poppler-utils の `pdftocairo` | 図の生成（`make figures`） |

**図の SVG はコミット対象**なので、図を触らないなら TeX は要らない。
サイト生成に opam・node・qemu の類は一切要らない。

```bash
make site                # .site/ に全ページを生成
make serve               # 生成して http://127.0.0.1:8000/ で配信（Ctrl-C で終了）
make serve PORT=9000
make serve HOST=tailscale   # 別端末から Tailscale 経由で見る
make serve HOST=0.0.0.0     # 全インターフェース
make check-links         # 内部リンク切れを検査
make check-docs          # 原稿・配布物の整合（下記）
make check-publish       # 公開範囲と個人情報だけを検査
make check               # site → check-links → check-docs をまとめて
make figures             # 図の SVG を作り直す（図を触ったときだけ）
make clean               # .site/ と .pages/ を消す（コミット済みの SVG は消さない）
python3 tools/build_site.py --only 03-   # 1ページだけ作り直す
```

CI（`.github/workflows/ci.yml`）は push のたびに `make site`・`make check-links`・
`make check-docs` を通す。CI とリリース処理（`.github/workflows/release-pages.yml`）は
共通の [Pandoc 導入処理](../.github/actions/setup-pandoc/action.yml) を使い、
[公式配布の Pandoc 3.10.2](https://github.com/jgm/pandoc/releases/tag/3.10.2) を導入する。
Ubuntu の配布版や自動的に変わる最新版に依存せず、版と SHA-256 をこの一か所に固定する。
ダウンロードしたアーカイブを照合してから展開し、その実行ファイルを PATH の先頭へ置く。

ローカルでも検証版の 3.10.2 を推奨する。[公式の導入手順](https://pandoc.org/installing.html)
でインストールし、`pandoc --version` で確認する。構文強調には
`--syntax-highlighting=tango` を使うため、このオプションがない旧版は更新する。
Pandoc を更新するときは共通処理の版・SHA-256 と本書・README・AGENTS の検証版を揃え、
`make check` と `make serve` で生成・表示を確認する。稼働中の `make serve` は起動し直す。
演習モデル（MiniZinc）と演習コード（Z3）は CI では走らせない。
動作確認はローカルで行い、結果を品質記録に残す。

ページ間のリンクは `sessions/03-minizinc-sudoku/` のディレクトリ形式なので、
`file://` で開いても辿れない。ローカルで見るときは必ず `make serve` を使う。

既定は `127.0.0.1` だけに開く。別端末から見るときは `HOST` を指定する。
`HOST=tailscale` は起動のたびに `tailscale ip -4` を引いて `tailscale0` の
アドレスだけにバインドする。`HOST=0.0.0.0` は全インターフェースなので、
**LAN や docker bridge からも見える**。認証は無いので、公開したい範囲に合わせて選ぶ。

`make serve` は原稿を保存すると作り直し、ブラウザを自動で再読み込みする。
再ビルドの範囲は変更内容で変わる。

| 変えたもの | 作り直す範囲 |
|---|---|
| 原稿 `.md` 1本 | そのページだけ（先頭 H1 を変えた場合は全ページ） |
| `site/style.css`・`site/lightbox.js` | 静的ファイルのコピーのみ |
| `site/template.html`・`site/boxes.lua`・`site/nav.yaml` | 全ページ |
| `materials/figures/*.svg` | 図のコピーのみ |

### 表示部品

原稿で使える表示部品は [表示見本](../materials/guides/style-sample.md) に
1ページで並べてある。書き方と見え方はそちらを見る。実装は次の2か所にある。

| 部品 | 実装 |
|---|---|
| `::: note` などのボックス、演習の `level`、`::: {.hint summary=...}` | `site/boxes.lua` の `box_title` / `exercise_level_title` / `Div` |
| コードブロックの言語別名・`filename=` キャプション | `site/boxes.lua` の `lang_alias` / `no_highlight` / `CodeBlock` |
| H2「この回の目標」の枠 | `site/boxes.lua` の `GOAL_HEADING`（`check_docs.py` の同名定数と揃える） |
| 各部品の配色 | `site/style.css`（`latex/figure-preamble.tex` と同じ値を使う） |

MiniZinc は pandoc の構文定義に無いので着色されない（`no_highlight` に入れて
ラベルだけ出す）。着色が要るようになったら、skylighting 用の構文定義 XML を
`site/syntax/minizinc.xml` として自作し、`--syntax-definition` を渡す。

### 図

図は `materials/figures/*.tex`（TikZ）を正本とし、`make figures` で SVG にする。
**`.tex` と `.svg` の両方をコミットする。**

- 共通プリアンブルは `latex/figure-preamble.tex`。各図から `\input{figure-preamble}` する。
- 配色は `site/style.css` と揃える。片方を変えたらもう片方も直す。
- 色そのものが意味を持つ図（グラフ彩色・勤務表）では、**色だけに頼らず記号も併記する**。
- 代替テキストは必須。`check_docs.py` の `figure` 検査が空と極端に短いものを弾く。

```bash
make figures                                   # 全図
python3 tools/build_figures.py graph-          # ファイル名の前方一致で絞る
```

---

## 教材追加の手順

0. その回で**新しく導入する概念**があれば、先に
   [`glossary-ledger.md`](./glossary-ledger.md) に行を足す。
   `introduces:` / `requires:` と `references/glossary.md` は台帳からの導出値なので、
   台帳を直さずに原稿だけを直すと `make check-docs` の `concepts` 検査が落ちる。
1. `materials/sessions/` に Markdown 原稿を書く。
   frontmatter と H2 の標準構成は下記。
2. 図が必要なら `materials/figures/` に TikZ ソースを追加し（`figure-preamble.tex` を
   `\input` する）、`make figures` で SVG を生成して**両方コミットする**。
3. `workbook/sessions/NN-xxx/` に README・穴埋め前のファイル・入力データ・
   動作確認スクリプトを追加する。README には教材ページへのリンクを入れる。
   **Playground の操作手順を README に書き写さない。**手順は
   `references/setup-minizinc.md` の「手順カード（モデル + データ）」1か所だけに置き、
   README からはそれを指してモデルとデータの**ファイル名だけ**を書く
   （Playground の画面が変わったときに直す場所を1つにするため）。
4. **`site/nav.yaml` の該当セクションに原稿のパスを1行足す**
   （新しい回はコメント行になっているので、コメントを外す）。
5. 標準演習の中心部分・発展演習の完成コードは非公開リポジトリ
   `../cp-practice-design/teacher/answers/NN-xxx/` に置き、実際に実行して
   期待どおりに動くことを確かめる。
6. `make check`（`make site && make check-links && make check-docs`）を通す。
7. [`quality_guide.md`](./quality_guide.md) に従いレビューし、記録を残す。
8. 公開する段になったら「公開とリリース」の手順でリリースする。

教材を改名・削除したときも 4 を忘れないこと。
`nav.yaml` に載せ忘れた原稿は `make check-docs` の `nav` 検査が検出する。

### 各回の frontmatter

```yaml
---
session: 3
track: minizinc            # prolog | minizinc | z3 | project | presentation
tools:
  - MiniZinc
description: 数独を題材に、変数・定義域・制約・解の語彙をMiniZinc構文と対応付ける
introduces:                # この回が初出で導入する概念
  - csp_vocabulary
requires:                  # 前提となる概念（台帳からの導出値。手で足し引きしない）
  - declarative_description
---

# 第03回 数独: MiniZincで盤面を解く
```

frontmatter は pandoc がメタデータとして消費するので生成ページには出ない。

- `title:` は**置かない**。原稿の先頭 H1 が正本（`build_site.py` の `read_title()`）。
- `duration:` は**置かない**。全15回が100分で同一である。
- `objectives:` は**置かない**。本文の「## この回の目標」が正本。
- `updated:` は**置かない**。手書きの更新日は必ず腐る。
- `description:` は残す。`<meta name="description">` とホームのカード説明に使う。

### 各回の H2 標準構成

基礎回（第01〜10回）はこの順を原則とする。
`check_docs.py` の `structure` 検査が並び順を見る（間に別の H2 を挟むのは許す）。

```markdown
# 第NN回 タイトル

## この回の目標          ← boxes.lua が .goal で囲む（観察可能な行動で3〜4項目）
## 前提と準備
## 今回解く問題
## 変数・定義域・制約・目的へ分解
## 概念と構文
## 小さな実行例
## 予想してから試す
## 必須演習              ← ::: {.exercise level=required}
## 標準演習              ← ::: {.exercise level=standard}
## 発展演習              ← ::: {.exercise level=advanced}
## よくある誤り
## 完了チェック          ← ::: done のチェックリスト
## 扱わないこと          ← 先送り先を必ずリンクにする
## 次回への接続
```

H1 の直後、`## この回の目標` の前に **「この回の最短ルート」の `::: {.important}` を1つ置く**
（第01〜10回）。授業の100分で最低限やることを5行で書く。書く内容は
「読む節 → 必須演習 → 完了チェック → 自習に回してよいもの」の順である。
`check_docs.py` の `structure` 検査は H2 の並びだけを見るので、この枠は検査に影響しない。

`::: {.important}` は**1回につき3個まで**にする（最短ルートを含めた数）。
それ以上は `note` か `warning` へ落とす。強調が多いと強調が効かなくなる。

学習者が書く必要のないコード（`output` の整形など）は本文に直接置かず、
`::: {.hint summary="...（読まなくてよい）"}` に畳んで `<details>` にする。

第05・06回は `## 概念と構文` の前に `## 理論概説` を置く。

`## この回の進み方`（時間配分の表）を置くのは**第05・06回だけ**である。
`curriculum-2026.md` §10 が個別の時間配分を示しているのがこの2回だけで、
ほかの題材回は §10 の標準配分どおりに進むためである。
題材回に個別の時間配分表を足さない。

第11〜14回（自由課題）と第15回（発表会）は簡略形とし、
`## この回の目標` / `## 今回やること` / `## 支援物` / `## チェックポイント` /
`## 扱わないこと` / `## 次回への接続` に絞る（演習3段階を持たないため）。
第15回だけは送り先が次の回ではないので、末尾を `## この科目のあと` にする。
`check_docs.py` の `structure` 検査は、回番号で基礎回と自由課題回を切り替える
（`PROJECT_REQUIRED_H2` / `PROJECT_H2`）。

自由課題の支援物（`materials/projects/`）は各回の原稿ではないので、
frontmatter は `description` だけでよい。参考資料と同じ扱いである。

### 解答をどこに置くか

`curriculum-2026.md` §2 の「応用演習の解答は公開しない」を、置き場で守る。

| 資産 | 置き場 |
|---|---|
| 基礎的な実行例のコード | 公開 `materials/sessions/*.md` の本文 |
| 必須演習の解答 | 公開 `materials/sessions/*.md` の `::: {.hint}` 最終段 |
| 標準演習の中心部分の完成コード | 非公開 `../cp-practice-design/teacher/answers/` |
| 発展演習の完成コード | 非公開 同上 |
| 隠しテスト・反例データ | 非公開 `../cp-practice-design/teacher/tests/` |
| 評価ルーブリック | 非公開 `../cp-practice-design/teacher/rubric/` |
| 学習者の成績・提出物・出席 | **どちらにも置かない**（授業運用側のリポジトリに残す） |

---

## 文書検査（`make check-docs`）

`tools/check_docs.py` は検出種別ごとに検査を分けている。
一覧は `python3 tools/check_docs.py --list-checks` で出る。

| 種別 | 検査すること |
|---|---|
| `frontmatter` | 各回に `session` / `track` / `description` / `introduces` / `requires` があり、型が正しく、`session` が 1〜15 で重複せず、ファイル名の回番号と一致する |
| `nav` | `nav.yaml` に載っていない `materials/**/*.md` がない。逆に `nav.yaml` の登録先に実体がある。重複掲載がない |
| `structure` | 各回に「この回の目標」「必須演習」「完了チェック」の H2 がある。基礎回は H2 の標準の並びに沿っている |
| `codeblock` | すべてのコードブロックに言語名が付いている。`console` ブロックに実行結果が混ざっていない |
| `figure` | すべての画像に代替テキストがあり、参照先の SVG が実在する |
| `style` | 回の呼称は「第NN回」、学ぶ人の呼称は「学習者」 |
| `publish` | `teacher` を含むパス、`answer` / `solution` / `rubric` を含むファイル名が公開リポジトリに無い。原稿から非公開側へのリンクが無い |
| `privacy` | `/home/` で始まる絶対パス、IP アドレス、学籍番号らしき連続数字が無い |
| `numbers` | 派生する数値（演習ファイルの本数、コード行数）を本文に書いていない |
| `concepts` | 用語初出台帳 `design/glossary-ledger.md` と各回の `introduces:` / `requires:` が一致する。同じ概念が二度「初出」していない。未導入の概念を先取りしていない |
| `glossary` | 台帳の用語が `materials/references/glossary.md` に項目を持ち、初出回への案内がある。用語集に台帳外の項目が無い |

内部リンクの検査は `make check-links`（`build_site.py --check-links`）が担当する。
用語集への `#識別子` リンクのようなページ内アンカーも、生成 HTML の `id` と
突き合わせて検査する（見出しを改名するとリンク元が `(アンカー無し)` で落ちる）。

```bash
make check-docs                              # 既定のチェックすべて
python3 tools/check_docs.py --only nav,style # 一部だけ
python3 tools/check_docs.py --list-allowed   # 除外リストの内容
python3 tools/check_docs.py --list-kinds     # 除外に書ける検出種別
```

除外は `tools/doc_check_allowlist.yaml` に「ファイル + 行の内容（`match`）+
検出種別（`check`）」の3点で書く。行番号では留めない。理由を `reason` に必ず書く。
`status: legitimate`（恒久的に正当）と `status: pending`（未修正）を使い分ける。

---

## 同梱物（web/prolog/vendor/）

Prolog 実行ページは、処理系 **Tau Prolog** を `web/prolog/vendor/tau-prolog/` に
同梱して動かす。**CDN からは読まない**（`design/prolog-environment.md` §5、
外部サービスの可用性に授業を依存させないため）。
版・ライセンス・原著作権表記・入手元は `THIRD_PARTY_NOTICES.md` が正本である。

同梱しているのは配布物のうち次の3ファイルだけで、**改変しない**。

| ファイル | 役割 |
|---|---|
| `modules/core.js` | 処理系本体（構文解析・単一化・探索・組み込み述語） |
| `modules/lists.js` | `member` / `permutation` / `nth1` などのリスト述語 |
| `LICENSE` | BSD 3-Clause License の全文 |

`vendor/` は「こちらが書いた文章ではない」ので `tools/check_docs.py` の検査対象から
外してある（`SKIP_DIRNAMES`）。公開物への混入検査は `tools/build_pages.py` の
`verify_output()` が公開ツリー全体に対して行うので、安全網は残っている。

### 同梱物を更新する手順

1. 配布物を取得して展開する（例: npm レジストリの `tau-prolog-<版>.tgz`）。
2. `modules/core.js`・`modules/lists.js`・`LICENSE` を
   `web/prolog/vendor/tau-prolog/` へ上書きする。他のファイルは持ち込まない。
3. `THIRD_PARTY_NOTICES.md` の版・著作権表記・入手元・同梱ファイル一覧を直す。
   ライセンスが変わっていないかを `LICENSE` の全文で確かめる。
4. `make site` して実行ページを開き、サンプルを全部読み込んで実行する。
   最低限、論理グリッド（4人・3属性）が数秒以内に解けること、
   「次の解」「中断」が効くこと、日本語のアトムが引用符付きで扱えることを見る。
5. 実測値を非公開側の品質記録（`../cp-practice-design/teacher/quality/records/`）へ追記する。

`app.js` は `window.pl` が無いときに「処理系を読み込めない」と表示して
SWISH（外部）へ誘導するので、置き換えに失敗しても白い画面にはならない。

### 実行ページの作り

- **通信をしない。** 画像・フォント・スクリプトを外部から読み込まない
  （favicon も空の `data:` URI にしてある）。
- **長い探索でも画面が固まらない。** `pl.create(limit)` の推論ステップ上限で
  探索を刻み、1スライスの実時間を測って次のスライスのステップ数を調整する
  （`app.js` の `SLICE_TARGET_MS`）。「中断」は再開を止めるだけでよい。
- **サンプルは `app.js` の `SAMPLES`** にある。教材ページからは
  `tools/prolog/?example=<id>` で直接読み込める。id を変えるときは
  `materials/references/setup-prolog.md` の一覧も直す。
- **見た目は `site/style.css` の値を写してある。** 資料サイトの配色を変えたら
  `web/prolog/style.css` も同じ値に直す（実行ページは資料サイトの CSS を読まない）。

---

## 公開とリリース

### ブランチの役割

| ブランチ | 役割 |
|---|---|
| `dev` | 既定ブランチ。原稿・演習ファイル・ビルド系の開発はすべてここで行う |
| `main` | **Release Pages** workflow が生成する公開専用ブランチ。手で編集しない |

GitHub Pages の配信元は `main` のルート（`Deploy from a branch` / `main` / `/(root)`）である。
`main` を手で直しても、次のリリースで丸ごと置き換わって失われる。

### リリース手順

1. `dev` で `make check`（`make site && make check-links && make check-docs`）を通す。
2. `make pages VERSION=vX.Y.Z` でローカルに `.pages/` を組み立て、
   下の**公開前チェックリスト**を実施する。
3. GitHub の **Actions > Release Pages** を開き、ブランチ `dev` を選んで
   `Run workflow` を押し、`version` に `vX.Y.Z`（`v` 付き）を入力する。
4. workflow が、Python の構文検査 → サイト生成 → 内部リンク検査 → 文書検査 →
   許可リスト付きの組み立て → 組み立て後のリンク検査 → ZIP の健全性検査 を通過した
   ときだけ `main` を作り直して force 相当の更新をする。1つでも落ちれば `main` は変わらない。
5. 公開 URL <https://yf-fyf.github.io/cp-practice/> を開き、トップ・任意の回・
   Prolog 実行ページ・ZIP のダウンロードを確認する。

`main` は初回リリースで初めて作られる。Pages の設定はその後で行う（下記）。

版番号は、回や参考資料を足したときにマイナス（`v1.1.0`）、
誤りの修正だけならパッチ（`v1.0.1`）を上げる。ZIP の名前に入るので、
学習者が「どの版を配られたか」を言えるようにするための番号である。

### 公開前チェックリスト

`make pages VERSION=vX.Y.Z` のあと、`.pages/` に対して行う。
1〜4 は機械で確かめられる。5〜7 は人の目でしか確かめられない。

1. **教員用資産の混入がゼロである。**
   `find .pages -path '*teacher*' -o -iname '*answer*' -o -iname '*solution*' -o -iname '*rubric*' | grep -v '^$'` が何も返さない（パスとファイル名の検査。本文中の用語 `optimal_solution` 等は対象外）
   （`build_pages.py` の `verify_output()` も同じことを実行時に見ているが、
   組み立て前に落ちた場合に備えて手でも確かめる）。
2. **個人情報・環境固有識別子が無い。**
   `python3 tools/check_docs.py --only publish,privacy`（原稿側）に加えて、
   公開ツリーに対して `grep -rn -E '/home/|学籍|[0-9]{1,3}(\.[0-9]{1,3}){3}' .pages/` と
   `grep -rn '@' .pages/ --include='*.html'`（メールアドレス）を実行し、
   出たものが教材上正当な出現かを確かめる。
   `check_docs.py` は原稿（`materials/` `workbook/` `design/`）を見るので、
   組み立て後のツリーは grep で見る。
3. **ZIP の中身が意図どおりである。**
   `unzip -l .pages/downloads/cp-practice-workbook-vX.Y.Z.zip` で、
   `workbook/` の README・各回・自由課題の雛形だけが入っていること、
   `teacher` を含むパスが無いことを見る。展開して `verify.py` が動くことも見る。
4. **公開ツリーのトップレベルが許可リストどおりである。**
   `ls -a .pages/` の結果が下の一覧と一致する。
5. **外部リンクが生きている。**
   原稿から外部 URL を集めて `curl -I` で確かめる。
   対象は MiniZinc Playground・MiniZinc ハンドブック・SWISH・Tau Prolog・
   Z3 のドキュメントと PyPI である。リダイレクトは追う（`-L`）。
   CI では検査しない（一時的な障害で赤くなるため）。

   ```bash
   grep -rhoE 'https?://[^)"< ]+' materials/ workbook/ web/ | sed 's/[.,)]*$//' \
     | sort -u | while read -r u; do printf '%s\t' "$u"; \
       curl -sILo /dev/null -w '%{http_code}\n' --max-time 20 "$u"; done
   ```

6. **図が再生成しても変わらない。** 図の `.tex` を触った回だけ、
   `make figures` のあと `git status --short materials/figures/` が空であることを見る。
   差分が出るなら、生成が環境依存になっている（フォント・LaTeX の版）。
7. **実機で見る。** スマートフォンと、Chromium 以外のブラウザ（Firefox / Safari）で、
   トップ・任意の回・Prolog 実行ページ・長い制約式・幅の広い表を確認する。
   `make serve HOST=tailscale` を使えばリリース前に別端末から見られる。

### 公開物の許可リスト

完成解答・隠しテスト・ルーブリック・品質記録は、兄弟の非公開リポジトリ
`../cp-practice-design/teacher/` だけで管理する。公開リポジトリには置かない。

公開物は次の許可リストに限る。

```text
index.html                 サイトのトップ
assets/                    スタイルシート・lightbox.js
figures/                   図の SVG
sessions/ projects/ references/ guides/    資料のページ
tools/                     ブラウザ補助ツール（Tau Prolog 実行ページ）
downloads/*.zip            workbook/ の配布アーカイブ
LICENSE
LICENSE-MATERIALS
THIRD_PARTY_NOTICES.md
.nojekyll
```

この許可リストは `tools/build_pages.py` の `ALLOWED_TOP_LEVEL` としてもコードで
検査している（`verify_output()`）。**リストを変えるときは文書とコードの両方を直す。**

`build_pages.py` は加えて次を実行時に落とす。

- 公開ツリー・配布 ZIP に `teacher` を含むパスがある
- `answer` / `solution` / `rubric` を名前に含むファイルがある
- 許可リスト外のトップレベルがある
- セクションの入口ページや図が1つも無い

配布 ZIP の名前は `cp-practice-workbook-vX.Y.Z.zip` である
（`build_site.py` と `build_pages.py` の `WORKBOOK_ARCHIVE_PREFIX`）。

学習者の個人情報はそもそもこのリポジトリに置かない運用とし、
授業ログ・成績・提出物は授業運用側のリポジトリだけで管理する。

### GitHub の初期設定

初回コミットを `dev` に push したら、GitHub 側で次を設定する。

1. `dev` を既定ブランチにする。
2. **Settings > Actions > General** で workflow の `Read and write permissions` を許可する。
3. **Settings > Pages** で `Deploy from a branch`、ブランチ `main`、フォルダ `/(root)` を選ぶ。
   `main` は最初の **Release Pages** 成功後に作成されるため、その後で設定する。
4. `main` の branch protection は通常利用者の直接 push を禁止し、
   `github-actions[bot]` にだけ release workflow 用の push を許可する。
5. `dev` は通常のレビュー・CI 対象ブランチとして保護する。

**Release Pages** は `dev` を表示中に手動起動し、`v1.0.0` のような版番号を入力する。
workflow はサイト生成・リンク検査・文書検査・許可リスト検査・ZIP 検査を
通過したときだけ `main` を更新する。`main` を手で修正した場合、次回リリースで失われる。

---

## 授業期間中の更新

**全15回の原稿・演習ファイル・参考資料・用語集・自由課題の支援物は揃っている。**
`site/nav.yaml` にコメント行の未執筆ページは残っていない。
以降は、授業で判明した誤り・不足を直して版を重ねる運用に入る。

回ごとの更新は次の順で行う。原稿を直したら必ずリリースまで通す。
`dev` を直しただけでは公開サイトは変わらない。

1. **原稿・演習ファイルを直す**（`materials/` / `workbook/`。
   新しい概念が増えるなら先に `glossary-ledger.md`）。
2. **`site/nav.yaml`** を直す（ページを足す・改名した場合だけ）。
3. **`make check`** を通す。
4. **品質記録**（非公開 `../cp-practice-design/teacher/quality/records/NN.md`）の
   「変更履歴」に1行足す。授業で見つけた問題は「利用後の観察」の表に入れる。
5. **リリース**（上の「リリース手順」）。授業日の直前ではなく、
   前日までに済ませて公開 URL で確認する。

授業ログ・学習者の状況・成績は公開リポジトリにも非公開リポジトリにも書かない。
授業運用側のリポジトリに残す。

年度末には、年度別 URL を切るかどうかを判断する（`site-design.md` §5）。
標準演習の中心部分・発展演習の解答は恒久非公開である。
学習者の成果物は初年度は載せない。

---

## 非公開側との連携

公開リポジトリから見えるのは、兄弟の非公開リポジトリ `../cp-practice-design/` の
`teacher/` だけである。`planning/`（検討過程・内容設計ドラフト・2024年度の旧資料）は
公開側の作業から参照しない。

| 非公開側 | いつ触るか |
|---|---|
| `teacher/answers/sessions/NN-xxx/` | 標準・発展演習を書いた／直したとき。実際に実行して確かめる |
| `teacher/tests/NN-xxx/` | 隠しテスト・反例データを足したとき |
| `teacher/rubric/` | 自由課題・発表の評価を決めたとき。公開側には観点名だけを出す |
| `teacher/notes/NN.md` | 授業の進め方メモ・時間配分・想定質問 |
| `teacher/quality/records/` | 回を作成・改訂したとき（`quality_guide.md` の手順） |
| `tasks/TODO.md` | 作業の区切りごと。未解決の判断待ちもここに集める |

非公開側では AI エージェントがコミットしてよいが、**`git push` はしない**。
公開側は逆で、**明示的な許可なくコミット・ステージ・push をしない**。
`teacher/answers/` の中身を公開側へコピーしない。

---

## 教材の品質管理

教材を作成・レビュー・公開・改善するときは
[`quality_guide.md`](./quality_guide.md) に従う。

教材別の品質状態・レビュー証拠・公開判断は
`../cp-practice-design/teacher/quality/template.md` から記録を作り、
`../cp-practice-design/teacher/quality/records/` に保存する。
記録の単位は**回**で、第08〜10回のように複数回で1つの題材になる束には
束としても1本記録を持つ。
