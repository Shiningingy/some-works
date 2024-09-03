%Allen Luo
%20001744
match(Month,Day,Word):-
    weather(Month,Day,Word,_,_);
    weather(Month,Day,_,Word,_);
    weather(Month,Day,_,_,Word).

wet(Month,Day):-
    match(Month,Day,rain);
    match(Month,Day,snow).

desert(Month,Day):-
    match(Month,Day,hot),
    match(Month,Day,dry).

tropical(Month,Day):-
    match(Month,Day,hot),
    match(Month,Day,rain).

hotOrWarm(Month,Day):-
    match(Month,Day,hot);
    match(Month,Day,warm).


impossible(Month,Day):-
    hotOrWarm(Month,Day),
    match(Month,Day,snow).

summer(Month):-
    Month = jun;
    Month = jul;
    Month = aug.

winter(Month):-
    Month = jan;
    Month = feb;
    Month = mar.

unseasonWinter(Month,Day):-
    hotOrWarm(Month,Day),
    winter(Month).

coolOrCold(Month,Day):-
    match(Month,Day,cool);
    match(Month,Day,cold).

unseasonSummer(Month,Day):-
    coolOrCold(Month,Day),
    summer(Month).

unseasonable(Month,Day):-
    unseasonWinter(Month,Day);
    unseasonSummer(Month,Day).

mixed(Month):-
    match(Month,_,hot),
    match(Month,_,cold).







