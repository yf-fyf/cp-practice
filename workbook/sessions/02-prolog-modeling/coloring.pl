% 第02回 小さな実行例と発展演習 C: グラフ彩色
%
% 架空の市の5地区を3色で塗り分ける。隣り合う地区は違う色にする。
% 論理グリッドと同じ「生成とテスト」の形で書いてある。
%
% 教材ページ: materials/sessions/02-prolog-modeling.md（サイトの「第02回」）
% このファイルの中身を、実行ページのプログラム欄に貼り付けて使う。

color(red).
color(green).
color(blue).

% 地区のつながり
%   中央区は北区・南区・東区・西区のすべてと隣り合う
%   外側は 北 - 東 - 南 - 西 - 北 の順に隣り合う
paint(Kita, Minami, Higashi, Nishi, Chuo) :-
    color(Kita), color(Minami), color(Higashi), color(Nishi), color(Chuo),
    Kita    \= Chuo,
    Minami  \= Chuo,
    Higashi \= Chuo,
    Nishi   \= Chuo,
    Kita    \= Higashi,
    Higashi \= Minami,
    Minami  \= Nishi,
    Nishi   \= Kita.


% ── そのまま試す ────────────────────────────────────
%   paint(Kita, Minami, Higashi, Nishi, Chuo)
%
% 「次の解」で別の塗り分けが出る。false. になるまで押して解の数を数える。
% color(blue). をコメントアウトして2色にすると何が起きるかも見る。
%
% ── 発展演習 C ──────────────────────────────────────
% 地区を7つに増やす。隣接関係は教材ページの表にある。
% 3色で塗り分けられるか。解はいくつあるか。2色ではどうか。
% 5地区のときと比べて実行時間はどう変わったか。
