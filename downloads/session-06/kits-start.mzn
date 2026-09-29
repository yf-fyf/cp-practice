int: material_capacity;
int: time_capacity;
int: score_u;
int: score_v;
% TODO(作業1): u・vの意味と安全な整数範囲を決め、二つの容量制約を書く。
% TODO(作業2): 得点scoreを定義し、最大化するsolveを書く。
var int: material_used = 2*u + v;
var int: time_used = u + 2*v;
output ["u = ", show(u), ", v = ", show(v), "\n",
        "material = ", show(material_used), ", time = ", show(time_used), "\n",
        "score = ", show(score), "\n"];
