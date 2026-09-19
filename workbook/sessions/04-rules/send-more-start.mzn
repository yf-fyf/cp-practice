% 選択M04：SEND + MORE = MONEY
include "alldifferent.mzn";
% TODO(作業1): SとMが0ではない制約を書く。
var 0..9: S;
var 0..9: E;
var 0..9: N;
var 0..9: D;
var 0..9: M;
var 0..9: O;
var 0..9: R;
var 0..9: Y;
% TODO(作業2): 八文字の全相異なりと加算の等式を書く。
var int: send = 1000*S + 100*E + 10*N + D;
var int: more = 1000*M + 100*O + 10*R + E;
var int: money = 10000*M + 1000*O + 100*N + 10*E + Y;
solve satisfy;
output [show(send), " + ", show(more), " = ", show(money), "\n"];
