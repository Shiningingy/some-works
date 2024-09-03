%ZILI LUO
%#20001744

order(P1,P2,[P1+P2]):- P1@<P2.
order(P1,P2,[P2+P1]):- P2@<P1.

search([P1/T1,P2/T2],_,Maxtime,Moves,T):-
    order(P1,P2,Moves),
    T is max(T1,T2),
    T =< Maxtime.

search(Left,Right,Maxtime,[P1+P2,P3|Moves],Time):-
    select(P1/T1,Left,PLeft1),
    select(P2/T2,PLeft1,PLeft2),
    P1@<P2,
    LT is max(T1,T2),%cross
    select(P3/RT,[P1/T1,P2/T2|Right],PRight),%moveback
    search([P3/RT|PLeft2],PRight,Maxtime,Moves,Time1),
    Time is LT + RT + Time1,
    Time =< Maxtime.

moveFamliy(Name,Maxtime,Moves,Time):-
    family(Name,Members),
    search(Members,[],Maxtime,Moves,Time).
