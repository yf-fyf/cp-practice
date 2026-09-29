% 第04回：4×4数独の基本条件。対角線などの追加条件は含まない。
% 手順1　基本条件の再開
include "alldifferent.mzn";

% givenの0は空欄を表す。gridに入る数は1〜4。
array[1..4, 1..4] of 0..4: given;
array[1..4, 1..4] of var 1..4: grid;

int: clue_total;

% 初期値のあるマスだけを固定する。
constraint forall(r in 1..4, c in 1..4 where given[r,c] > 0)(
    grid[r,c] = given[r,c]
);

% 各行と各列で重複させない。
constraint forall(r in 1..4)(alldifferent([grid[r,c] | c in 1..4]));
constraint forall(c in 1..4)(alldifferent([grid[r,c] | r in 1..4]));

% 四つの2×2ブロック。今回は具体的な添字で書く。
constraint alldifferent([grid[1,1], grid[1,2], grid[2,1], grid[2,2]]);
constraint alldifferent([grid[1,3], grid[1,4], grid[2,3], grid[2,4]]);
constraint alldifferent([grid[3,1], grid[3,2], grid[4,1], grid[4,2]]);
constraint alldifferent([grid[3,3], grid[3,4], grid[4,3], grid[4,4]]);

% 手順2　合計条件の追加
constraint sum([grid[1,2], grid[1,3], grid[2,3]]) = clue_total;

% 手順3　入力の交換
solve satisfy;

% 表示部分はそのまま使ってよい。
output [concat([show(grid[r,c]) ++ " " | c in 1..4]) ++ "\n" | r in 1..4];
