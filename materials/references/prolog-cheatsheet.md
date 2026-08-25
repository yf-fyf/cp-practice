---
description: 第01〜02回で使うProlog構文の早見表。事実・規則・クエリ・変数・リスト・member・permutation・非等号を、初出回への案内つきで1ページにまとめる
---

# Prolog 早見表

第01〜02回で**実際に使う書き方だけ**を並べてある。
Prolog の全機能ではない。実行のしかたは
[Prolog 実行環境の使い方](setup-prolog.md)を見る。

::: note
この表の「初出」は、その書き方を最初に使う回である。
まだ習っていない書き方は、この表にも載せていない。
:::

## 一覧

| 書き方 | 読み | 初出 |
|---|---|---|
| `drinks(aoi, cocoa).` | 事実 | [第01回](../sessions/01-prolog-intro.md) |
| `X` `Y` `People` | 変数（大文字始まり） | [第01回](../sessions/01-prolog-intro.md) |
| `aoi` `cocoa` `brass_band` | アトム（小文字始まり） | [第01回](../sessions/01-prolog-intro.md) |
| `_` | 無名変数（値はどうでもよい） | [第01回](../sessions/01-prolog-intro.md) |
| `頭部 :- 条件1, 条件2.` | 規則。`,` は「かつ」 | [第01回](../sessions/01-prolog-intro.md) |
| `% 説明` | コメント（行末まで） | [第01回](../sessions/01-prolog-intro.md) |
| `[a, b, c]` | リスト | [第02回](../sessions/02-prolog-modeling.md) |
| `member(X, [a, b, c])` | リストから1つ選ぶ | [第02回](../sessions/02-prolog-modeling.md) |
| `permutation([a, b, c], L)` | 並べ替えを作る | [第02回](../sessions/02-prolog-modeling.md) |
| `X \= Y` | 等しくない | [第02回](../sessions/02-prolog-modeling.md) |
| `p(aoi, cocoa, photo)` | 複数の属性を1つにまとめた項 | [第02回](../sessions/02-prolog-modeling.md) |
| `People = [p(aoi, D, C)]` | 左右を結びつける（単一化） | [第02回](../sessions/02-prolog-modeling.md) |
| `:- use_module(library(lists)).` | `member` などを使う宣言 | [第02回](../sessions/02-prolog-modeling.md) |

## 事実・規則・クエリ

**事実**は「成り立っていること」を1行で書く。ピリオドで終わる。

```{.prolog filename="事実"}
drinks(aoi, cocoa).
club(aoi, photo).
```

**規則**は「条件が成り立てば頭部も成り立つ」と書く。`:-` は「ならば」を右から左に書いたもの、
`,` は「かつ」である。

```{.prolog filename="規則"}
% X と Y が同じサークル C に属していれば、2人は teammate である
teammate(X, Y) :- club(X, C), club(Y, C).
```

**クエリ**は実行ページのクエリ欄に1行で書く。末尾のピリオドは省略してよい。

| クエリ | 意味 | 結果の例 |
|---|---|---|
| `drinks(aoi, cocoa)` | 成り立つか | `true.` |
| `drinks(aoi, X)` | `aoi` は何を飲むか | `X = cocoa.` |
| `drinks(X, cocoa)` | ココアを飲むのは誰か | `X = aoi.`（「次の解」で続きが出る） |
| `drinks(X, cocoa), club(X, photo)` | 両方を満たす `X` | `X = aoi.` |

## アトムと変数

先頭の文字だけで区別する。**綴りではなく大文字・小文字が意味を持つ。**

| 書き方 | 種類 | 例 |
|---|---|---|
| 小文字で始まる | アトム（固有の名前） | `aoi` `cocoa` `brass_band` |
| 大文字か `_` で始まる | 変数（値がまだ決まっていない） | `X` `Drink` `_` |
| 引用符で囲む | アトム（記号や日本語を含められる） | `'コーヒー'` `'A組'` |

`_`（アンダースコア1文字）は**無名変数**で、「何でもよい」を表す。
同じ節の中に `_` を何度書いても、それぞれ別の値でよい。

```{.prolog filename="無名変数"}
% 飲み物は問わず、写真部の人を探す
photo_member(X) :- club(X, photo), drinks(X, _).
```

## リストと `member`

リストは `[` `]` で囲んで書く。`member/2` は
「リストの要素を1つずつ返す」述語で、候補の生成に使う。

```{.prolog filename="候補を作る"}
:- use_module(library(lists)).

drink(D) :- member(D, [coffee, tea, cocoa]).
club(C)  :- member(C, [tennis, brass_band, photo]).
```

