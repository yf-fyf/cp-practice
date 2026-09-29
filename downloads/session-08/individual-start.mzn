% 発展2　個人の最大違反と合計
include "metrics-core.mzn";
% TODO(作業1): 個人の違反personalと、その最大worstを定義する。
% TODO(作業2): 合計violationsと最大worstの最小化を別々に試す。
output ["personal=" ++ show(personal) ++ " M=" ++ show(worst) ++ "\n"];
