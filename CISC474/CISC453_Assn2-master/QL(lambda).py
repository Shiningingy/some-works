# eligibility traces
import numpy
import random
import matplotlib.pyplot as plt

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
        plt.show()


def getMax(actions):
    maxVal = max(actions) # get max val
    allMax = []
    numAct = len(actions)
    for i in range(numAct):
        if maxVal == actions[i]:
            allMax.append(i)
    return allMax

def equal(action, aStar, maxActions):
    # aStar should be in maxActions
    if aStar not in maxActions:
        print("U screwed up")
    else:
        if action in maxActions:
            # is greedy
            return True
        else:
            # exploratory
            return False

class gridWorld:
    def __init__(self):
        self.i = 0
        self.j = 3
        self.states = []
        for x in range(10):
            for y in range(7):
                self.states.append((x,y))

    def currentState(self):
        return (self.i, self.j)

    # only 4 moves, deterministic wind
    def move(self, action):
        if (action == 0): # move right
            if (self.i < 9): # check out of bounds
                if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 6: # wind factor of 1
                    self.j += 1
                elif (self.i == 6 or self.i == 7) and self.j < 5: # wind factor of 2
                    self.j += 2
                self.i += 1
        elif (action == 1): # move up
            if (self.j < 6): # check out of bounds
                if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 5: # wind factor of 1
                    self.j += 2
                elif (self.i == 6 or self.i == 7) and self.j < 4: # wind factor of 2
                    self.j +=3
                else:
                    self.j += 1
        elif (action == 2): # move left
            if (self.i > 0): # check out of bounds
                if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 6: # wind factor of 1
                    self.j += 1
                elif (self.i == 6 or self.i == 7) and self.j < 5: # wind factor of 2
                    self.j += 2
                self.i -= 1
        elif (action == 3): # move down
            if (self.j > 0): # check out of bounds
                if (self.i == 3 or self.i == 4 or self.i == 5 or self.i == 8) and self.j < 6: # wind factor of 1
                    self.j += 0
                elif (self.i == 6 or self.i == 7) and self.j < 5: # wind factor of 2
                    self.j += 1
                else:
                    self.j -= 1


    def getReward(self, state):
        if state == (7,3):
            reward = 1
        else:
            reward = -1
        return reward


class QLearning:
    def __init__(self, gamma, alpha, epsilon, decay):
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.decay = decay # lambda
        # 4 moves for each of the 10 x and 7 y coords
        self.q = numpy.zeros(shape=(10,7,4))
        self.z = numpy.zeros(shape=(10,7,4)) # eligibility traces
        self.graph=Graph()

    def runAlg(self, forever):
        # number of episodes (games completed)
        final = []
        last = forever - 1
        for i in range(forever):
            converged = False
            count = 0
            grid = gridWorld()
            s = grid.currentState() # returns current coords
            #a = random.choice([0,1,2,3]) # first choice is random
            # just use greedy?
            temp = self.q[s[0]][s[1]]
            a = temp.argmax(axis=0)
            while grid.currentState() != (7,3): # win condition

                if i == last:
                    final.append(s)
                    
                # take action a, get r, s'
                grid.move(a)
                s2 = grid.currentState()
                r = grid.getReward(s2)

                # choose future action using Q table and e greedy
                actions = self.q[s2[0]][s2[1]]
                # will be a 1x4 array

                chance = random.random()

                # get indexes of all max values
                # for greedy and astar
                maxActions = getMax(actions)
                # choose actual action
                if chance <= self.epsilon:
                    # explore
                    action = random.randint(0,3)                    
                else:
                    # greedy      
                    action = random.choice(maxActions)

                # THIS IS DIFFERENT FROM SARSA
                # get maximum action
                # will have to compare with action for actual value
                aStar = random.choice(maxActions)
                # now have action, calculate delta
                count += 1
                delta = r + self.gamma*self.q[s2[0]][s2[1]][aStar] - self.q[s[0]][s[1]][a]
                if (abs(delta) < 0.0001) and (delta != 0):
                    if not(converged):
                        converged = True
                        self.graph.add_x(count)
                self.z[s[0]][s[1]][a] += 1 # eligibility
                # go through all states and actions
                #for m in range(10): # x
                    #for n in range(7): # y
                
                for j in range(4): # all actions
                    self.q[s[0]][s[1]][j] += self.alpha*delta*self.z[s[0]][s[1]][j]
                    # check if action and aStar are the same
                    if equal(action, aStar, maxActions):
                        # what is lambda?
                        self.z[s[0]][s[1]][j] = self.gamma*self.decay*self.z[s[0]][s[1]][j]
                    else:
                        self.z[s[0]][s[1]][j] = 0

                s = s2
                a = action
        final.append(s)
        return final

def draw(states):
    board = [['0' for x in range(10)] for y in range(7)]
    for i in states:
        board[i[1]][i[0]] = 'X'
    for i in board:
        print(i)
        
def main():
    gamma = 0.5
    alpha = 0.5
    epsilon = 0.1
    decay = 0.8
    forever = 200
    agent = QLearning(gamma, alpha, epsilon, decay)
    final = agent.runAlg(forever)
    print(final)
    draw(final)
    agent.graph.show()
main()





                
                
                    
                    
            
            
    
    
