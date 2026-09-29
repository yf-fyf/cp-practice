% 必修2：基本の一人一講座・定員・許可は完成済み。
include "assignment-base.mzn";
array[COURSES] of var 0..1: opened;
% TODO(作業1): 開催時は2人以上にする。
% TODO(作業2): 非開催時は0人にし、開催時の上限も守る。
output ["opened = ", show(opened), "\n"];
