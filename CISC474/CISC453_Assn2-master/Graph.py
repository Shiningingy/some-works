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
