/* 
 * Searching code for Prolog searching topic, Part 2.
 * This is a full solution for the puzzle we talked about in class,
 * moving a boat across a river (described on slides 8&9 of the slides).
 */
 
/*
 * A query to solve the initial problem (taking the boat, the wolf, 
 * the goat and the cabbage from the north to the south side of the 
 * river
 */
boatPuzzle(Path) :-
    search(n/n/n/n, % initial state
           s/s/s/s, % final state 
           Path).

% General searching algorithm: if A and B are nodes in a 
% graph, search (A,B,Path) means that Path is a path from
% A to B.
search(A, B, Path) :-
    search4(A,B,[],Path). % initially no nodes have been visited yet
  
% search4(Start,Finish,Visited,Path) means that Path is a
% path from Start to Finish that doesn't include any 
% nodes in Visited (except that Start might be a member
% of Visited)
search4(Start,Start,_,[Start]).
search4(A,B,Visited,[A|Path]) :-
    move(A,C),
    not(member(C,Visited)),
    search4(C,B,[A|Visited],Path).
    
% Representing the goat-wolf-cabbage problem as a graph.
% A node in the graph consists of a structure with four elements,
% each of which is n or s, representing the north or south side
% of the river.  

% handy facts to establish that north and south are the opposite sides
% of the river
opposite(n,s).
opposite(s,n).
    
% possible(A,B) it is physically possible to get from state A
% to state B in one move.  It does not prevent states where
% the wolf can eat the goat or the goat can eat the cabbage.

%1. boat takes cabbage across river
possible(Boat/Wolf/Goat/Boat,
         Other/Wolf/Goat/Other) :-
    opposite(Boat,Other).
    
%2. boat takes wolf across
possible(Boat/Boat/Goat/Cabbage,
         Other/Other/Goat/Cabbage) :-
    opposite(Boat,Other).
    
%3. boat takes goat across
possible(Boat/Wolf/Boat/Cabbage,
         Other/Wolf/Other/Cabbage) :-
    opposite(Boat,Other).
    
%4. boat goes alone
possible(Boat/Wolf/Goat/Cabbage,
         Other/Wolf/Goat/Cabbage) :-
    opposite(Boat,Other).
    
% a state is safe if nothing can get eaten
safe(State) :- not(dangerous(State)).

% a state is dangerous is something can get eaten.

% dangerous state #1: the wolf will eat the goat
dangerous(Boat/Wolf/Wolf/_) :-
    opposite(Boat,Wolf).
    
% dangerous state #2: the goat will eat the cabbage
dangerous(Boat/_/Goat/Goat) :-
    opposite(Boat,Goat).
    
% Here, finally, is the rule to produce the legal moves 
% between states for this puzzle.  To be a legal move in
% the graph we're using to map out the possibilities, a 
% move has to be physically possible and the ending state
% must be safe.
move(A,B) :-
    possible(A,B),
    safe(B).
         
  
