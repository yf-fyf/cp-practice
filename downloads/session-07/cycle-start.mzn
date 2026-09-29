% 発展3：入力も条件も新しい周期勤務。前の演習の条件は含めない。
int: group_size;
int: n_days;
int: min_work;
int: max_work;
set of int: PEOPLE = 1..2*group_size;
set of int: DAYS = 1..n_days;
array[PEOPLE, DAYS] of var 0..1: work;
% TODO(作業1) 各日各群から一人、各人の日数の下限・上限
% TODO(作業2) 連続日（最終日と初日も含む）の禁止、同じ組の再登場の禁止
solve satisfy;
% 条件を記入した後、各日の二人をJSON形式で表示する。
output ["[" ++ concat([
    (if d>1 then "," else "" endif) ++ "[" ++
    show(sum(p in 1..group_size)(p*work[p,d])) ++ "," ++
    show(sum(p in group_size+1..2*group_size)(p*work[p,d])) ++ "]"
    | d in DAYS]) ++ "]\n"];
