# 同梱する第三者ソフトウェアの表記

この教材リポジトリは、ブラウザ用の Prolog 実行ページ（`web/prolog/`）のために
次の第三者ソフトウェアを**そのままの形で同梱**している。
公開サイトでも同じファイルを配信し、CDN や外部サービスからは読み込まない
（`design/prolog-environment.md` §5、`design/maintaining.md` の「同梱物」）。

本リポジトリ自身のライセンスは、プログラムコードが [MIT](./LICENSE)、
講義資料が [CC BY-NC-SA 4.0](./LICENSE-MATERIALS) である。
下記の同梱物には、それぞれのライセンスが適用される。

---

## Tau Prolog

| 項目 | 内容 |
|---|---|
| 名称 | Tau Prolog |
| バージョン | 0.3.4 |
| ライセンス | BSD 3-Clause License |
| 著作権表記 | Copyright (c) 2017-2020, José Antonio Riaza Valverde. All rights reserved. |
| 入手元 | npm レジストリの配布物 `tau-prolog-0.3.4.tgz`（`https://registry.npmjs.org/tau-prolog/`） |
| 開発元 | `https://github.com/tau-prolog/tau-prolog` ／ `http://tau-prolog.org/` |
| 同梱場所 | `web/prolog/vendor/tau-prolog/` |
| 同梱したファイル | `modules/core.js`（処理系本体）、`modules/lists.js`（`member`・`permutation` 等のリスト述語）、`LICENSE` |
| 改変の有無 | 無し（配布物のファイルをそのまま置いている） |

ライセンス条項の全文は `web/prolog/vendor/tau-prolog/LICENSE` にある。
BSD 3-Clause License は、著作権表示・条件・免責事項を再配布物に添えることを求めており、
本ファイルと同梱の `LICENSE` がそれにあたる。

配布物には他にも `charsio` `concurrent` `dom` `format` `js` `os` `promises` `random`
`statistics` の各モジュールがあるが、第01〜02回の教材では使わないので同梱していない。

---

## 同梱していないもの

- **SWISH（SWI-Prolog のオンライン実行環境）** は外部サービスであり、
  参考資料からリンクするだけで同梱しない（`design/prolog-environment.md` §3.3）。
- 2024年度版の実行ページが使っていた jQuery・milligram・CodeMirror は**引き継いでいない**。
  実行ページの UI は自前の HTML・CSS・JavaScript だけで書いてある。

## KaTeX

- Version: 0.18.7
- Source: https://github.com/KaTeX/KaTeX
- License: MIT（`site/vendor/katex/LICENSE`）
- Files: `site/vendor/katex/`。サイト生成時に `assets/katex/` へコピーする。
