include "assignment-core.mzn";
array[PEOPLE, COURSES] of int: cost;
% TODO(作業1): 選んだ位置だけを足し、totalを定義する。
% TODO(作業2): totalを最小化するsolveを書く。
output [concat([show(x[p,c]) ++ " " | c in COURSES]) ++ "\n" | p in PEOPLE];
output ["total = ", show(total), "\n"];
