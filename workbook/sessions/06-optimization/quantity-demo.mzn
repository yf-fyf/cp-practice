% 手順4　個数と最大化
var 0..4: q;
constraint 2*q <= 8;
solve maximize q;
output ["q = ", show(q), "\n"];
