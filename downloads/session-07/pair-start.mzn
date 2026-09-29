% 第07回・発展1。技能なしの基本条件に、AとBの同日勤務の禁止を追加する。
int: n_people;
int: n_days;
set of int: PEOPLE = 1..n_people;
set of int: DAYS = 1..n_days;
array[PEOPLE] of string: person_name;
array[DAYS] of string: day_name;
array[DAYS] of int: required;
array[PEOPLE, DAYS] of 0..1: available;
array[PEOPLE] of int: max_days;

% 式(1)：人と日ごとの勤務有無
array[PEOPLE, DAYS] of var 0..1: work;

% 式(2)：各日の人数
constraint forall(d in DAYS)(
    sum(p in PEOPLE)(work[p,d]) = required[d]
);

% 式(3)：勤務可能性
constraint forall(p in PEOPLE, d in DAYS)(
    work[p,d] <= available[p,d]
);

% 式(4)：各人の勤務日数の上限
constraint forall(p in PEOPLE)(
    sum(d in DAYS)(work[p,d]) <= max_days[p]
);

% TODO(作業1) AとBが同日に勤務しない条件を追加する
% TODO(作業2) 二人とも休む日を許すか確かめる
solve satisfy;

% 表示用。解として許す条件は変えない。
output ["人 " ++ concat([day_name[d] ++ " " | d in DAYS]) ++ "\n"]
    ++ [person_name[p] ++ "  "
        ++ concat([show(work[p,d]) ++ "  " | d in DAYS]) ++ "\n"
        | p in PEOPLE];
