# 2026年度の回割りと方針

2026-09-19。新版の原稿と配布物をこのリポジトリへ移植した。以後のレビュー・修正は `materials/` と `workbook/` で行う。内容の人手レビュー・授業試行は未完了。

## 対象と目的

Pythonの読み書きと基礎的なプログラミング演習に習熟した学習者を前提とする。命題論理式・真理値表・論理回路は既習。数学の定着や数式への慣れには幅があり、Prolog・MiniZinc・Z3と制約モデル化は授業で導入する。

示された問題の条件から変数・定義域・制約・必要なら目的を選び、解いて結果を説明することを目指す。

## 回割り

全15回、各100分。通常回の本文・目標・演習の詳細は以下の原稿を正本とする。

| 回 | 本文 | 配布物 |
|---|---|---|
| 第01回 | [第01回　Prologで関係を書く](../materials/sessions/01-prolog/lesson.md) | [演習ファイル](../workbook/sessions/01-prolog/) |
| 第02回 | [第02回　MiniZincで小さな数独を解く](../materials/sessions/02-minizinc/lesson.md) | [演習ファイル](../workbook/sessions/02-minizinc/) |
| 第03回 | [第03回　候補を減らし、場合分けして解く](../materials/sessions/03-search/lesson.md) | [演習ファイル](../workbook/sessions/03-search/) |
| 第04回 | [第04回　ルールを制約にして、パズルを作る](../materials/sessions/04-rules/lesson.md) | [演習ファイル](../workbook/sessions/04-rules/) |
| 第05回 | [第05回　講座の割当を0/1の表で表す](../materials/sessions/05-assignment/lesson.md) | [演習ファイル](../workbook/sessions/05-assignment/) |
| 第06回 | [第06回　目的関数で良さを比べる](../materials/sessions/06-optimization/lesson.md) | [演習ファイル](../workbook/sessions/06-optimization/) |
| 第07回 | [第07回　勤務表を数理モデルとして解く](../materials/sessions/07-schedule/lesson.md) | [演習ファイル](../workbook/sessions/07-schedule/) |
| 第08回 | [第08回　希望の上限と、最小化する指標](../materials/sessions/08-preferences/lesson.md) | [演習ファイル](../workbook/sessions/08-preferences/) |
| 第09回 | [第09回　SATで依存・排他・選択を扱う](../materials/sessions/09-sat/lesson.md) | [演習ファイル](../workbook/sessions/09-sat/) |
| 第10回 | [第10回　SMTで作業の日程を組む](../materials/sessions/10-smt/lesson.md) | [演習ファイル](../workbook/sessions/10-smt/) |

第11〜15回は個別の自由課題。「日常に出会う、自分が興味がある対象や問題について、それを数理的にモデル化し、制約プログラミングによって問題を解決せよ」を課題とする。固定の工程・共通の中間提出・発表だけの回は設けない。

## 通常回の進め方

解説・実装実演の後、解説例と同程度の必修1、一段難しい必修2、発展へ進む。各回の発展は3問あり、関心や残り時間に応じて選ぶ。既存題材を使う選択演習もこの枠で扱う。全題の完了は求めず、発展を次の通常回の前提にしない。

通常演習の提出・宿題・完了報告・教員の完了承認は設けない。自己確認は理解と結果を確かめるためのもの。未完分や環境準備を必須の授業外作業にしない。

提出は最終課題のみ、評価は合否。提出方法は未確定で、決まり次第案内する。環境説明の最終整備と授業試行は別途行う。
