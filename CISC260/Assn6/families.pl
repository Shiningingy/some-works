% Some example families for testing Assignment 6
% CISC 260, Winter 2015

% The family in the original puzzle from the web
family(original, [father/1, mother/2, child/5, granny/10]).

% A less traditional (and larger) family
family(fastkids, [father/6, mother/4, teen/3, kid/2, baby/1]).

% Another four-person family
family(four, [a/1,b/3,c/4,d/7]).

% Some smaller families for testing
family(two, [fred/1, george/2]).
family(three, [harry/1, ron/2, hermoine/3]).

% A Predicate to force Prolog to print long lists in full.
% If Prolog is printing ellipsis (...) instead of complete lists,
% type "fixOutput." to the prompt and this will fix the problem
% for the rest of your Prolog session.
fixOutput :- set_prolog_flag(toplevel_print_options,
    [quoted(true), portray(true), max_depth(0), spacing(next_argument)]). 
    



