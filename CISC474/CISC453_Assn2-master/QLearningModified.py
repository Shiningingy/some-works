'''
Written by Ella Stewart on 2019-11-12
Implements QLearning for the Windy Grid World
'''
import random
import numpy
import matplotlib.pyplot as plt

'''
Sets up the grid to be used for Qlearning
Initializes coordinates as start state
Moves states given an action
'''


class Graph():
    def __init__(self):
        self.x = []

    def add_x(self,x):
        self.x.append(x)

    def show(self,ylabel="Num of steps take to converage",xlabel="Episode",ro=False):
        print([i for i in range(1,len(self.x)+1)])
        if len(self.x)==1 or ro:
            plt.plot([i for i in range(1,len(self.x)+1)],self.x,"ro")
        else:
            plt.plot([i for i in range(1,len(self.x)+1)],self.x)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.axis([0, 200, 0, 800])
        plt.show()
        
class gridWorld:

    # Constructor that initializes start state and all possible states
    def __init__(self):
        self.i = 0
        self.j = 3
        self.states = []
        for x in range(10):
            for y in range(7):
                self.states.append((x, y))

    # Moves i and j given an action
    def moveState(self, action):
        if (action == 0): # move right
            temp = [self.i, self.j]
            if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 6: # wind factor of 1
                temp[1] += 1
            elif (self.i == 6 or self.i == 7) and self.j < 5: # wind factor of 2
                temp[1] += 2
##            if (self.i < 9): # check out of bounds
##                if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 6: # wind factor of 1
##                    self.j += 1
##                elif (self.i == 6 or self.i == 7) and self.j < 5: # wind factor of 2
##                    self.j += 2
##                self.i += 1
            temp[0] += 1
        elif (action == 1): # move up
            temp = [self.i, self.j]
            if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 5: # wind factor of 1
                temp[1] += 2
            elif (self.i == 6 or self.i == 7) and self.j < 4: # wind factor of 2
                temp[1] += 3
            else:
                temp[1] += 1
##            if (self.j < 6): # check out of bounds
##                if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 5: # wind factor of 1
##                    self.j += 2
##                elif (self.i == 6 or self.i == 7) and self.j < 4: # wind factor of 2
##                    self.j +=3
##                else:
##                    self.j += 1 # WHY ARE YOU ADDING. MOVING UP SHOULD BE - ?
           
        elif (action == 2): # move left
            temp = [self.i, self.j]
            if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 6: # wind factor of 1
                temp[1] += 1
            elif (self.i == 6 or self.i == 7) and self.j < 5: # wind factor of 2
                temp[1] += 2
##            if (self.i > 0): # check out of bounds
##                if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 6: # wind factor of 1
##                    self.j += 1
##                elif (self.i == 6 or self.i == 7) and self.j < 5: # wind factor of 2
##                    self.j += 2
##                self.i -= 1
            temp[0] -= 1
        elif (action == 3): # move down
            temp = [self.i, self.j]
            if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 6: # wind factor of 1
                temp[1] += 0
            elif (self.i == 6 or self.i == 7) and self.j < 5: # wind factor of 2
                temp[1] += 1
            else:
                temp[1] -= 1
##            if (self.j > 0): # check out of bounds
##                if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 6: # wind factor of 1
##                    self.j += 0
##                elif (self.i == 6 or self.i == 7) and self.j < 5: # wind factor of 2
##                    self.j += 1
##                else:
##                    self.j -= 1
        # CHECK OUT OF BOUNDS, IF OUT DONT CHANGE
        if temp[0] >= 0 and temp[0] <= 9 and temp[1] >= 0 and temp[1] <= 6:
            self.i = temp[0]
            self.j = temp[1]

    # Returns current state as tuple
    def getCurrentState(self):
        currentState = (self.i, self.j)
        return currentState

    # Accessor for the states
    def getStates(self):
        return self.states

    # Defines rewards for each state
    def getReward(self, state):
        if state == (7, 3):
            reward = 1
        else:
            reward = -1
        return reward

'''
Used to implement the QLearning algorithm
Creates instance of grid
Initializes qTable
'''
class QLearning:

    # Adjustable gamma, alpha and epsilon parameters
    def __init__(self, gamma, alpha, epsilon):
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.graph = Graph()
        # 70 x 4 qTable
        # 70 states, 4 actions
        self.qTable = numpy.zeros((70,4))

    # Called to the the QLearning algorithm
    def runAlgorithm(self):
##        finalStates = []
        # Large number of episodes
        for i in range(201):
            converged = False
            count = 0
            #print(i)
            # Print states visited in order in final round
            if i == 200:
                finalStates = []
            # Initializing grid and getting current state
            grid = gridWorld()
            S = grid.getCurrentState()
            if i == 9999:
                finalStates.append(S)
            states = grid.getStates()

            # Episode ends at goal state (3,7) on grid
            while grid.getCurrentState() != (7, 3):
                # Get the possible actions
                index1 = states.index(S)
                actionValues = self.qTable[index1]

                # Determines greedy or random
                num = random.random()

                if num <= self.epsilon:
                    # Random action
                    action = random.randint(0, 3)
                else:
                    # Greedy action
                    action = (numpy.ndarray.tolist(actionValues)).index(max(actionValues))

                # Observe S' and R
                grid.moveState(action)
                S2 = grid.getCurrentState()
                reward = grid.getReward(S2)

                # Append state to list if final episode
                if i == 9999:
                    finalStates.append(S2)

                # Get possible A'
                index2 = states.index(S2)
                possibleActions = self.qTable[index2]
                count += 1
                maxA = (numpy.ndarray.tolist(possibleActions)).index(max(possibleActions))
                qSA = self.qTable[index1][action]
                newQ = self.alpha*(reward + self.gamma*self.qTable[index2][maxA] - qSA)
                # Update QTable
                self.qTable[index1][action] = qSA + newQ
                if (abs(newQ) < 0.0001) and (newQ != 0):
                    if not(converged):
                        converged = True
                        self.graph.add_x(count)
                S = S2  # S <- S'

        return finalStates

def main():

    agent = QLearning(0.5, 0.5, 0.1)
    finalStates = agent.runAlgorithm()
    print(finalStates)
    agent.graph.show()
    

main()















