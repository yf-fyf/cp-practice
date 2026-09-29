include "assignment-core.mzn";
array[PEOPLE, COURSES] of int: cost;
var int: total = sum(p in PEOPLE, c in COURSES)(cost[p,c] * x[p,c]);
output [concat([show(x[p,c]) ++ " " | c in COURSES]) ++ "\n" | p in PEOPLE];
output ["total = ", show(total), "\n"];
