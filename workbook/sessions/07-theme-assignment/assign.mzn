% 第07回 研究テーマの割当 — 穴埋め前
%
% 教材ページ: 講義（全15回）> 第07回 学生と研究テーマの割当
% 実行環境:   MiniZinc Playground（ブラウザ）
%
% データは small.dzn（6人・3テーマ）と medium.dzn（12人・4テーマ）にある。
% モデルはどちらでも動く。TODO を埋めて、実行するデータを切り替える。

% ── データから受け取るもの（値は .dzn 側にある） ──────────────
int: ns;                                 % 割り当てる人数
int: nt;                                 % テーマの数
int: cap;                                % 1つのテーマに入れる人数の上限（定員）

set of int: STUDENTS = 1..ns;
set of int: THEMES   = 1..nt;
set of int: RANKS    = 1..nt;            % 希望順位は 1..nt

array[STUDENTS, THEMES] of RANKS: rank;  % rank[s, t] = s が t を第何希望にしたか
array[RANKS] of int: point;              % point[k] = 第k希望に割り当てたときの得点
array[THEMES] of string: tname;          % テーマの名前（表示用）

% ── 得点表（すでに書いてある。読むだけでよい） ─────────────────
% score[s, t] = 「s を t に割り当てたときの得点」。
% rank[s, t]（s が t を第何希望にしたか）を point で引いただけのものである。
% 順位のままでは足せないので、先に得点に直しておく。
array[STUDENTS, THEMES] of int: score =
  array2d(STUDENTS, THEMES, [ point[rank[s, t]] | s in STUDENTS, t in THEMES ]);

% ── 決定変数 ──────────────────────────────────────────────
% 1人につきテーマを1つ。「1人が2つのテーマに入る」ことは
% この書き方そのものが防いでいる（値を1つしか取れないため）。
array[STUDENTS] of var THEMES: assign;

% ── 制約 ──────────────────────────────────────────────────
% TODO(1) 必須演習: 定員制約を書く。
%   どのテーマについても、割り当てる人数は cap 人以下である。
%   count(assign, t) が「assign の中に t がいくつあるか」である。
% constraint forall(t in THEMES)( ... );

% ── 標準演習: ここから下を足す ───────────────────────────────
% TODO(2) 合計満足度 total を定義し、下の solve を maximize に変える。
%   全員について「割り当てられたテーマの得点」を足す。
%   s に割り当てられたテーマは assign[s] なので、その人の得点は score[s, assign[s]]。
% var int: total = ...;

solve satisfy;

% ── 出力 ──────────────────────────────────────────────────
% 割当てと、テーマごとの人数と、希望順位ごとの人数を出す。
output
  [ show(s) ++ "番 -> " ++ tname[fix(assign[s])]
    ++ "（第" ++ show(rank[s, fix(assign[s])]) ++ "希望）\n"
  | s in STUDENTS ]
  ++ [ "人数  " ]
  ++ [ tname[t] ++ ": " ++ show(count(assign, t)) ++ "人  " | t in THEMES ]
  ++ [ "\n順位  " ]
  ++ [ "第" ++ show(k) ++ "希望: "
       ++ show(count([ rank[s, fix(assign[s])] | s in STUDENTS ], k)) ++ "人  "
     | k in RANKS ]
  ++ [ "\n" ];
