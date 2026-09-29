int: flour;
int: banana;
int: sugar;
int: butter;
int: cocoa;
% TODO(作業1): b・cの安全な整数範囲を導き、宣言する。
var int: revenue = 400*b + 450*c;
% TODO(作業2): 五資源の容量制約と売上の最大化を書く。
output ["b = ", show(b), ", c = ", show(c), "\n",
        "flour = ", show(250*b+200*c), ", banana = ", show(2*b), "\n",
        "sugar = ", show(75*b+150*c), ", butter = ", show(100*b+150*c), "\n",
        "cocoa = ", show(75*c), ", revenue = ", show(revenue), "\n"];
