

#I confirm that this submission is my own work and is consistent with
#the Queen's regulations on Academic Integrity.
import random

class hashtable: #implement a hashtable object.

    def __init__(self,size):
        self.size = size
        self.table = {}
        for i in range(size):  #init hashtable of intal size
            self.table[i] = "" #assign inital values(empty)

    def quadraticProbing_InsertList(self,valueList,c1,c2):
        complete = False
        while not complete:
            for valuestr in valueList:
                value = str2Int(valuestr) #convernt str to int
                currentProbeLen = 1
                v = value % self.size
                a = v
                while (currentProbeLen < 4) and (self.table[a] != ""): #while insertion is complete or failed
                    currentProbeLen += 1
                    a = (v + int(c1*currentProbeLen) + int(c2*(currentProbeLen**2))) % self.size
                if currentProbeLen <= 3: #if the currentprobelen <= 3    
                    if self.table[a] == "": #if insertion succeed
                        self.table[a] = valuestr
                        currentProbeLen = 1
                        if valuestr == valueList[-1]: #if all the elements in List are inserted then insertion is complete
                            complete = True
                else:    #if the currentprobelen >3 we need to
                    len = 0
                    self.size += 1      #re size the hashtable by adding 1 to current size and flush the table.
                    for i in range(self.size):
                        self.table[i] = ""
                    break

                
    def doubleHashing_InsertList(self,valueList,hashfunc1,hashfunc2):
        complete = False
        while not complete:
            for valuestr in valueList:
                value = str2Int(valuestr)
                currentProbeLen = 1
                v1 = hashfunc1(value,self.size) #v1 = h(k)
                v2 = hashfunc2(value,self.size) #v2 = h'(k)
                a = v1
                while (currentProbeLen < 4) and (self.table[a] != ""):#while insertion is complete or failed
                    currentProbeLen += 1
                    a = (v1 + currentProbeLen*v2) % self.size
                if currentProbeLen <= 3: #if the currentprobelen <= 3    
                    if self.table[a] == "": #if insertion succeed
                        self.table[a] = valuestr
                        currentProbeLen = 1
                        if valuestr == valueList[-1]: #if all the elements in List are inserted then insertion is complete
                            complete = True
                else:    #if the currentprobelen >3 we need to
                    len = 0
                    self.size += 1      #re size the hashtable by adding 1 to current size and flush the table.
                    for i in range(self.size):
                        self.table[i] = ""
                    break




                    

def str2Int(word): #convernt str to int by get ASCII value of characters in str
    value = ""     #and then minus 67 to ensure all of them have to digits
    for character in word:
        value += str(ord(character)-67) #then put them together
    return int(value) #and return int value of it.



def load_wordList():
    wordList = []
    try:        #try to open the data file
        file = open("HOTNCU_code_names_2018_4657.txt")
        for line in file:
            wordList.append(line.strip()) #add datas into wordList
        file.close() #close the file
        return wordList
    except FileNotFoundError:  #if the file do not exist
        print('cannot find file')
        return wordList
    except IOError:            #if the file can't be open
        print('cannot open file')
        return wordList



def doubleHash_mod(k,m): #double hash function that return k mod m
    return k % m


def doubleHash_square(k,m):#double hash function that return k^2
    return k^2


def doubleHash_sumOfDigits(k,m):#double hash function that return sum of all digits of k
    result = 0
    while k!=0:
        result += k % 10
        k = k // 10
    return result

def randomchoice(aList,size):
    try:
        newList = random.sample(aList, size)
        return newList
    except ValueError:
        print("source size is smaller than excepted!!")
        return aList
        
            
def main():
    aList=randomchoice(load_wordList(),4000) # get a random sample size of 4000 from the movie pool
    hashTable = hashtable(4000) #by the instrusion the table size will > 4000 so i set inital size at 4000
    hashTable.quadraticProbing_InsertList(aList,1,1)
    print("table size for quadratic probing when c1=1 , c2=1 (self probe length <=3):")
    print(hashTable.size)
    
    hashTable = hashtable(4000)
    hashTable.quadraticProbing_InsertList(aList,2,0.5)
    print("table size for quadratic probing when c1=2 , c2=0.5 (self probe length <=3):")
    print(hashTable.size)

    hashTable = hashtable(4000)
    hashTable.quadraticProbing_InsertList(aList,0.5,2)
    print("table size for quadratic probing when c1=0.5 , c2=2 (self probe length <=3):")
    print(hashTable.size)

    hashTable = hashtable(4000)
    hashTable.doubleHashing_InsertList(aList,doubleHash_mod,doubleHash_square)
    print("table size for double hashing when h(k)' = k % m , h(k)'' = k^2 (self probe length <=3):")
    print(hashTable.size)

    hashTable = hashtable(4000)
    hashTable.doubleHashing_InsertList(aList,doubleHash_sumOfDigits,doubleHash_square)
    print("table size for double hashing when h(k)' = \"sum of all digits of k\" , h(k)'' = k^2 (self probe length <=3):")
    print(hashTable.size)

    hashTable = hashtable(2500)
    hashTable.doubleHashing_InsertList(aList,doubleHash_mod,doubleHash_sumOfDigits)
    print("table size for double hashing when h(k)' = k % m , h(k)'' = \"sum of all digits of k\" (self probe length <=3):")
    print(hashTable.size)
    
main()
