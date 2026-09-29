% 第05回発展1：一人一変数の表現。y[p]は人pの講座番号。
int: n_people;
int: n_courses;
set of int: PEOPLE = 1..n_people;
set of int: COURSES = 1..n_courses;
array[PEOPLE, COURSES] of 0..1: allowed;
array[COURSES] of int: cap;

array[PEOPLE] of var COURSES: y;
% TODO(作業1): 各講座の人数を数え、定員以下にする。
% TODO(作業2): 選んだ講座がその人に許可されている条件を書く。
solve satisfy;
output [show(y), "\n"];
