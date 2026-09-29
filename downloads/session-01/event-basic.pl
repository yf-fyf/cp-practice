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

% 手順3　問い合わせ（下のコメント内は実行されない）

/** <examples>
?- available(aki, tue).
?- can_work(P, tue).
?- can_work(aki, D).
?- can_work(P, D).
?- available(P, D), available(Q, D).
*/
