% 完成した複数ヒントモデルを再配布。発展1の完成は不要。
include "multi-base.mzn";
array[1..4, 1..4] of 1..4: first;
% TODO(作業1): firstと少なくとも一マス異なる制約を書く。
% solveとoutputはmulti-base.mznにあるので、ここには追加しない。
