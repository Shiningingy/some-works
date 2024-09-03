type ShoppingList = [(String,Integer)]

shopList = [("eggs",12),("apples",4),("bananas",2)]

addItem::String->Integer->ShoppingList->ShoppingList

addItem name amount [] = [(name,amount)]

addItem name amount ((n1,num):xs)
	|name == n1 = (n1,num+amount):xs
	|otherwise = (n1,num) : addItem name amount xs





data Tree = Empty | MakeTree Tree Int Tree


examTree = MakeTree (MakeTree (MakeTree (MakeTree Empty 17 Empty) 25 (MakeTree Empty 30 (MakeTree (MakeTree Empty 38 Empty) 36 Empty))) 42 (MakeTree (MakeTree Empty 45 Empty) 49 Empty)) 57 (MakeTree (MakeTree (MakeTree Empty 52 Empty) 63 (MakeTree Empty 72 Empty)) 78 Empty)

leaves::Tree->[Int]
leaves Empty = []
leaves (MakeTree Empty value Empty) = [value]
leaves (MakeTree left value right) = (leaves left) ++ (leaves right)



addTree::Tree->Int->Tree
addTree Empty addValue = MakeTree Empty addValue Empty
addTree (MakeTree left value right) addValue
	|addValue > value = (MakeTree left value (addTree right addValue))
	|addValue < value = (MakeTree (addTree left addValue) value right)




three_functions::(Bool->Bool,
	Integer->Integer->Integer,
	Integer->Bool)
three_functions = (not,
	(+),
	(\n->n/=5))

first::(a,b,c) -> a
first (x,_,_) = x

second::(a,b,c) -> b
second (_,x,_) = x

third::(a,b,c) -> c
third (_,_,x) = x

three_f::Bool->Integer->Integer->Integer->(Bool,Integer,Bool)
three_f a b c d =  ((first three_functions) a,
	(second three_functions) b c,
	(third three_functions) d)