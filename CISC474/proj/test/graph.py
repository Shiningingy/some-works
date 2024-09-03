import matplotlib.pyplot as plt
import numpy as np
class Graph():
    def __init__(self):
        self.x = []

    def add_x(self,x):
        self.x.append(x)

    def show(self,ylabel="Loss",xlabel="Episode",ro=False):
        if len(self.x)==1 or ro:
            plt.plot([i for i in range(1,len(self.x)+1)],self.x,"ro")
        else:
            plt.plot([i for i in range(1,len(self.x)+1)],self.x)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.show()


graph = Graph()
data = np.loadtxt("withBetterMemory_loss10000",delimiter=",")
for reward in data:
    graph.add_x(reward)
graph.show()
