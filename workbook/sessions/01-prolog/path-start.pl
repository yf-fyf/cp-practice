% 有向辺。edge(出発地, 到着地)。逆向きの辺は含めない。
edge(a, b).
edge(a, c).
edge(b, d).
edge(c, d).
edge(d, a).

% 発展3　再訪しない経路
% TODO(作業1): path(Start, Goal, Path) と必要な補助関係を書く。
% Start と Goal は問い合わせで具体的な場所を指定する。

/** <examples>
?- edge(a, X).
?- path(a, d, Path).
?- path(a, a, Path).
*/
