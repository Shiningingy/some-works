-- |ZILI LUO, Student# 20001744
shape :: Double -> Double -> Double -> Char
shape a b c
    | a <= 0 || b <= 0 || c <= 0 = 'X'
    | a == b && a == c && b == c = 'S'
    | a == b || a == c || b == c = 'F'
    | otherwise = 'E'


volume :: Double -> Double -> Double -> Double
volume a b c
    | a < 0 || b < 0 || c < 0 = error "ellipsoid with negative side(s)"
	| a == 0 || b == 0 || c == 0 = 0.0
	| otherwise = 4/3*pi*a*b*c

logSum :: Int -> Int -> Double
logSum a b 
	| a == b = log (fromIntegral a)
	| a > b = 0.0
	| otherwise = logSum (a+1) b + log (fromIntegral a)



growET :: Double -> Int -> Double
growET mass 0 = mass
growET mass day
	| mass < 0 = error "initial mass less than zero"
	| mass >= 0 && day < 0 = error "days are less than zero"
	| mass >= 0 && day > 100 = error "no ET has been observed to survive for more than 100 days"
	| day == 0 = mass
	| mass < 1 = growET (mass*2) (day-1)
	| mass >= 1 && mass < 20 = growET (mass*1.5+2) (day-1)
	| mass >= 20 && mass < 100 = growET (mass*1.2+1) (day-1)
	| mass >= 100 = growET (mass*1.1+0.5) (day-1)


