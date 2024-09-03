{-
    A recursive algebraic type for a family tree
    CISC 260, winter 2018
    author: M. Lamb
-}
module FamilyTree where
  
-- Each person has a name (a String).  
-- Every person also has zero or more children, who are themselves people.
data Person = MakePerson String [Person]

-- Example: the queen and all her descendants
-- I could have written the queen's family with one big
-- nested expression, but I think it's more readable when
-- it's broken up like this.  (And it's harder to mess up
-- all the parenthesis and brackets!)
queen = MakePerson "Elizabeth" [charles, anne, andrew, edward]
anne = MakePerson "Anne" [peter,zara]
beatrice = MakePerson "Beatrice" []
andrew = MakePerson "Andrew" [beatrice,eugenia]
charles = MakePerson "Charles" [william,harry]
edward = MakePerson "Edward" [louise,james]
eugenia = MakePerson "Eugenia" []
harry = MakePerson "Harry" []
james = MakePerson "James" []
louise = MakePerson "Louise" []
peter = MakePerson "Peter" []
william = MakePerson "William" []
zara = MakePerson "Zara" []

-- Another family tree as one big expression (George was my grandfather)
grandpa = MakePerson "George" [
    MakePerson "Helen" [
      MakePerson "Margaret" [
        MakePerson "Carolyn" [],
        MakePerson "Alan" [],
        MakePerson "Ian" []
      ],
      MakePerson "Barbara" []
    ],
    MakePerson "Dorothy" [
      MakePerson "Janet" [],
      MakePerson "Danny" [
        MakePerson "Tiffani" [],
        MakePerson "Dana" []
      ],
      MakePerson "Jimmy" [MakePerson "James" []]
    ]
  ]
  
-- Define what it means to display a family tree.  For this type, we're 
-- defining it to mean that we display an indented form of the tree.

-- Create a multi-line string to display a person's family tree
showPerson :: Person -> String
showPerson p = showPersonWithIndent p 0

-- Create a multi-line string to display a person's family tree,
-- starting with a specified level of indentation
showPersonWithIndent (MakePerson name kids) level =
    (indent level) ++ name ++ "\n" ++
    (showKidsWithIndent) kids (level+1)
    
-- Create a multi-line string to display a list of people,
-- starting with a specified level of indentation
showKidsWithIndent [] _ = []
showKidsWithIndent (kid:kids) level =
    (showPersonWithIndent kid level) ++ (showKidsWithIndent kids level)

instance Show Person where
    show person = showPerson person 

-- A string of spaces for indenting a line (4 spaces per level)
indent :: Int -> String
indent 0 = ""
indent n = "    " ++ (indent (n-1))

-- Returns a person's name
getName :: Person -> String
getName (MakePerson name _) = name

-- Returns a list of a person's children (a list of the tree structures
-- representing each child)
getKids :: Person -> [Person]
getKids (MakePerson _ kids) = kids

-- Returns a list of a person's children's names
childNames :: Person -> [String]
childNames tree = map getName (getKids tree)
    
-- Returns a list of all the names in a family tree
-- Note: the concat function takes a list of lists and mashes them into
-- a single list.  For example, concat [[1,2],[3,4,5],[6]] = [1,2,3,4,5,6]
allNames :: Person -> [String]
allNames (MakePerson name kids) =
    name : (concat (map allNames kids))

-- Searches for a name in a family tree
search :: String -> Person -> Bool
search target (MakePerson name kids)
    | name == target = True
    | otherwise = or (map (search target) kids)

-- Adds a new person to a family tree, producing a new family tree
-- Parameters: family tree, name of parent, name of child
-- Assumption: no duplicate names allowed
-- If the parent is not in the family tree, the tree is unchanged.
addDescendent :: Person -> String -> String -> Person
addDescendent (MakePerson name kids) parentName childName
    | name == parentName = (MakePerson name (kids ++ [newPerson]))
    -- We can call addDescendent recursively for every subtree.  
    -- Our assumption means that this will add the new child to at most
    -- one sub-tree.
    | otherwise = (MakePerson name 
        (map (\tree -> addDescendent tree parentName childName) kids))
    where
    -- newPerson is a tree representing the new child
    newPerson = MakePerson childName []

-- Suggestions for experimenting:
-- 1. Write a function that counts the number of people 
--    in a tree
-- 2. Write a function that returns the maximum depth of a
--    tree (the length of the longest path from the root to
--    a leaf)
-- 3. Write a more efficient version of addDescendent.  Instead
--    of using the map, make the function stop as soon as it
--    has found the parent and added the child.  This will
--    require a helper function that reports success or failure.
-- 4. Write a function that deletes a person and all of 
--    their descendants from a tree -- taking a tree and the
--    name of a person as parameters.
    
personCount::Person->Int
personCount (MakePerson _ []) = 1
personCount (MakePerson _ child) = sum (map personCount child) + 1

initialCount::Char->Person->Int
initialCount initial (MakePerson (x:xs) [])
  |initial==x=1
  |otherwise = 0
initialCount initial (MakePerson (x:xs) kids)
  |initial == x = sum (map (initialCount initial) kids) + 1
  |otherwise = sum (map (initialCount initial) kids)



