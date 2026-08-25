% 第01回 標準演習: 事実から新しい関係を導く規則を書く
%
% 使い方と完了条件は教材ページを見る。
%   materials/sessions/01-prolog-intro.md（サイトの「第01回」）
%
% このファイルの中身を、実行ページのプログラム欄に貼り付けて使う。
% 必須演習で完成させたものと同じ知識ベースが最初から入っている。
%
% 登場する名前・サークル・属性はすべて架空のものである。

% ── 知識ベース ──────────────────────────────────────
% 好きな飲み物
drinks(aoi, cocoa).
drinks(hikaru, coffee).
drinks(tsubasa, tea).
drinks(kaede, cocoa).

% 所属サークル
club(aoi, photo).
club(hikaru, tennis).
club(tsubasa, brass_band).
club(kaede, photo).

% 通学手段
commute(aoi, bicycle).
commute(hikaru, train).
commute(tsubasa, walk).
commute(kaede, train).

% 規則の例: X と Y が同じサークル C に所属していれば、2人は teammate である
teammate(X, Y) :- club(X, C), club(Y, C).


% ── ここから書く ────────────────────────────────────
% TODO(A) ride_together/2
%   同じ通学手段で通う2人を表す規則を書く。
%   teammate/2 と同じ形になる。使う述語が違うだけである。



% TODO(B) train_tennis/1
%   電車で通っていて、かつテニス部にいる人を表す規則を書く。
%   条件が2つあり、使う述語はそれぞれ別である。条件は , でつなぐ。



% ── 書けたら、クエリ欄で試す ────────────────────────
%   teammate(aoi, Y)        規則の例の動きを見る
%   ride_together(X, Y)     「次の解」で false. になるまで押す
%   train_tennis(X)         X = hikaru. が出る
%
% 考察: ride_together(aoi, aoi) のような「同じ人どうしの組」が出てくる。
%       なぜ出るのか。書いた規則のどこがそうさせているのか。
%       （除く書き方は第02回で導入する。ここでは理由が言えればよい）
