% 第04回 数独（盤面を差し替えられる共通モデル） — 穴埋め前
%
% 教材ページ: 講義（全15回）> 第04回 数独: データ分離、列挙、一意性
% 実行環境:   MiniZinc Playground（ブラウザ）
%
% 第03回の sudoku4.mzn を、盤面を外から受け取れる形に直したものである。
% 制約はすでに書いてある（第03回で完成させたものと同じ）。
% この回で埋めるのは TODO(1) と TODO(2) の2か所だけである。

include "globals.mzn";

% ── パラメータ ──────────────────────────────────────────────
% TODO(1) 必須演習: 盤面の大きさを .dzn から受け取れるようにする。
%   下の2行は値まで書いてあるので、.dzn 側で差し替えられない。
%   「値を書かない宣言」に直す。
int: n = 4;                 % 盤面の一辺
int: b = 2;                 % ブロックの一辺（n = b * b）

set of int: DIGITS = 1..n;
set of int: ROWS   = 1..n;
set of int: COLS   = 1..n;

% TODO(2) 必須演習: 初期値も .dzn から受け取れるようにする。
%   下の宣言から `= [| ... |]` の部分を外し、宣言だけに直す。
array[ROWS, COLS] of int: given =
  [| 1, 0, 3, 0
   | 0, 0, 0, 2
   | 2, 0, 0, 0
   | 0, 3, 0, 1 |];

% ── 決定変数 ────────────────────────────────────────────────
array[ROWS, COLS] of var DIGITS: x;

% ── 制約（第03回で完成させたもの。この回では触らない） ──────────
constraint forall(r in ROWS)( all_different([ x[r, c] | c in COLS ]) );

constraint forall(c in COLS)( all_different([ x[r, c] | r in ROWS ]) );

constraint forall(br in 0..b-1, bc in 0..b-1)(
  all_different([ x[br * b + i, bc * b + j] | i in 1..b, j in 1..b ])
);

constraint forall(r in ROWS, c in COLS)(
  given[r, c] != 0 -> x[r, c] = given[r, c]
);

% ── 第2解の探索（標準演習で使う） ────────────────────────────
% 次の2行のコメントを外し、.dzn に `found = [| ... |];` を足すと、
% 「found と1マス以上ちがう解」だけを探すようになる。
% 第2解を調べ終わったら、またコメントに戻す。
%
% array[ROWS, COLS] of int: found;
% constraint exists(r in ROWS, c in COLS)( x[r, c] != found[r, c] );

solve satisfy;

% ── 出力 ────────────────────────────────────────────────────
% 前半は人が読むための盤面、後半は .dzn へそのまま貼れる `found` の行である。
output [
  if c == 1 /\ r != 1 /\ (r - 1) mod b == 0 then "\n" else "" endif
  ++ if c != 1 /\ (c - 1) mod b == 0 then " " else "" endif
  ++ show(x[r, c])
  ++ if c == n then "\n" else " " endif
  | r in ROWS, c in COLS
] ++ [
  "\n% 第2解を調べるときは、ここから下を .dzn へ写す\nfound = [| "
] ++ [
  show(x[r, c])
  ++ (if c == n then (if r == n then " |];\n" else "\n         | " endif)
      else ", " endif)
  | r in ROWS, c in COLS
];
