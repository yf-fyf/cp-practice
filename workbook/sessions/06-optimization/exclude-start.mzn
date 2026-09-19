% 全最適解の別の求め方：既知の一つだけを除く。
include "cost-core.mzn";
int: best;
array[PEOPLE, COURSES] of 0..1: first;
constraint total = best;
% TODO(作業1): firstと少なくとも一セル違う制約を書く。
solve satisfy;
