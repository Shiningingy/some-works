'''
Written by Ella Stewart on 2019-11-12
Implements QLearning for the Windy Grid World
'''
import random
import numpy 

'''
Sets up the grid to be used for Qlearning
Initializes coordinates as start state
Moves states given an action
'''
class gridWorld:

    # Constructor that initializes start state and all possible states
    def __init__(self):
        self.i = 0
        self.j = 3
        self.states = []
        for x in range(10):
            for y in range(7):
                self.states.append((x, y))

    def getWind(self): # given a position, randomly returns a wind (in the y or j direction)
        # don't worry about bounds, handled in moveState
        light = [0,1,2] # light wind, randomly choose one
        heavy = [1,2,3] # heavy wind
        if (self.i >= 3 and self.i <=5 or self.i == 8): # average is 1
            choice = random.choice(light)
        elif (self.i == 6 or self.i == 7): # average is 2
            choice = random.choice(heavy)
        else: # no wind
            choice = 0
        return choice

    # Moves i and j given an action
    def moveState(self, action):
        # take action first, then get wind, check if out of bounds, if so, don't assign temp (no movement)
        # if we take a move, this is where we would land - need to check if valid
        tempI = 0 
        tempJ = 0
        
        if (action == 0): # move right
            tempI = self.i + 1
        elif (action == 1): # move up
            tempJ = self.j - 1
        elif (action == 2): # move left
            tempI = self.i - 1
        elif (action == 3): # move down
            tempJ = self.j + 1
        elif (action == 4): # move right-up
            tempI = self.i + 1
            tempJ = self.j - 1
        elif (action == 5): # move left-up
            tempI = self.i - 1
            tempJ = self.j - 1
        elif (action == 6): # move right-down
            tempI = self.i + 1
            tempJ = self.j + 1
        elif (action == 7): # move left-down
            tempI = self.i - 1
            tempJ = self.j + 1
        wind = self.getWind()
        tempJ += wind
        # check bounds, only assign if in bounds
        if tempI > 0 and tempI < 10 and tempJ > 0 and tempJ < 7:
            self.i = tempI
            self.j = tempJ
        


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

        # 70 x 4 qTable
        # 70 states, 8 actions
        self.qTable = numpy.zeros((70,8))

    # Called to the the QLearning algorithm
    def runAlgorithm(self):

        # Large number of episodes
        for i in range(10000):
            #print(i)
            # Print states visited in order in final round
            if i == 9999:
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
                    action = random.randint(0, 7)
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

                maxA = (numpy.ndarray.tolist(possibleActions)).index(max(possibleActions))
                qSA = self.qTable[index1][action]
                # Update QTable
                self.qTable[index1][action] = qSA + self.alpha*(reward + self.gamma*self.qTable[index2][maxA] - qSA)
                S = S2  # S <- S'

        return finalStates
    def optimalPolicy(self):
        optimalPolicy = numpy.zeros((7, 10))
        for i in range(70):
            row = i // 7
            column = i % 7

            optimalPolicy[column][row] = (numpy.ndarray.tolist(self.qTable[i])).index(max(self.qTable[i]))

        print(optimalPolicy)

def main():

    agent = QLearning(0.5, 0.5, 0.1)
    finalStates = agent.runAlgorithm()
    print(finalStates)
    agent.optimalPolicy()

main()















