include "metrics-core.mzn";
array[PEOPLE] of var 0..n_days: personal;
constraint forall(p in PEOPLE)(
    personal[p] = sum(d in DAYS)(request[p,d]*work[p,d])
);
var int: worst = max(personal);
output ["personal=" ++ show(personal) ++ " M=" ++ show(worst) ++ "\n"];
