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

% 必修1　修理の規則
% TODO(作業1): can_help(P, D) の規則をここへ書く。
% 未記入の間、can_help の問い合わせは未定義のエラーになる。

/** <examples>
?- can_work(P, D).
?- can_help(P, D).
?- can_help(ben, D).
*/
