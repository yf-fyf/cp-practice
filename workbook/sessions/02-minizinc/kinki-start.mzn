% 第02回・選択M02。地域順: K, O, H, S, N, W, M
int: nc = 3;
% TODO(作業1): 各地域の色をvar 1..ncで宣言する。
% 辺: K-H, K-O, K-N, K-S, K-M, H-O, O-N, O-W, S-M, N-W, N-M, W-M
% TODO(作業2): 辺ごとに二地域の色を異ならせる。
solve satisfy;
output [show([K, O, H, S, N, W, M]) ++ "\n"];
