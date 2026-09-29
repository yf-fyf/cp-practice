% 第02回・必修2。解説例の完成モデルに、主対角線の条件を加える。
include "alldifferent.mzn";

% 手順2　入力と決定変数。givenの0は空欄、gridは1〜4。
array[1..4, 1..4] of 0..4: given;
array[1..4, 1..4] of var 1..4: grid;

% 手順3　初期値を保持する。
constraint forall(r in 1..4, c in 1..4 where given[r,c] > 0)(
    grid[r,c] = given[r,c]
);

% 手順4　行・列・ブロックで重複させない。
constraint forall(r in 1..4)(alldifferent([grid[r,c] | c in 1..4]));
constraint forall(c in 1..4)(alldifferent([grid[r,c] | r in 1..4]));

% 四つの2×2ブロック。今回は具体的な添字で書く。
constraint alldifferent([grid[1,1], grid[1,2], grid[2,1], grid[2,2]]);
constraint alldifferent([grid[1,3], grid[1,4], grid[2,3], grid[2,4]]);
constraint alldifferent([grid[3,1], grid[3,2], grid[4,1], grid[4,2]]);
constraint alldifferent([grid[3,3], grid[3,4], grid[4,3], grid[4,4]]);

% TODO(作業1): 左上から右下の四つのマスを添字で選ぶ。
% TODO(作業2): 選んだマスの重複を禁止する。

solve satisfy;

% 表示部分はそのまま使ってよい。
output [concat([show(grid[r,c]) ++ " " | c in 1..4]) ++ "\n" | r in 1..4];
