% 第05回：人×講座の0/1割当
int: n_people;
int: n_courses;
set of int: PEOPLE = 1..n_people;
set of int: COURSES = 1..n_courses;
array[PEOPLE, COURSES] of 0..1: allowed;
array[COURSES] of int: cap;

% TODO(作業1): 人×講座の0/1決定変数xを宣言する。
% TODO(作業2): 一人一講座・定員・許可の三条件を書く。
solve satisfy;
output [concat([show(x[p,c]) ++ " " | c in COURSES]) ++ "\n" | p in PEOPLE];
