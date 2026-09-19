% 第08回・必修1　希望の変更
include "roster-core.mzn";
array[PEOPLE, DAYS] of 0..1: request;
int: alpha;
int: beta;
constraint assert(alpha >= 0 /\ beta >= 0 /\ alpha + beta > 0,
    "重みは非負で、少なくとも一方は正にする");
array[PEOPLE] of var 0..n_days: load;
constraint forall(p in PEOPLE)(load[p] = sum(d in DAYS)(work[p,d]));
% TODO(作業1): 希望違反violationsと、全員の日数差spreadを定義する。
% TODO(作業2): 重み付きのobjectiveを定義し、最小化する。
output ["人 " ++ concat([day_name[d] ++ " " | d in DAYS]) ++ "\n"]
    ++ [person_name[p] ++ "  "
        ++ concat([show(work[p,d]) ++ "  " | d in DAYS]) ++ "\n"
        | p in PEOPLE];
output ["load=" ++ show(load)
    ++ "\nV=" ++ show(violations) ++ " F=" ++ show(spread)
    ++ " J=" ++ show(objective) ++ "\n"];
