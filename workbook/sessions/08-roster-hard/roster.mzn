% 第08回 勤務表: ハード制約 — 穴埋め前
%
% 教材ページ: 講義（全15回）> 第08回 勤務表: ハード制約
% 実行環境:   MiniZinc Playground（ブラウザ）
%
% データは small.dzn（4人・3日）と week.dzn（8人・7日）にある。
% モデルはどちらでも動く。TODO を埋めて、実行するデータを切り替える。
%
% ここに出てくる職場・職員・勤務規則はすべて架空である。

% ── データから受け取るもの（値は .dzn 側にある） ──────────────
int: ns;                                  % 職員の人数
int: nd;                                  % 日数

set of int: STAFF = 1..ns;
set of int: DAYS  = 1..nd;

array[STAFF] of string: sname;            % 職員の表示名
array[STAFF] of bool: leader;             % リーダー資格を持つか
array[DAYS]  of int: need_day;            % その日に必要な日勤の人数
array[DAYS]  of int: need_night;          % その日に必要な夜勤の人数

% ── シフトの種類 ──────────────────────────────────────────
% 値そのものに名前を付ける。1（日勤）2（夜勤）3（休み）と番号で覚えなくてよい。
enum SHIFTS = { day, night, off };

% 表示用の1文字。SHIFTS の宣言と同じ並びにする。
array[SHIFTS] of string: mark = ["日", "夜", "休"];

% ── 決定変数 ──────────────────────────────────────────────
% 職員1人・1日につきマスが1つ。マスの値は3つのシフトのうちどれか1つ。
% 「1人1日1シフト」は、この書き方そのものが保証している（制約に書かない）。
array[STAFF, DAYS] of var SHIFTS: roster;

% ── 制約 ──────────────────────────────────────────────────
% TODO(1) 必須演習: 必要人数制約を書く。
%   どの日についても、日勤の人数はちょうど need_day[d] で、
%   夜勤の人数はちょうど need_night[d] である。
%   「その日の列」は [ roster[s, d] | s in STAFF ] で取り出せる。
% constraint forall(d in DAYS)( ... );
% constraint forall(d in DAYS)( ... );

% ── 標準演習: ここから下を足す ───────────────────────────────
% TODO(2) 資格制約。どの日も、夜勤に入る人のうち1人以上がリーダー資格を持つ。
%   資格を持つ人だけを取り出すには、内包表記に where を付ける。
% constraint forall(d in DAYS)( ... );

% TODO(3) 休息制約。夜勤に入った翌日は休みにする。
%   d の翌日は d + 1 である。d を動かす範囲に注意する（最終日の翌日は無い）。
% constraint forall(s in STAFF, d in ...)( ... );

solve satisfy;

% ── 出力 ──────────────────────────────────────────────────
% 表と、日ごとの人数と、夜勤に入った資格者の人数を出す。
% 制約を書き忘れていても解は出る。必ずこの数字で確かめること。
output
  [ "        " ++ concat([ show(d) ++ "日 " | d in DAYS ]) ++ "\n" ]
  ++ [ "職員" ++ sname[s] ++ "   "
       ++ concat([ mark[fix(roster[s, d])] ++ "  " | d in DAYS ]) ++ "\n"
     | s in STAFF ]
  ++ [ "日勤    "
       ++ concat([ show(count([ roster[s, d] | s in STAFF ], day)) ++ "   " | d in DAYS ])
       ++ "\n" ]
  ++ [ "夜勤    "
       ++ concat([ show(count([ roster[s, d] | s in STAFF ], night)) ++ "   " | d in DAYS ])
       ++ "\n" ]
  ++ [ "資格者  "
       ++ concat([ show(count([ roster[s, d] | s in STAFF where leader[s] ], night)) ++ "   "
                 | d in DAYS ])
       ++ "\n" ];
