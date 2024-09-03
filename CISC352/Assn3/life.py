'''
Yiwen Feng 20010649
Yifei Yin 20054101
Lixian Su 20033873
Zili Luo 20001744
Qianyu Zhang 20032962
'''
from tkinter import *
import math
import random
from datetime import datetime

class Graph():
        def __init__(self,WIDTH,HEIGHT,mygame,generation): #1 UNIT = 10*10 pixels
            self.gen = 0
            self.generation = int(generation)
            self.mygame = mygame
            self.row = HEIGHT
            self.col = WIDTH
            self.root = Tk()
            self.root.overrideredirect(True)
            self.root.geometry('%dx%d+%d+%d' % (820, 840, (self.root.winfo_screenwidth() - 800) / 2, (self.root.winfo_screenheight() - 840) / 2))
            self.root.bind_all('<Escape>', lambda event: event.widget.destroy())
            self.graph = Canvas(self.root, width=820, height=840, background='white')
            self.graph.after(500,self.update)
            self.graph.pack()
            self.root.mainloop()
            
        def update(self):
            start = datetime.now()
            self.graph.delete(ALL)
            if self.gen == self.generation + 1:
                self.graph.create_text(400,400,font = ('微软雅黑', 20, 'bold'),text="End",fill='magenta')
                return

            self.graph.create_text(400,20,font = ('微软雅黑', 10),text="Generation " + str(self.gen),fill='magenta')
            data = self.mygame.display()
            for row in range(self.row):
                for col in range(self.col):
                    if data[row][col] == "1":
                        self.graph.create_rectangle((800/self.col)*col +10,(800/self.row)*row + 30,(800/self.col)*(col+1)+10,(800/self.row)*(row+1)+30,fill = "black")
                    else:
                        self.graph.create_rectangle((800/self.col)*col +10,(800/self.row)*row + 30,(800/self.col)*(col+1)+10,(800/self.row)*(row+1)+30,fill = "white")
            self.mygame.step()
            self.gen += 1
            self.graph.after(int(2000 - (datetime.now()-start).total_seconds()*1000),self.update) #2sec per generation
            
        def exit(self):
                self.root.quit()
                self.root.destroy()
        
# version for homework
class Game(object):

    def __init__(self, state):
        self.state = state
        self.width = state.width
        self.height = state.height

    def step(self, count = 1):
        for generation in range(count):
            new_board = [[False] * self.width for row in range(self.height)]
            for x, row in enumerate(self.state.board):
                for y, cell in enumerate(row):
                    neighbours = self.neighbours(x, y)
                    previous_state = self.state.board[x][y]
                    live = (neighbours == 3) or (neighbours == 2 and previous_state == True)
                    new_board[x][y] = live
            self.state.board = new_board

    def neighbours(self, x, y):
        count = 0
        for hor in [-1, 0, 1]:
            for ver in [-1, 0, 1]:
                newhor = hor + x
                newver = ver + y
                if (not (hor == 0 and ver == 0)) and (0 <= newver < self.width and 0 <= newhor < self.height):                    
                    if self.state.board[newhor][newver] == True:
                        #print("newhor, newver: ", newhor, newver)
                        count += 1
        return count

    def display(self):
        return self.state.display()


class State(object):

    def __init__(self, positions, width, height):        
        self.board = self.board(positions, width, height)
        #print(self.board)
        self.width = width
        self.height = height

    def board(self, positions, width, height):
        active_cells = []
        # x is row index
        for x, row in enumerate(positions.splitlines()):
            # y is column index 
            for y, cell in enumerate(row.strip()):                
                if cell == '1':
                    active_cells.append((x,y))
        # index of the living grid
        #print(active_cells)
        
        # create a new board with 'ture' and 'false'
        board = [[False] * width for row in range(height)]        
        for cell in active_cells:
            board[cell[0]][cell[1]] = True
        return board
    
    

    def display(self):
        data = []
        line = ""
        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                if self.board[x][y]:
                    line += '1'
                else:
                    line += '0'
            data.append(line)
            line = ""
        return data


class Gamelife:
    def  __init__(self):
        self.data = self.getDisplayData()
        self.h = 0
        self.w = 0

    def readfile(self, file):
        with open(file, "r") as f:
            generation = f.readline()   # it's a string
            preglider = f.readlines()
            # width is the number of columns
            self.w = len(preglider[0]) - 1
            # height is the number of rows
            self.h = len(preglider)            
            s = ''
            glider = s.join(preglider)
            #print(self.w,self.h,glider)
            mygame = Game(State(glider, width = self.w, height = self.h))
            
            return mygame, generation

    def getDisplayData(self):
        mygame, generation = self.readfile('inLife.txt')
        self.Graph = Graph(self.w,self.h,mygame,generation)
        
                    
if __name__ == "__main__":
    outcome = Gamelife()


