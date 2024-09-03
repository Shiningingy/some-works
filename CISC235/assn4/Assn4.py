#Student:ZiLi Luo
#20001744

#CISC235
#Assignment4 Code part

#I confirm that this submission is my own work and is consistent with
#the Queen's regulations on Academic Integrity.
import random

class linkedList:   #implement a linked list object
    def __init__(self,value, next=None):
        self.value = value
        self.next = next



def load_graphData(filename):
    graphs = []
    graph={}
    try:        #try to open the data file
        file = open(filename)
        for lines in file:
            line = lines.strip()
            while line.count("  ")>0:
                    line.replace("  "," ") #remove extra spaces
            if line[0].isdigit():
                if graph != {}:
                    graphs.append(graph)
                    graph = {}
            else:   #construct graph using adjacent list 
                item = line.split()
                if item[1] == 0:
                    graph[item[0]] = linkedList(None)
                    continue
                vertex = linkedList(None)
                current = vertex
                for i in range(2,len(item),2):
                    current.next = linkedList((item[i],int(item[i+1])))
                    current = current.next
                graph[item[0]] = vertex.next
        if graph != {}:
            graphs.append(graph)
        file.close() #close the file
        return graphs
    except FileNotFoundError:  #if the file do not exist
        print('cannot find file: ' + filename)
        return graphs
    except IOError:            #if the file can't be open
        print('cannot open file: '+ filename)
        return graphs


def getKeyList(keys):
    keyList = []
    for key in keys:
        keyList.append(key)
    return keyList


def BFS(graph):
    keyList = getKeyList(graph.keys())
    startVertex = random.choice(keyList) #start from a randon vertex
    visited = []
    total = 0
    queue = [startVertex]
    addToQueue = [startVertex]
    while len(queue) != 0:
        x = queue.pop(0)
        visited.append(x)
        y = graph[x]
        while y != None: #for all neighbours (y) of x
            value = y.value
            if (visited.count(value[0]) == 0) and (addToQueue.count(value[0]) == 0): #if y is not visited and y is not added to queue
                queue.append(value[0])
                addToQueue.append(value[0])
                total += value[1]   #add the weight of edge(x,y) to total weight of BFS
            y = y.next
    return total

def MSTUpdateHelper(smallestEdgeList,vertex,current): #a function to update the array when a vertex picked up
    while vertex != None:
        vertexState = smallestEdgeList[vertex.value[0]][0]
        value = smallestEdgeList[vertex.value[0]][1][1]
        if (value == -1) or (value >  vertex.value[1]): #if there exist a egde that is smaller than perivous one replace it.
            smallestEdgeList[vertex.value[0]] = (vertexState,(current,vertex.value[1]))
        vertex = vertex.next
        

def MST(graph):
    keyList = getKeyList(graph.keys())
    startVertex = random.choice(keyList)    #start from a randon vertex
    end = len(keyList)
    total = 0
    select = 1
    smallestEdgeList = {}
    for vertex in keyList:  #construct the 1-3 array
        smallestEdgeList[vertex] = (True,(None,-1)) #(inrest,smallestEdge)
        
    smallestEdgeList[startVertex] = (False,(None,-1))   #set state for the start vertex
    MSTUpdateHelper(smallestEdgeList,graph[startVertex],startVertex)

    while select < end: #while |T| < TotalVertex
        choosedVertex = (None,-1) #edge,weight
        for vertex in smallestEdgeList:
            vertexState = smallestEdgeList[vertex]
            try:
                vertexStateSm = smallestEdgeList[vertexState[1][0]]
            except KeyError:
                continue
            if (vertexState[0] == True) and (vertexStateSm[0] == False): #edge start in T end in R
                if (choosedVertex[1] == -1) or (choosedVertex[1] > vertexState[1][1]):
                    choosedVertex = (vertex,vertexState[1][1]) #pick up the least weight edge
           
        smallestEdgeList[choosedVertex[0]] = (False,(None,-1))  #set state for the picked vertex
        MSTUpdateHelper(smallestEdgeList,graph[choosedVertex[0]],choosedVertex[0]) #update the array
        select += 1
        total += choosedVertex[1]    #add the weight of edge(x,y) to total weight of MST
    return total




def main():
    testGraph = {"1":linkedList(("2",15),linkedList(("4",7),linkedList(("5",10)))),
                 "2":linkedList(("3",9),linkedList(("4",11),linkedList(("6",9),linkedList(("1",15))))),
                 "3":linkedList(("2",9),linkedList(("5",12),linkedList(("6",7)))),
                 "4":linkedList(("1",7),linkedList(("2",11),linkedList(("5",8),linkedList(("6",14))))),
                 "5":linkedList(("4",8),linkedList(("3",12),linkedList(("6",8),linkedList(("1",10))))),
                 "6":linkedList(("5",8),linkedList(("4",14),linkedList(("3",7),linkedList(("2",9)))))}
    graphs = load_graphData("Test_Cases.txt") #load the graph data
    print("start calculating, this may take 3~5 mins, please be patient")
    #calculate the diff by using pervious functions
    averageBFS = {}
    averageMST = {}
    count = {}
    for graph in graphs:
        BFStotal = BFS(graph)
        MSTtotal = MST(graph)
        key = len(graph)
        try:
            averageBFS[key] += BFStotal
            averageMST[key] += MSTtotal
            count[key] += 1
        except KeyError:
            averageBFS[key] = BFStotal
            averageMST[key] = MSTtotal
            count[key] = 1
    for key in count:
        averageBFS[key] = averageBFS[key]/count[key]
        averageMST[key] = averageMST[key]/count[key]
        print("average diff with graph size = " + str(key) + " is " + '{:.2f}'.format((averageBFS[key]/averageMST[key] - 1)*100) + "%") #print the result
            


main()
