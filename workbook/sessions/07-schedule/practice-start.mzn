% 必修1の出発ファイル。入力の宣言と表示は完成している。
% 作業1〜4を書き足すまで、このファイルは実行できない。
int: n_people;
int: n_days;
set of int: PEOPLE = 1..n_people;
set of int: DAYS = 1..n_days;
array[PEOPLE] of string: person_name;
array[DAYS] of string: day_name;
array[DAYS] of int: required;
array[PEOPLE, DAYS] of 0..1: available;
array[PEOPLE] of int: max_days;

% TODO(作業1) 人と日ごとの勤務有無を表す決定変数 work を宣言する

% TODO(作業2) 各日の勤務人数を required[d] に一致させる

% TODO(作業3) 勤務できない位置を選ばないようにする

% TODO(作業4) 各人の勤務日数を max_days[p] 以下にする

solve satisfy;

% 表示用。解として許す条件は変えない。
output ["人 " ++ concat([day_name[d] ++ " " | d in DAYS]) ++ "\n"]
    ++ [person_name[p] ++ "  "
        ++ concat([show(work[p,d]) ++ "  " | d in DAYS]) ++ "\n"
        | p in PEOPLE];
