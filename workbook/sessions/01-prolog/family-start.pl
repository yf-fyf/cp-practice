% 架空の家系図。この問題で使う属性と親子関係の全事実。
male(ren).
male(kai).
male(nao).
female(emi).
female(mio).
female(yui).

% parent(親, 子)。
parent(ren, kai).
parent(emi, kai).
parent(ren, mio).
parent(emi, mio).
parent(kai, nao).
parent(yui, nao).

% 選択P01　家系図
% TODO(作業1): father(P, C) と mother(P, C) を書く。
% TODO(作業2): grandparent(G, C) を書く。

/** <examples>
?- parent(P, mio).
?- father(P, mio).
?- mother(P, nao).
?- grandparent(G, nao).
?- grandparent(ren, C).
?- grandparent(kai, nao).
*/
