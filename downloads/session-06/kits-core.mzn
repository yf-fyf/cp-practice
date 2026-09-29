int: material_capacity;
int: time_capacity;
int: score_u;
int: score_v;
var 0..(material_capacity div 2): u;
var 0..(time_capacity div 2): v;
constraint 2*u + v <= material_capacity;
constraint u + 2*v <= time_capacity;
var int: material_used = 2*u + v;
var int: time_used = u + 2*v;
var int: score = score_u*u + score_v*v;
output ["u = ", show(u), ", v = ", show(v), "\n",
        "material = ", show(material_used), ", time = ", show(time_used), "\n",
        "score = ", show(score), "\n"];
