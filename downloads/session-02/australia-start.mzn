% 第02回・選択M02。地域順: WA, NT, SA, Q, NSW, V, T
int: nc = 3;
% TODO(作業1): 各地域の色をvar 1..ncで宣言する。
% 辺: WA-NT, WA-SA, NT-SA, NT-Q, SA-Q, SA-NSW, SA-V, Q-NSW, NSW-V
% TODO(作業2): 辺ごとに二地域の色を異ならせる。
solve satisfy;
output [show([WA, NT, SA, Q, NSW, V, T]) ++ "\n"];
