% 第03回 4×4数独 — 穴埋め前のモデル
%
% 教材ページ: 講義（全15回）> 第03回 数独: MiniZincで盤面を解く
% 実行環境:   MiniZinc Playground（ブラウザ）
%
% % TODO の4か所を埋めると、下の初期値どおりの盤面が1つ求まる。
%   TODO(1) TODO(2) が必須演習、TODO(3) TODO(4) が標準演習である。

include "globals.mzn";

% ── パラメータ（あらかじめ分かっている値） ───────────────────────
int: n = 4;                 % 盤面の一辺
int: b = 2;                 % ブロックの一辺（n = b * b）

set of int: DIGITS = 1..n;
set of int: ROWS   = 1..n;
set of int: COLS   = 1..n;

% 初期値。0 は「まだ決まっていないマス」を表す。
% ここは入力データであって、決定変数ではない。
array[ROWS, COLS] of int: given =
  [| 1, 0, 3, 0
   | 0, 0, 0, 2
   | 2, 0, 0, 0
   | 0, 3, 0, 1 |];

% ── 決定変数（ソルバーに決めてもらう値） ─────────────────────────
% 各マスに 1..4 のどれかが入る。定義域を DIGITS に限っているので、
% 「1〜4 以外は入らない」という制約は別に書かなくてよい。
array[ROWS, COLS] of var DIGITS: x;

% ── 制約 ────────────────────────────────────────────────────
% TODO(1) 必須演習: 行制約。
%   すべての行 r について、その行に並ぶ n 個のマスが互いに異なるようにする。
%   ヒントの形: constraint forall(r in ROWS)( all_different([ ... | ... ]) );
% constraint

% TODO(2) 必須演習: 列制約。
%   すべての列 c について、その列に並ぶ n 個のマスが互いに異なるようにする。
% constraint

% TODO(3) 標準演習: ブロック制約。
%   b×b の各ブロックの中で数字が重複しないようにする。
%   ブロックの位置を br・bc（どちらも 0..b-1）、ブロック内の位置を i・j
%   （どちらも 1..b）とすると、そのマスは x[br * b + i, bc * b + j] で指せる。
%   br = 0, bc = 0, i = 1, j = 1 が盤面の左上 x[1, 1] である。
%   ヒントの形: constraint forall(br in 0..b-1, bc in 0..b-1)( all_different([ ... ]) );
% constraint

% TODO(4) 標準演習: 初期値の固定。
%   given[r, c] が 0 でないマスは、その値でなければならない。
% constraint

solve satisfy;

% ── 出力 ────────────────────────────────────────────────────
% 1行ずつ数字を並べ、ブロックの区切りに空行を入れる。
output [
  if c == 1 /\ r != 1 /\ (r - 1) mod b == 0 then "\n" else "" endif
  ++ if c != 1 /\ (c - 1) mod b == 0 then " " else "" endif
  ++ show(x[r, c])
  ++ if c == n then "\n" else " " endif
  | r in ROWS, c in COLS
];
