% 第02回・必修1。gridが未宣言なので、このままでは実行できない。
include "alldifferent.mzn";
array[1..4, 1..4] of 0..4: given;

% TODO(作業1): 決定変数gridを宣言し、初期値を保持する。
% TODO(作業2): 各行・各列・四つのブロックの重複を禁止する。

solve satisfy;
output [concat([show(grid[r,c]) ++ " " | c in 1..4]) ++ "\n" | r in 1..4];