`drink(X)` を実行して「次の解」を押すと、`coffee` → `tea` → `cocoa` と順に出る。

::: warning
実行ページ（Tau Prolog）では、`member` や `permutation` を使う前に
`:- use_module(library(lists)).` を書く。
書き忘れると `existence_error(procedure, member/2)` になる。
:::

## 生成とテスト

候補を作ってから条件で落とす、という2段構えの書き方である。
第02回の中心になる形なので、形ごと覚えてよい。

```{.prolog filename="生成してから絞り込む"}
% 生成: 候補を作る
% テスト: 条件に合わないものを落とす
pair(D, C) :-
    drink(D),          % 生成
    club(C),           % 生成
    D \= tea,          % テスト
    C \= tennis.       % テスト
```

`\=` は「等しくない」である。手掛かりが「〜ではない」の形のときに使う。

## `permutation` で重複を作らない

「4人に4種類の飲み物を1つずつ、重複なく割り当てる」ときは、
`permutation/2` で並べ替えとして生成する。
こう書けば「同じ飲み物が2人に当たらない」ことを**別の条件として書かなくてよい**。

```{.prolog filename="並べ替えで割り当てる"}
:- use_module(library(lists)).

assign(D1, D2, D3, D4) :-
    permutation([coffee, tea, cocoa, juice], [D1, D2, D3, D4]).
```

## 生成の順序が速さを決める

条件は**書いた順に**試される。
「全部の属性を生成してから手掛かりを試す」と候補が爆発する。
**1つ生成するたびに、その属性で分かる手掛かりを試す**と桁違いに速くなる。

```{.prolog filename="遅い書き方（すべて生成してから絞る）"}
slow(People) :-
    People = [p(aoi, D1, C1), p(hikaru, D2, C2), p(tsubasa, D3, C3)],
    permutation([coffee, tea, cocoa], [D1, D2, D3]),
    permutation([tennis, photo, art], [C1, C2, C3]),
    % 手掛かりはすべてこの後で試す
    member(p(hikaru, coffee, _), People),
    member(p(_, coffee, tennis), People),
    member(p(aoi, _, AoiClub), People),
    AoiClub \= photo.
```

```{.prolog filename="速い書き方（生成のたびに絞る）"}
fast(People) :-
    People = [p(aoi, D1, C1), p(hikaru, D2, C2), p(tsubasa, D3, C3)],
    permutation([coffee, tea, cocoa], [D1, D2, D3]),
    member(p(hikaru, coffee, _), People),      % 飲み物で分かる手掛かりをここで試す
    permutation([tennis, photo, art], [C1, C2, C3]),
    member(p(_, coffee, tennis), People),      % サークルが決まってから試す
    member(p(aoi, _, AoiClub), People),
    AoiClub \= photo.
```

どちらも同じ解を返す。違うのは**試す候補の数**である。
属性が3つ4つと増えるほど差が開き、遅い書き方は授業時間内に終わらなくなる。

実行ページの[5人・4属性のサンプル](../../tools/prolog/?example=logic-grid-5)が、
この順序で書いた例である。

## 実行環境の操作

| やりたいこと | 操作 |
|---|---|
| プログラムを読み込んで解を1つ出す | 「実行（ロード＋問い合わせ）」 |
| 次の解を見る | 「次の解」 |
| 長い探索を止める | 「中断」 |
| サンプルを直接開く | `../../tools/prolog/?example=<名前>` |

サンプルの名前と、結果の読み方は
[Prolog 実行環境の使い方](setup-prolog.md)にある。

## この科目では使わない書き方

次の記法は Prolog でよく見かけるが、第01〜02回では**使わない**。
動きが分かりにくくなるためである。

| 書き方 | 何をするもの | 代わりに |
|---|---|---|
| `\+` | 否定（失敗としての否定） | `\=` と条件の書き分けで足りる |
| `!` | カット（バックトラックの打ち切り） | 使わない |
| `is` / `=:=` | 算術 | 数値を扱う題材は MiniZinc・Z3 で扱う |
| 再帰による述語の定義 | リスト処理の自作 | `member` `permutation` を使う |

## 関連ページ

- [Prolog 実行環境の使い方](setup-prolog.md) — 操作・結果の読み方・日本語入力の注意
- [よくあるエラーと対処](errors.md) — `syntax_error` `existence_error` などの読み方
- [グラフ彩色の3つの表現](graph-coloring.md) — 同じ問題を Prolog・MiniZinc・Z3 で書き比べる
- [用語集](glossary.md) — 事実・規則・単一化・バックトラックなどの定義
