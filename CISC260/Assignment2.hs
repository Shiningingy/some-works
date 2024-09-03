-- |ZILI LUO, Student# 20001744
module Assignment2 where
import OlympicDatabase


doubleVowels::String->String
doubleVowels aString
    |aString == [] = []
    |first == "a" || first == "e" || first == "i" || first == "o" || first == "u" = (first ++ first) ++ (doubleVowels (tail aString))
    |otherwise = first ++ (doubleVowels (tail aString))
    where first = take 1 aString

pairFlip::[a]->[a]
pairFlip aList
    |length aList == 0 = []
    |length aList == 1 = aList
    |otherwise = (reverse (take 2 aList)) ++ (pairFlip (tail (tail aList)))

sublistSum::[Int]->Int->[[Int]]
sublistSum aList aNumber = [[] ++ sublist|sublist<-(sublists aList),(sum sublist) == aNumber]
    where 
    sublists :: [a] -> [[a]]
    sublists [] = [[]]
    sublists (x:xs) = [x:sublist | sublist <- sublists xs] ++ sublists xs

runnerUp :: String->Integer->ResultList->String
runnerUp eventname years medallist
    |namelist == [] = ""
    |otherwise = head namelist
    where
        namelist = [name|(event,year,medal,name,country)<-medallist,medal==2,event == eventname,year == years]


medals :: String->ResultList->[(String,Integer)]
medals athletename medallist
    |namelist == [] = []
    |otherwise = namelist
    where
        namelist = [(event,year)|(event,year,medal,name,country)<-medallist,medal == 1 || medal == 2 || medal == 3,name == athletename]

goldCount :: String->Integer->ResultList->Int
goldCount countryname years medallist
    |namelist == [] = 0
    |otherwise = length namelist
    where
    	namelist = [(name,event)|(event,year,medal,name,country)<-medallist,medal == 1,year == years,country == countryname]

