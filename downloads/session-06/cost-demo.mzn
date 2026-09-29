% 手順1　基本条件の再開
include "assignment-core.mzn";
array[PEOPLE, COURSES] of int: cost;
% 手順2　合計不満度
var int: total = sum(p in PEOPLE, c in COURSES)(cost[p,c] * x[p,c]);
% 手順3　最小化と終了状態
solve minimize total;
output [concat([show(x[p,c]) ++ " " | c in COURSES]) ++ "\n" | p in PEOPLE];
output ["total = ", show(total), "\n"];
