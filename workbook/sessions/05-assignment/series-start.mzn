% 選択M05：s[i]は数iの出現回数。添字は0始まり。
int: n;
array[0..n-1] of var 0..n: s;
% TODO(作業1): 一つの数iの出現回数をsumとbool2intで表す。
% TODO(作業2): 各iについてs[i]と出現回数を等しくする。
solve satisfy;
output [show(s), "\n"];
