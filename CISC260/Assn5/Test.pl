elem(X,[X|_]).
elem(X,[_|XS]):- elem(X,XS).

conc(L1,L2,L3):- append(L1,L2,L3).


same_length(L1,L2) :-
    length(L1,X),
    length(L2,Y),
    X=Y.

middle(L, M) :-
    append(L1, [M|L2], L),
    same_length(L1, L2).

middle(L, [M,N]) :-
    append(L1, [M,N|L2], L),
    same_length(L1, L2).
