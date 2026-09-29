% 手順1　予定と技能の事実
% 架空の識別子。available(人, 曜日)、trained(人, 技能)。
available(aki, tue).
available(aki, wed).
available(ben, tue).
available(chi, wed).

trained(aki, register).
trained(aki, repair).
trained(ben, register).
trained(chi, repair).

% 手順2　受付の規則
can_work(P, D) :- available(P, D), trained(P, register).

% 必修1　修理の規則（必修2以降では出発点として提供）
can_help(P, D) :- available(P, D), trained(P, repair).

% 必修2　同じ日の役割候補
pair(P, Q, D) :- can_work(P, D), can_help(Q, D).

% 発展1　別人での役割分担
% TODO(作業1): pair と dif を使い distinct_pair(P, Q, D) を書く。

/** <examples>
?- pair(P, Q, D).
?- distinct_pair(P, Q, D).
?- distinct_pair(aki, aki, tue).
*/
