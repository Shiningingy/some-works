listSection([X,_|Tail],[X|NewTail]):-listSection(Tail,NewTail),!.
listSection([],[]).
listSection([Z],[Z]).
listSection([_|Tail],NewTail):-listSection(Tail,NewTail).




fillOrder([],[],[]).

fillOrder([_/Count/Max|Items],Exp,Reg):-
    Count*2 >= Max,
    fillOrder(Items,Exp,Reg).

fillOrder([Item/Count/Max|Items],[Item/Result|Exps],Reg):-
    Count*4 < Max,
    Result is Max - Count,
    fillOrder(Items,Exps,Reg).

fillOrder([Item/Count/Max|Items],Exp,[Item/Result|Regs]):-
    Count*4 >= Max,
    Count*2 < Max,
    Result is Max - Count,
    fillOrder(Items,Exp,Regs).

flatten([],[]).
flatten([Item|Tail],Fl):-
    is_list(Item),
    flatten(Item,FlTail),
    flatten(Tail,FL),
    append(FlTail,FL,Fl).
flatten([Item|Tail],[Item|FlTail]):-
    \+ is_list(Item),
    flatten(Tail,FlTail).




hobby(alf, tennis).
hobby(bert, hunting).
hobby(carl, golf).
hobby(dee, golf).
hobby(ed, fishing).
hobby(ed, tennis).

eats(alf, meat).
eats(alf, fish).
eats(bert, fish).
eats(carl, eggs).
eats(dee, meat).



likes(X,Y):-
    hobby(X,H),
    hobby(Y,H),
    X\=Y.
likes(X,Y):-
    eats(X,El),
    !,
    eats(Y,E2),
    X\=Y,
    El\=E2.

respects(alf,Y):-
    hobby(Y,golf).
respects(bert,Y):-
    eats(Y,eggs),
    not(hobby(Y,hunting)),
    !.
respects(carl,Y):-
    hobby(Y,tennis),
    hobby(Y,fishing).

admires(carl,Y):- not(hobby(Y,golf)).


reveres(ed,Y):- not(hobby(carl,golf)), eats(Y,meat).
reveres(ed,Y):-eats(Y,fish).
