% 有向辺。edge(出発地, 到着地)。逆向きの辺は含めない。
edge(a, b).
edge(a, c).
edge(b, d).
edge(c, d).

% 発展2　一辺以上の到達
% TODO(作業1): reach(X, Y) の直接の場合と途中を経由する場合を書く。

/** <examples>
?- edge(a, X).
?- reach(a, Y).
?- reach(d, Y).
*/
