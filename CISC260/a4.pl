% CISC 360 a4, Fall 2020
%
% See a4.pdf for instructions

/*
 * Q1: Student ID
 */
student_id(  ).

/*
 * Q2: Prime numbers
 */
% hasFactor
hasFactor(N, F) :- N mod F =:= 0.
hasFactor(N, F) :- N mod F =\= 0,
                   F * F < N,
                   Fplus1 is F + 1,
                   hasFactor(N, Fplus1).

% isPrime(N, What)
%   What = prime      iff  N is prime
%   What = composite  iff  N is composite

isPrime(1, prime).
isPrime(2, prime).
isPrime(N, composite) :- N > 2,    hasFactor(N, 2).
isPrime(N, prime)     :- N > 2, \+ hasFactor(N, 2).
%                               ^^
%                               "not"


% findPrimes(Numbers, Primes)
%   Primes = all prime numbers in Numbers
%
% Q2a. Replace the word "change_this" in the rules below.
%      HINT: Try to use  findPrimes(Xs, Ys)
findPrimes([], []).

findPrimes([X | Xs], Ys) :-
    change_this.

findPrimes([X | Xs], [X | Ys]) :-
    change_this.

% upto(X, Y, Zs):
%   Zs is every integer from X to Y
%   Example:
%     ?- upto(3, 7, Range)
%     Range = [3, 4, 5, 6, 7]

upto(X, X, [X]).
upto(X, Y, [X | Zs]) :-
    X < Y,
    Xplus1 is X + 1,
    upto(Xplus1, Y, Zs).

% primes_range(M, N, Primes)
%   Primes = all prime numbers between M and N
%   Example:
%     ?- primes_range(60, 80, Primes).
%     Primes = [61, 67, 71, 73, 79] .

% Q2b. Replace the word "change_this" in the rule below.
%      HINT: Use upto and findPrimes.

primes_range(M, N, Primes) :-
   change_this.


/*
 * Q3. Translate the tower function from a1.
 *

  tower :: Integer -> Integer -> Integer
  tower k n =
    if k > n then 1
    else (div (n + k + 1) k) * tower (k + 1) n

I rewrote this definition to look more like the
Prolog code you need to write:

  tower :: Integer -> Integer -> Integer
  tower k n
      | k > n     = 1
      | otherwise = r
                    where
                      kplus1 = k + 1
                      towerresult = tower kplus1 n
                      r = (div (n + k + 1) k) * towerresult

Alternatively, using 'let':

  tower :: Integer -> Integer -> Integer
  tower k n
      | k > n     = 1
      | otherwise = let kplus1 = k + 1
                        towerresult = tower kplus1 n
                        r = (div (n + k + 1) k) * towerresult
                    in
                        r

In Haskell, div (n + k) k
            returns the "floor" of (n + k) divided by k.

In Prolog, this operation is also named "div":
   ?- X is 11 div 2.
   X = 5.

tower(K, N, R) true iff R = (tower K N)
*/
tower(K, N, 1) :-
    change_this.
tower(K, N, R) :-
    change_this.

/*
  To test: ?- tower(6, 5, 1).
           true .
           ?- tower(5, 5, 2).
           true .
           ?- tower(3, 16, R).
           R = 829440 .          % type .
           ?- tower(3, 16, R).
           R = 829440            % type ;
           false.

  Hint: If you get more than one solution when you type ;,
        look at how we defined hasFactor.
*/


/*
  Q4: Tree paths

  Consider the tree     (We are *not* representing
                          trees with Empty "leaves":
             4                         4
            / \                      /   \
           2   5                   2       5
          / \                    /  \     / \
         1   3                 1     3   E   E
                              / \   / \
                          Empty  E E   E            )

  What we are doing here is similar to the Haskell type
  
    data A4Tree = Node Integer A4Tree A4Tree
                | Leaf Integer

  In the tree above (leaves 1, 3, 5),
  the paths starting from the root are:

    4 to 2 to 1          [4, 2, 1]
    4 to 2 to 3          [4, 2, 3]
    4 to 5               [4, 5]

  The above tree can be represented in Prolog as

    node(4, node(2, leaf(1), leaf(3)), leaf(5))

  In this question, define a Prolog predicate

    findpath(Tree, Path)

  such that if we start from the root of Tree,
  then Path is a list of numbers from the root to a leaf.

  For example:
  
    ?- findpath(node(2, leaf(1), leaf(3)), [2, 1]).
    true
    ?- findpath(node(2, leaf(1), leaf(3)), [2, 3]).
    true

  Your predicate should be written so that when the first argument is a specific tree
  (containing no variables) and the second argument is a variable, typing ; returns
  *all* possible paths to all the leaves, from left to right.  For example:

    ?- findpath(node(4, node(2, leaf(1), leaf(3)), leaf(5)), Path).
    Path = [4, 2, 1]
    Path = [4, 2, 3]
    Path = [4, 5].

  Hint:
    ?- findpath(leaf(2), [2]).
  should be true.

  Add clauses defining 'findpath' below.
*/

