#随手一码
import random
import gc
from datetime import datetime

def check_Solution(csp):#看起来用不到了。
    pass


def init_greedy(size):
    rowStat = {}
    diagonalStat_R = {}
    diagonalStat_L = {}
    conflictCandidates = []
    current = []
    for col in range(1,size+1):
        minConflict = -1
        rowCandidate = {}
        for row in range(1,size+1):
            #------------------------------------- Calculate the number of conflict
            try:
                Conflict = diagonalStat_R[row + col][0]
            except KeyError:
                Conflict = 0
            try:
                Conflict += diagonalStat_L[row - col][0]
            except KeyError:
                pass
            try:
                Conflict += rowStat[row][0]
            except KeyError:
                pass
            #------------------------------------- check if the conflict is smaller than before
            if minConflict == -1:
                minConflict = Conflict
                rowCandidate[row] = 0
            if Conflict < minConflict:
                minConflict = Conflict
                rowCandidate.clear()
                rowCandidate[row] = 0
            if Conflict == minConflict:
                rowCandidate[row] = 0
        #------------------------------------- choose a candidate in the candidatelist with least conflict
        choice = random.choice(list(rowCandidate.keys()))
        #------------------------------------- modify the data list
        try:
            diagonalStat_R[choice + col][0] += 1
            diagonalStat_R[choice + col].append((col,choice))
        except KeyError:
            diagonalStat_R[choice + col] = [1,(col,choice)]
        try:
            diagonalStat_L[choice - col][0] += 1
            diagonalStat_L[choice - col].append((col,choice))
        except KeyError:
            diagonalStat_L[choice - col] = [1,(col,choice)]
        try:
            rowStat[choice][0] += 1
            rowStat[choice].append((col,choice))
        except KeyError:
            rowStat[choice] = [1,(col,choice)]
        if minConflict >0:
            conflictCandidates.append((col,choice))
        #------------------------------------- add the placement to the table
        current.append(choice)
    #------------------------------------- memory reduce
    del rowCandidate
    gc.collect()
    print("step1 done")
    return [current,rowStat,diagonalStat_R,diagonalStat_L,conflictCandidates]
        
        
def appendNoDupe(origin,aList):
    for item in aList:
        if not (item in origin):
            origin.append(item)
    return origin

def min_Conflicts(csp,max_Step=100):
    current = csp[0]
    rowStat = csp[1]
    diagonalStat_R = csp[2]
    diagonalStat_L = csp[3]
    conflictCandidates = csp[4]
    size = len(current)
    
    if conflictCandidates == []:
        return current
    
    for i in range(max_Step):
        candidate = random.choice(conflictCandidates)
        minConflict = -1
        rowCandidate = {}
        col = candidate[0]
        newConflict = []
        for row in range(1,size+1):
            if row == candidate[1]:
                continue
            #------------------ Calculate the number of conflict
            try:
                Conflict = diagonalStat_R[row + col][0]
            except KeyError:
                Conflict = 0
            try:
                Conflict += diagonalStat_L[row - col][0]
            except KeyError:
                pass
            try:
                Conflict += rowStat[row][0]
            except KeyError:
                pass
            #------------------------------------- check if the conflict is smaller than before
            if minConflict == -1:
                minConflict = Conflict
                rowCandidate[row] = 0
            if Conflict < minConflict:
                minConflict = Conflict
                rowCandidate.clear()
                rowCandidate[row] = 0
            if Conflict == minConflict:
                rowCandidate[row] = 0
        #--------------------------------------- modify the data list
        conflictCandidates.remove(candidate)
        diagonalStat_R[candidate[1] + col].remove(candidate)
        diagonalStat_R[candidate[1] + col][0] -= 1
        if diagonalStat_R[candidate[1] + col][0] == 1:
            try:
                conflictCandidates.remove(diagonalStat_R[candidate[1] + col][1])
            except:
                pass
        diagonalStat_L[candidate[1] - col].remove(candidate)
        diagonalStat_L[candidate[1] - col][0] -= 1
        if diagonalStat_L[candidate[1] - col][0] == 1:
            try:
                conflictCandidates.remove(diagonalStat_L[candidate[1] - col][1])
            except:
                pass
        rowStat[candidate[1]].remove(candidate)
        rowStat[candidate[1]][0] -= 1
        if rowStat[candidate[1]][0] == 1:
            try:
                conflictCandidates.remove(rowStat[candidate[1]][1])
            except:
                pass                                          
        #--------------------------------------- choose a candidate in the candidatelist with least conflict
        choice = random.choice(list(rowCandidate.keys()))
        #---------------------------------------
        try: #if there are new conflicts appears after the change
            diagonalStat_R[choice + col][0] += 1
            #--------------------------------------- add the new conflicts to the conflict candidate list
            newConflict += diagonalStat_R[choice + col][1:]

            diagonalStat_R[choice + col].append((candidate[0],choice))
        except KeyError: #if there are not we are fine
            diagonalStat_R[choice + col] = [1,(candidate[0],choice)]
            
        try:
            diagonalStat_L[choice - col][0] += 1
            newConflict += diagonalStat_L[choice - col][1:]
            diagonalStat_L[choice - col].append((candidate[0],choice))
        except KeyError:
            diagonalStat_L[choice - col] = [1,(candidate[0],choice)]
            
        try:
            rowStat[choice][0] += 1
            newConflict += rowStat[choice][1:]
            rowStat[choice].append((candidate[0],choice))
        except KeyError:
            rowStat[choice] = [1,(candidate[0],choice)]
        #--------------------------------------- append the new conflicts into the candidatelist with no dupelicates
        conflictCandidates = appendNoDupe(conflictCandidates,newConflict)
        
        #--------------------------------------- if the new position we find still have conflits we try to fix the table again
        if minConflict >0:
            conflictCandidates.append((candidate[0],choice))
        else: #--------------------------------------- we find a new position with no conflict, lets check if that is a solution
            print("check")
            print(conflictCandidates)
            if conflictCandidates == []:
                #------------------------------------- memory reduce
                del rowCandidate
                gc.collect()
                #------------------------------------- return the solution
                current[candidate[0]-1] = choice
                return current
        #------------------------------------- change the placing
        current[candidate[0]-1] = choice   
        #-------------------------------------memory reduce
        del rowCandidate
        gc.collect()
    #------------------------------------- Step exceed should try with another table  
    return False




def kejin(size):
    row_candi = []
    current = []
    perivious = -1
    for i in range(1,size+1):
        row_candi.append(i)
    for col in range(1,size+1):
        while True:
            currentchoice = random.choice(row_candi)
            row_candi.remove(currentchoice)
            if perivious == -1 or abs(perivious-currentchoice) != 1:
                perivious = currentchoice
                current.append(currentchoice)
                break
            else:
                row_candi.append(currentchoice)
    print(666)

                
            
            
        
        



def main():
##    for i in range(100):
##        kejin(100000)
    print("start")
    start=datetime.now() 
    result = min_Conflicts(init_greedy(10000))
    if result != False:
        end = datetime.now()
        print("solved")
        print((end-start).seconds)
#test run <100 size ~2s, <1000size ~10s,<10000 size ~130s maybe still can find better solution
    
    
    

main()
