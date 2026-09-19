include "roster-core.mzn";
array[PEOPLE, DAYS] of 0..1: request;
array[PEOPLE] of var 0..n_days: load;
constraint forall(p in PEOPLE)(load[p] = sum(d in DAYS)(work[p,d]));
var int: violations = sum(p in PEOPLE, d in DAYS)(
    request[p,d]*work[p,d]
);
var int: spread = max(load) - min(load);
output ["人 " ++ concat([day_name[d] ++ " " | d in DAYS]) ++ "\n"]
    ++ [person_name[p] ++ "  "
        ++ concat([show(work[p,d]) ++ "  " | d in DAYS]) ++ "\n"
        | p in PEOPLE];
output ["load=" ++ show(load)
    ++ "\nV=" ++ show(violations) ++ " F=" ++ show(spread) ++ "\n"];
