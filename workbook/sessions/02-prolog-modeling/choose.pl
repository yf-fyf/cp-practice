% 第02回 必須演習: 候補を選ぶ規則を書き、手掛かりを条件に直す
%
% 使い方と完了条件は教材ページを見る。
%   materials/sessions/02-prolog-modeling.md（サイトの「第02回」）
%
% このファイルの中身を、実行ページのプログラム欄に貼り付けて使う。
% 登場する名前・サークル・属性はすべて架空のものである。

:- use_module(library(lists)).


% ── 前半: 候補を選ぶ規則 ────────────────────────────
% TODO(1) drink/1
%   coffee, tea, cocoa, juice の4つから1つ選ぶ規則を書く。
%   member/2 を使う。
%
%   確認: drink(X) を実行し、「次の解」で4つ出てから false. になる。



% TODO(2) not_train/1
%   train, bicycle, walk, bus の4つのうち、train ではないものを選ぶ規則を書く。
%   まず候補を選び、次に \= で落とす（生成してからテストする）。
%
%   確認: not_train(T) を実行し、「次の解」で3つ出てから false. になる。



% ── 後半: 手掛かりを条件に直す ──────────────────────
% 練習用の割当て。標準演習（grid.pl）とまったく同じ形
%   p(名前, 飲み物, サークル, 通学手段)
% で書いてある。ここで書く clue_a〜clue_c は、そのまま grid.pl で使える。
%
% ただしこれは9個の手掛かりを満たす表ではない。練習のために適当に埋めた値である
% （たとえば手掛かり4「aoi は写真部ではない」を破っている）。
lineup([p(aoi,     cocoa,  photo,      walk),
        p(hikaru,  coffee, tennis,     train),
        p(tsubasa, tea,    brass_band, bicycle),
        p(kaede,   juice,  art,        bus)]).


% TODO(3) clue_a/1  「hikaru はテニス部にいる」
%   肯定形の手掛かり。member/2 と _ で書ける。



% TODO(4) clue_b/1  「コーヒーを飲む人はテニス部にいる」
%   対応形の手掛かり。2つの属性が同じ行に現れることを言う。



% TODO(5) clue_c/1  「aoi は紅茶を飲まない」
%   否定形の手掛かり。まず変数に取り出し、次に \= で条件を付ける（2つの条件になる）。



% ── 書けたら、クエリ欄で試す ────────────────────────
%   drink(X)
%   not_train(T)
%   lineup(P), clue_a(P), clue_b(P), clue_c(P)      成功する
%
% そのあと clue_c の tea を cocoa に書き換えて、最後のクエリが false. になることも見る。
% 条件が効いていることは、失敗する例でしか確かめられない。
%
% ここで書いた clue_a・clue_b・clue_c は、標準演習の grid.pl でそのまま使える。
% 項の形（引数4つ）が同じだからである。
