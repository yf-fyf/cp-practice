% 手順1　二つの未知の整数を条件で決める。
var 1..4: x;
var 1..4: y;
constraint x < y;
constraint x + y = 5;
solve satisfy;
output ["x = " ++ show(x) ++ ", y = " ++ show(y) ++ "\n"];
