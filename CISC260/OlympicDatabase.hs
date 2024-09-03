module OlympicDatabase where

{--
    a tuple describing an Olympic Result has five parts:
    1. The name of the sport (String)
    2. The year of the Olympic games (Int)
    3. The type of the medal (1=gold, 2=silver, 3=bronze)
    4. The name of the athlete (String)
    5. The athlete's country
--}
type Result = (String,Integer,Integer,String,String)
type ResultList = [Result]

{--
    results is a list of all of the results in the database.
    For convenience, I'm breaking the data up into sublists and 
    defining allResults as the concatenation of all of the sublists,
    but this doesn't make any difference to the type of ResultList
    and how you should use it.
    
    Student code will be tested with a different database that contains
    different events, years and athlete names, so please be careful not
    to make any assumptions based on the contents of this file.
    
    The facts in this file were taken from the following web sites:
    https://en.wikipedia.org/wiki/List_of_2010_Winter_Olympics_Result_winners    https://en.wikipedia.org/wiki/List_of_2014_Winter_Olympics_Result_winners
    https://en.wikipedia.org/wiki/List_of_2016_Summer_Olympics_Result_winners
    https://en.wikipedia.org/wiki/List_of_2012_Summer_Olympics_Result_winners

--}

results :: ResultList
results = [
    ("Women's Downhill Skiing", 2014, 3, "Lara Gut", "Switzerland"),
    ("Men's 3 m springboard diving", 2012, 3, "Patrick Hausding", "Germany"),
    ("Ice Dancing", 2010, 2, "Davis & White", "USA"),
    ("Men's 10 m platform diving", 2012, 3, "David Boudia", "USA"),
    ("Men's 200 Metre Race", 2016, 1, "Usain Bolt", "Jamaica"),
    ("Pairs Figure Skating", 2014, 1, "Volosozhar & Trankov", "Russia"),
    ("Men's Downhill Skiing", 2010, 3, "Bode Miller", "USA"),
    ("Women's Downhill Skiing", 2010, 3, "Elisabeth Gorgi", "Austria"),
    ("Women's Figure Skating", 2014, 2, "Kim Yuna", "South Korea"),
    ("Men's Downhill Skiing", 2014, 2, "Christof Innerhofer", "Italy"),
    ("Men's 100 Metre Race", 2016, 1, "Usain Bolt", "Jamaica"),
    ("Women's 3 m springboard diving", 2016, 1, "Shi Tinmao", "China"),
    ("Women's Figure Skating", 2014, 1, "Adelina Sotnikova", "Russia"),
    ("Ice Dancing", 2014, 1, "Davis & White", "USA"),
    ("Men's 200 Metre Race", 2016, 3, "Christophe Lemaitre", "France"),
    ("Men's 10 m platform diving", 2012, 2, "German Sanchez", "Mexico"),
    ("Men's Slalom", 2014, 1, "Mario Matt", "Austria"),
    ("Men's 200 Metre Race", 2012, 2, "Yohan Blake", "Canada"),
    ("Women's Downhill Skiing", 2010, 1, "Lindsey Vonn", "USA"),
    ("Women's 10 m platform diving", 2012, 1, "Ren Qian", "China"),
    ("Men's 100 Metre Race", 2016, 2, "Justin Gatlin", "USA"),
    ("Women's Figure Skating", 2010, 3, "Joannie Rochette", "Canada"), 
    ("Men's Figure Skating", 2010, 1, "Evan Lysacek", "USA"),
    ("Women's 3 m springboard diving", 2016, 2, "He Zi", "China"),
    ("Women's 100 Metre Race", 2012, 2, "Carmelita Jeter", "USA"),
    ("Men's 100 Metre Race", 2012, 3, "Justin Gatlin", "USA"),
    ("Men's Figure Skating", 2010, 3, "Daisuke Takahashi", "Japan"),
    ("Men's Downhill Skiing", 2014, 1, "Matthias Mayer", "Austria"),
    ("Men's 3 m springboard diving", 2016, 2, "Jack Laugher", "Great Britain"),
    ("Women's 10 m platform diving", 2012, 3, "Meaghan Benfeito", "Canada"),
    ("Women's Figure Skating", 2014, 3, "Carolina Kostner", "Italy"), 
    ("Men's Downhill Skiing", 2014, 3, "Kjetil Jansrud", "Norway"),
    ("Men's Figure Skating", 2010, 2, "Evgeni Plushenko", "Russia"),
    ("Women's 3 m springboard diving", 2016, 3, "tania Cagnotto", "Germany"),
    ("Women's 3 m springboard diving", 2012, 1, "Shi Tinmao", "China"),
    ("Men's 3 m springboard diving", 2012, 1, "Cao Yuan", "China"),
    ("Ice Dancing", 2014, 2, "Virtue & Moir", "Canada"),
    ("Women's Downhill Skiing", 2014, 1, "Dominique Gisin", "Switzerland"),
    ("Women's 200 Metre Race", 2016, 2, "Dafne Schippers", "Netherlands"),
    ("Men's 200 Metre Race", 2012, 3, "Warren Weir", "Jamaica"),
    ("Men's Slalom", 2014, 2, "Marcel Hirscher", "Austria"),
    ("Women's Slalom", 2014, 1, "Mikaela Shiffrin", "USA"),
    ("Women's Slalom", 2014, 3, "Kathrin Zettel", "Austria"),
    ("Men's 100 Metre Race", 2016, 3, "Andre De Grasse", "Canada"),
    ("Men's 3 m springboard diving", 2012, 2, "Jack Laugher", "Great Britain"),
    ("Men's Figure Skating", 2014, 1, "Yuzuru Hanyu", "Japan"),
    ("Men's 10 m platform diving", 2016, 2, "German Sanchez", "Mexico"),
    ("Men's Figure Skating", 2014, 2, "Patrick Chan", "Canada"),
    ("Women's 100 Metre Race", 2016, 1, "Elaine Thompson", "Jamaica"),
    ("Men's Slalom", 2010, 1, "Giuliano Razzoli", "Italy"),
    ("Men's Downhill Skiing", 2010, 1, "Didier Defago", "Switzerland"),
    ("Women's Slalom", 2010, 2, "Sarka Zahrobska", "Czech Republic"),
    ("Women's Figure Skating", 2010, 1, "Kim Yuna", "South Korea"),
    ("Pairs Figure Skating", 2014, 3, "Savchenko & Szolkowy", "Germany"),
    ("Women's 3 m springboard diving", 2012, 3, "tania Cagnotto", "Germany"),
    ("Men's Slalom", 2010, 2, "Ivica Kostelic", "Croatia"),
    ("Men's 10 m platform diving", 2016, 1, "Chen Aisen", "China"),
    ("Ice Dancing", 2010, 2, "Domnina & Shabalin", "Russia"),
    ("Women's Slalom", 2010, 2, "Marlies Schild", "Austria"),
    ("Women's 100 Metre Race", 2016, 3, "Shelly-Ann Fraser-Pryce", "Jamaica"),
    ("Women's 200 Metre Race", 2012, 3, "Carmelita Jeter", "USA"),
    ("Ice Dancing", 2014, 2, "Ilinykh & Katsalapov", "Russia"),
    ("Women's 3 m springboard diving", 2012, 2, "He Zi", "China"),
    ("Women's 200 Metre Race", 2012, 1, "Allyson Felix", "USA"),
    ("Pairs Figure Skating", 2010, 3, "Savchenko & Szolkowy", "Germany"),
    ("Women's 10 m platform diving", 2016, 3, "Meaghan Benfeito", "Canada"),
    ("Women's 100 Metre Race", 2012, 3, "Veronica Campbell-Brown", "Jamaica"),
    ("Men's 200 Metre Race", 2016, 2, "Andre De Grasse", "Canada"),
    ("Women's 10 m platform diving", 2016, 2, "Si Yajie", "China"),
    ("Men's 10 m platform diving", 2016, 3, "David Boudia", "USA"),
    ("Men's Figure Skating", 2014, 3, "Dennis Ten", "Kazakhstan"),
    ("Pairs Figure Skating", 2010, 2, "Pang & Tong", "China"),
    ("Men's 100 Metre Race", 2012, 2, "Yohan Blake", "Jamaica"),
    ("Men's Slalom", 2014, 3, "Henrik Kristoffersen", "Norway"),
    ("Pairs Figure Skating", 2010, 1, "Shen & Zhao", "China"),
    ("Women's Slalom", 2010, 1, "Maria Riesch", "Germany"),
    ("Men's Downhill Skiing", 2010, 2, "Aksel Lund Svindal", "Norway"),
    ("Women's 200 Metre Race", 2016, 3, "Tori Bowie", "USA"),
    ("Ice Dancing", 2010, 1, "Virtue & Moir", "Canada"),
    ("Men's Slalom", 2010, 3, "Andre Myhrer", "Sweden"),
    ("Men's 3 m springboard diving", 2016, 3, "Patrick Hausding", "Germany"),
    ("Men's 10 m platform diving", 2012, 1, "Chen Aisen", "China"),
    ("Women's 10 m platform diving", 2016, 1, "Ren Qian", "China"),
    ("Women's 100 Metre Race", 2012, 1, "Shelly-Ann Fraser-Pryce", "Jamaica"),
    ("Women's Figure Skating", 2010, 2, "Mao Asada", "Japan"),
    ("Women's Slalom", 2014, 2, "Marlies Schild", "Austria"),
    ("Men's 200 Metre Race", 2012, 1, "Usain Bolt", "Jamaica"),
    ("Men's 100 Metre Race", 2012, 1, "Usain Bolt", "Jamaica"),
    ("Women's 100 Metre Race", 2016, 2, "Tori Bowie", "USA"),
    ("Women's 200 Metre Race", 2016, 1, "Elaine Thompson", "Jamaica"),
    ("Women's Downhill Skiing", 2010, 1, "Julia Mancuso", "USA"),
    ("Women's 10 m platform diving", 2012, 2, "Si Yajie", "China"),
    ("Men's 3 m springboard diving", 2016, 1, "Cao Yuan", "China"),
    ("Pairs Figure Skating", 2014, 2, "Stolbova & Klimov", "Russia"),
    ("Women's Figure Skating", 2010, 1, "Kim Yuna", "South Korea"),
    ("Women's Downhill Skiing", 2014, 1, "Tina Maze", "Slovenia"),
    ("Women's 200 Metre Race", 2012, 2, "Shelly-Ann", "Fraser-Pryce")
    ] -- end of Results

              
              




