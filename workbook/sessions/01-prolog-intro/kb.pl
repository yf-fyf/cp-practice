% 第01回 必須演習: 名簿を知識ベースにする
%
% 使い方と完了条件は教材ページを見る。
%   materials/sessions/01-prolog-intro.md（サイトの「第01回」）
%
% このファイルの中身を、実行ページのプログラム欄に貼り付けて使う。
% 実行ページ: tools/prolog/
%
% 登場する名前・サークル・属性はすべて架空のものである。

% ── 与えられているもの ──────────────────────────────
% 好きな飲み物
drinks(aoi, cocoa).
drinks(hikaru, coffee).
drinks(tsubasa, tea).
drinks(kaede, cocoa).


% ── ここから書く ────────────────────────────────────
% TODO(1) 所属サークルの事実を4人分書く。述語の名前は club とする。
%
%   aoi     -> photo
%   hikaru  -> tennis
%   tsubasa -> brass_band
%   kaede   -> photo
%
% 1行の形は drinks と同じ。行の終わりのピリオドを忘れない。



% TODO(2) 通学手段の事実を4人分書く。述語の名前は commute とする。
%
%   aoi     -> bicycle
%   hikaru  -> train
%   tsubasa -> walk
%   kaede   -> train



% ── 書けたら、クエリ欄で順に試す ────────────────────
%   club(X, tennis)                     テニス部にいるのは誰か
%   drinks(X, cocoa), commute(X, M)     ココアを飲む人の通学手段（解は2つ）
%   commute(X, train), club(X, C)       電車で通う人のサークル（解は2つ）
%
% 「次の解」を押して false. になるまで確かめる。
