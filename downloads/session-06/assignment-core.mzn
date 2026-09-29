% 第05回：人×講座の0/1割当
int: n_people;
int: n_courses;
set of int: PEOPLE = 1..n_people;
set of int: COURSES = 1..n_courses;
array[PEOPLE, COURSES] of 0..1: allowed;
array[COURSES] of int: cap;

% 手順1　選択の変数
array[PEOPLE, COURSES] of var 0..1: x;

% 手順2　一人一講座
constraint forall(p in PEOPLE)(sum(c in COURSES)(x[p,c]) = 1);
% 手順3　定員と許可
constraint forall(c in COURSES)(sum(p in PEOPLE)(x[p,c]) <= cap[c]);
constraint forall(p in PEOPLE, c in COURSES)(x[p,c] <= allowed[p,c]);
