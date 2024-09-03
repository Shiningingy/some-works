'''-------------------------------------------
Student:Zili Luo
Student#:20001744

CISC 235
Assignment 1
Programming part
-------------------------------------------'''


import time
import random

def initValueList(listLength):
    newValueList = []
    for i in range(listLength):
        newValueList.append(random.randrange(0,listLength+1,2))
    return newValueList

def initTargetList(listLength,valueList,valueListLength):
    newTargetList = []
    for i in range(listLength // 2):
        newTargetList.append(random.choice(valueList))
    for i in range(listLength//2,listLength):
        newTargetList.append(random.randrange(1,valueListLength+1,2))
    return newTargetList


def binarySearch(aList,targetValue):
    low = 0
    high = len(aList) - 1
    while high >= low:
        mid = (low + high) // 2
        if(targetValue == aList[mid]):
            #if u want to see the result being printed remove the # before print
            #print(str(targetvalue) + "in the List?:yes" )
            return 
        if(targetValue < aList[mid]):
            high = mid - 1
        else:
            low = mid + 1
    #if u want to see the result being printed remove the # before print
    #print(str(targetvalue) + "in the List?:no" )
    return

def linearSearch(aList,targetValue):
    for value in aList:
        if value == targetValue:
            #if u want to see the result being printed remove the # before print
            #print(str(targetvalue) + "in the List?:yes" )
            return
    #if u want to see the result being printed remove the # before print
    #print(str(targetvalue) + "in the List?:no" )


    
def quickSort(aList):
    if len(aList) < 2:
        return aList
    less,equal,greater = [] , [] , []
    startValue = aList[0]
    for value in aList:
        if value < startValue:
            less.append(value)
        elif value > startValue:
            greater.append(value)
        else:
            equal.append(value)
    return quickSort(less) + equal + quickSort(greater)

def timeOfAlgoMA(valueList,targetList):
    start = time.time()
    for i in range(500):
        for targetValue in targetList:
            linearSearch(valueList,targetValue)
    return (time.time() - start) / 500

def timeOfAlgoMB(valueList,targetList):
    start = time.time()
    valueListSorted = quickSort(valueList)
    totalSortTime = time.time() - start
    start = time.time()
    for i in range(500):
        for targetValue in targetList:
            binarySearch(valueListSorted,targetValue)
    return (time.time() - start) / 500 + totalSortTime

def main():
    valueListLength = [1000,2000,4000,8000,16000]
    targetListLength = 10
    for listLength in valueListLength:
        while True:
            valueList = initValueList(listLength)
            targetList = initTargetList(targetListLength,valueList,listLength)
            timeAlgoMA = timeOfAlgoMA(valueList,targetList)
            timeAlgoMB = timeOfAlgoMB(valueList,targetList)
            if timeAlgoMA > timeAlgoMB:
                print("when (valueListLength)n = " + str(listLength) + " k = " + str(targetListLength) + " to make Algorithm B faster than Algorithm A")
                break
            else:
                targetListLength += 1
            
        
main()    
