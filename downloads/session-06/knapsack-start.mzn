int: capacity;
array[1..4] of int: weight = [2,3,4,5];
array[1..4] of int: value = [3,4,5,8];
% TODO(作業1): 各品物の選択takeの定義域を決め、宣言する。
var int: weight_used = sum(i in 1..4)(weight[i]*take[i]);
var int: value_total = sum(i in 1..4)(value[i]*take[i]);
% TODO(作業2): 容量制約と価値の最大化を書く。
output ["take = ", show(take), "\nweight = ", show(weight_used),
        ", value = ", show(value_total), "\n"];
