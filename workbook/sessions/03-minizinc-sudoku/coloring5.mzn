% 第03回 小さな実行例 — グラフ彩色（架空の5地区）の MiniZinc 版
%
% 第02回で Prolog の「候補を作って条件で落とす」書き方で解いた問題を、
% 制約だけを書いて解く。穴埋めは無い。そのまま実行して結果を見る。
%
% 地区と隣接関係は第02回の coloring.pl とまったく同じである。
%   中央区は北区・南区・東区・西区のすべてと隣り合う
%   外側は 北 - 東 - 南 - 西 - 北 の順に隣り合う
%
% 教材ページ: 講義（全15回）> 第03回 数独: MiniZincで盤面を解く

int: nd = 5;                       % 地区の数
int: nc = 3;                       % 使える色の数
set of int: DISTRICTS = 1..nd;
set of int: COLORS    = 1..nc;

% 地区の名前と色の名前（出力を読みやすくするためだけのもの）
% color は nc を 3 から減らしても使えるよう、3 つ分を固定で持たせてある。
array[DISTRICTS] of string: name  = ["北区", "南区", "東区", "西区", "中央区"];
array[1..3]      of string: color = ["色1", "色2", "色3"];

% 隣接している地区の組。ここが入力データである。
% 第02回の coloring.pl に並んでいる 8 本の \= と1対1に対応する。
int: ne = 8;
array[1..ne, 1..2] of int: edge =
  [| 1, 5      % 北区 - 中央区
   | 2, 5      % 南区 - 中央区
   | 3, 5      % 東区 - 中央区
   | 4, 5      % 西区 - 中央区
   | 1, 3      % 北区 - 東区
   | 3, 2      % 東区 - 南区
   | 2, 4      % 南区 - 西区
   | 4, 1 |];  % 西区 - 北区

% 決定変数: 各地区に塗る色
array[DISTRICTS] of var COLORS: paint;

% 制約: 隣り合う地区は違う色
constraint forall(e in 1..ne)( paint[edge[e, 1]] != paint[edge[e, 2]] );

solve satisfy;

output [ name[d] ++ ": " ++ color[fix(paint[d])] ++ "\n" | d in DISTRICTS ];
