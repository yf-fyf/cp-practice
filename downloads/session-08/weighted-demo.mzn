% 第08回・手順1　必須条件と希望
include "metrics-core.mzn";
% 手順2　全員の日数と日数差（metrics-core.mznのload・spread）
% 手順3　重みと最小化
int: alpha;
int: beta;
constraint assert(alpha >= 0 /\ beta >= 0 /\ alpha + beta > 0,
    "重みは非負で、少なくとも一方は正にする");
var int: objective = alpha*violations + beta*spread;
solve minimize objective;
output ["J=" ++ show(objective) ++ "\n"];
