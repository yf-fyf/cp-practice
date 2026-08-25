% 第09回 勤務表: ソフト制約と公平性 — 穴埋め前
%
% 教材ページ: 講義（全15回）> 第09回 勤務表: ソフト制約と公平性
% 実行環境:   MiniZinc Playground（ブラウザ）
%
% 第08回の roster.mzn を拡張したものである。
% ハード制約の3本は**すでに書いてある**（第08回の答えそのもの）。
% この回で足すのは、なるべく守りたい条件（ソフト制約）と目的関数である。
%
% データは small_pref.dzn（4人・3日）と week_pref.dzn（8人・7日）にある。
% ここに出てくる職場・職員・勤務規則・希望はすべて架空である。

% ── データから受け取るもの ────────────────────────────────
int: ns;
int: nd;

set of int: STAFF = 1..ns;
set of int: DAYS  = 1..nd;

array[STAFF] of string: sname;
array[STAFF] of bool: leader;
array[DAYS]  of int: need_day;
array[DAYS]  of int: need_night;

array[STAFF, DAYS] of bool: want_off;     % 希望休。true = その日は休みたい

int: w_pref;                              % 希望休違反1件あたりの重み
int: w_fair;                              % 勤務日数の偏り1あたりの重み
int: w_night;                             % 夜勤回数の偏り1あたりの重み

% ── シフトの種類 ──────────────────────────────────────────
enum SHIFTS = { day, night, off };
array[SHIFTS] of string: mark = ["日", "夜", "休"];
array[SHIFTS] of string: code = ["D", "N", "O"];    % 検証用の1文字

% ── 決定変数 ──────────────────────────────────────────────
array[STAFF, DAYS] of var SHIFTS: roster;

% ── ハード制約（第08回で書いたもの。破ったら勤務表として無効） ────
constraint forall(d in DAYS)(
  count([ roster[s, d] | s in STAFF ], day) = need_day[d]
);
constraint forall(d in DAYS)(
  count([ roster[s, d] | s in STAFF ], night) = need_night[d]
);
constraint forall(d in DAYS)(
  count([ roster[s, d] | s in STAFF where leader[s] ], night) >= 1
);
constraint forall(s in STAFF, d in 1..nd - 1)(
  roster[s, d] = night -> roster[s, d + 1] = off
);

% ── 数えておく値 ──────────────────────────────────────────
array[STAFF] of var 0..nd: works =        % 職員 s の勤務日数
  [ sum(d in DAYS)( bool2int(roster[s, d] != off) ) | s in STAFF ];

array[STAFF] of var 0..nd: nights =       % 職員 s の夜勤の回数
  [ count([ roster[s, d] | d in DAYS ], night) | s in STAFF ];

% ── ソフト制約のペナルティ ────────────────────────────────
% TODO(1) 必須演習: 希望休違反の件数 pref を定義する。
%   want_off[s, d] が true の日に、職員 s が休み以外なら違反1件である。
%   内包表記の where で希望休の日だけに絞れる。
% var int: pref = sum(s in STAFF, d in DAYS where want_off[s, d])( ... );

% TODO(2) 必須演習: 勤務日数の偏り unfair を定義する。
%   いちばん多い人の勤務日数と、いちばん少ない人の勤務日数の差である。
% var int: unfair = ...;

% TODO(3) 標準演習: 夜勤回数の偏り night_unfair を定義する。
% var int: night_unfair = ...;

% ── 目的関数 ──────────────────────────────────────────────
% TODO(1)(2)(3) を書いたら、次の2行のコメントを外して solve を差し替える。
% var int: penalty = w_pref * pref + w_fair * unfair + w_night * night_unfair;

solve satisfy;
% solve minimize pref;         % 必須演習その1
% solve minimize penalty;      % 必須演習その2・標準演習

% ── 出力 ──────────────────────────────────────────────────
% 希望休の日には * が付く。* の付いたマスが「休」でなければ違反である。
output
  [ "        " ++ concat([ show(d) ++ "日 " | d in DAYS ]) ++ "  勤務  夜勤\n" ]
  ++ [ "職員" ++ sname[s] ++ "   "
       ++ concat([ (if want_off[s, d] then "*" else " " endif)
                   ++ mark[fix(roster[s, d])] ++ " " | d in DAYS ])
       ++ "   " ++ show(works[s]) ++ "     " ++ show(nights[s]) ++ "\n"
     | s in STAFF ]
  % 第10回の検証プログラムが読む行。書式は変えないこと。
  ++ [ "#size " ++ show(ns) ++ " " ++ show(nd) ++ "\n" ]
  ++ [ "#shift " ++ sname[s] ++ " "
       ++ concat([ code[fix(roster[s, d])] | d in DAYS ]) ++ "\n" | s in STAFF ]
  % TODO(1)(2)(3) を書いたら、次の6行のコメントを外す。
  % ++ [ "希望休違反 = " ++ show(pref)
  %      ++ "   勤務日数の偏り = " ++ show(unfair)
  %      ++ "   夜勤回数の偏り = " ++ show(night_unfair)
  %      ++ "   目的関数 = " ++ show(penalty) ++ "\n" ]
  % ++ [ "#value pref " ++ show(pref) ++ "\n#value unfair " ++ show(unfair) ++ "\n"
  %      ++ "#value night_unfair " ++ show(night_unfair) ++ "\n#value penalty " ++ show(penalty) ++ "\n" ]
  ;
