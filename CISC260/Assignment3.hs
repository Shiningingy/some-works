-- |ZILI LUO, Student# 20001744
{-
 - Starting code for Assignment 3.
 - You should add the required functions plus your own
 - helper functions to this file and submit it to OnQ.
 - CISC 260, Winter 2018
 -}
module Assignment3 where

-- Definition of the Trie type.  A trie consists of a starting
-- letter (the special character '.' in a complete trie plus 
-- list of sub-tries.  
data Trie = MakeTrie Char [Trie] 
    deriving Eq

-- As a starting point, emptyTrie is a trie containing
-- nothing but the empty string
emptyTrie = MakeTrie '.' [MakeTrie '$' []]
    
-- showTrie creates a multi-line string describing a trie in 
-- indented form (very much like the show function for indented 
-- representations of the family trees we discussed in class)
-- There will be an extra newline at the beginning of the result.
showTrie :: Int -> Trie -> String
showTrie level (MakeTrie c []) = "\n" ++ (indent level) ++ [c]
showTrie level (MakeTrie c [subTrie]) = 
    "\n" ++ (indent level) ++ c:(showTrie (level+1) subTrie)
showTrie level (MakeTrie c subTrieList) = 
    "\n" ++ (indent level) ++ 
    c:concat (map (showTrie (level+1)) subTrieList)
    
-- Helper function for showTrie: indent n returns a string with 
-- 2*n spaces in it.
indent :: Int -> String
indent n
    | n <= 0 = ""
    | otherwise = "  " ++ (indent (n-1))

-- Specify how tries will be displayed by the interpreter
instance Show Trie 
    where show t = tail (showTrie 0 t) -- getting rid of extra 
                                       -- newline at beginning
                                       -- of the showTrie result

-- A simple trie containing "cat", "can" and "dog".  You can use -- this trie for initial testing before you've written functions 
-- to help you create larger tries.
simpleTrie = 
    MakeTrie '.' [
        MakeTrie 'c' [
            MakeTrie 'a' [
                lastLetter 'n',
                lastLetter 't'
                ]
            ],
        MakeTrie 'd' [
                MakeTrie 'o' [
                    lastLetter 'g'
                ]
            ]
        ]

-- helper to make the above shorter:
-- a trie containing a single character at the end of a word 
lastLetter ch = MakeTrie ch [MakeTrie '$' []]

-- The trie from the picture on the assignment page.  (Note that -- "cat" is added twice and will not result in duplication in the 
-- trie.)  Uncomment this example for more help with testing
-- after you have written the createTrie function.
webTrie = createTrie ["catnip", "cat", "dog", "cab", "dime","dim", "candy", "cat", "catalog", "do"]

-----------helper functions---------------------------
getCharInTrie::Trie->Char
getCharInTrie (MakeTrie aChar _) = aChar


getTriesInTrie::Trie->[Trie]
getTriesInTrie (MakeTrie _ tires) = tires


contains x [] = False
contains x (y:ys) = (x == y) || contains x ys


path::Char->[Trie]->Trie
path aChar subTrieList = head [x |x<-subTrieList,(getCharInTrie x) == aChar]


charToString :: Char -> String
charToString c = [c]


sortSubTrieList::[Trie]->[Trie]
sortSubTrieList [] = []
sortSubTrieList (x:xs) =
    let smaller = sortSubTrieList [a | a<-xs,(getCharInTrie a) <= (getCharInTrie x)]
        bigger = sortSubTrieList [a | a<-xs,(getCharInTrie a) > (getCharInTrie x)]
    in smaller ++ [x] ++ bigger


string2Char::String->Char
string2Char [aChar] = aChar



------task functions--------------------------------
searchWord::String->Trie->Bool
searchWord aString aTrie = contains aString wordList
    where
        wordList = wordInTrie aTrie


wordInTrie::Trie->[String]
wordInTrie (MakeTrie '.' [MakeTrie '$' []]) = [""]
wordInTrie (MakeTrie '.' subTrieList) = concat (map wordInTrie subTrieList)
wordInTrie (MakeTrie aChar []) = [""]
--wordInTrie (MakeTrie aChar [MakeTrie '$' []]) = [(charToString aChar)]
--wordInTrie (MakeTrie aChar subTrieList) = if (head subTrieList) == (MakeTrie '$' []) then map ((charToString aChar) ++) ((concat (map wordInTrie subTrieList)) ++ [""]) else map ((charToString aChar) ++) (concat (map wordInTrie subTrieList))
wordInTrie (MakeTrie aChar subTrieList) = map ((charToString aChar) ++) (concat (map wordInTrie subTrieList))



addWordToTrie::String->Trie->Trie
addWordToTrie aString (MakeTrie aChar subTrieList)
    |length modifedString == 1 = if (contains (MakeTrie '$' []) subTrieList) then (MakeTrie aChar subTrieList) else (MakeTrie aChar (subTrieList ++ [MakeTrie '$' []]))
    |sameHead == True = (MakeTrie aChar modifiedSubTrieList)
    |otherwise = addWordToTrie modifedString (MakeTrie aChar (sortSubTrieList (subTrieList ++ [MakeTrie first []])))
    where
        modifedString = if ((last aString) /= '$') then (aString ++ "$") else aString
        subTireHead = map getCharInTrie subTrieList
        first = head modifedString
        sameHead = contains first subTireHead
        nextTire = path first subTrieList
        modifiedSubTrieList = sortSubTrieList ([x |x<-subTrieList,(getCharInTrie x) /=(getCharInTrie nextTire)] ++ [(addWordToTrie (tail modifedString) nextTire)])


createTrie::[String]->Trie
createTrie [] = emptyTrie
createTrie strings = foldl (\aTrie aString->addWordToTrie aString aTrie) (MakeTrie '.' []) strings


countChar::Char->Trie->Int
countChar ch (MakeTrie aChar subTrieList)
    |aChar == '$' = 0
    |ch == aChar = 1 + (sum (map (countChar ch) subTrieList))
    |otherwise = sum (map (countChar ch) subTrieList)