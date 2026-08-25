% 第02回 標準演習: 論理グリッドを解き切る
%
% 使い方・手掛かりの一覧・完了条件は教材ページを見る。
%   materials/sessions/02-prolog-modeling.md（サイトの「第02回」）
%
% このファイルの中身を、実行ページのプログラム欄に貼り付けて使う。
% 登場する名前・サークル・属性はすべて架空のものである。

:- use_module(library(lists)).

% 並べ替え（permutation）で候補を作ると、
% 「同じ値が2人に当たらない」ことが最初から保証される。
solve(People) :-
    People = [p(aoi,     D1, C1, T1),
              p(hikaru,  D2, C2, T2),
              p(tsubasa, D3, C3, T3),
              p(kaede,   D4, C4, T4)],
    permutation([coffee, tea, cocoa, juice],      [D1, D2, D3, D4]),
    permutation([tennis, brass_band, photo, art], [C1, C2, C3, C4]),
    permutation([train, bicycle, walk, bus],      [T1, T2, T3, T4]),

    % TODO 教材ページ「今回解く問題」の手掛かり1〜9をここに書く。
    %
    %   1 hikaru は電車で通う
    %   2 コーヒーを飲む人はテニス部にいる
    %   3 写真部の人は徒歩で通う
    %   4 aoi は写真部ではない
    %   5 吹奏楽部の人は紅茶を飲む
    %   6 kaede はバスで通う
    %   7 tsubasa はココアを飲まない
    %   8 美術部の人は自転車で通う
    %   9 kaede はテニス部ではない
    %
    % 一度に全部書かない。1つ書くたびに solve(People) を実行して、
    % 解がどれだけ絞られたかを見る。
    % 各行の終わりを , にして、下の true. の前に並べる。

    true.


% ── 書けたら、クエリ欄で試す ────────────────────────
%   solve(People)
%
% 解が1つ出たあと「次の解」を押す。false. になれば解は1通りである。
% 別の解が出たら、手掛かりのどれかが書けていない。
%
% 発展演習 A: 手掛かりを1つずつコメントアウトして、解の数がいくつになるかを数える。
% 発展演習 B: permutation と手掛かりの並べ方を変えて、実行時間の変化を測る。
