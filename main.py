from tkinter import *
from PIL import ImageTk, Image

import time
from random import choices

#для дейкстры с кучами
import sys
import heapq

#задаем параметры окна и холста
tk = Tk()

tk.title('Minecraft 2D')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)

canvas = Canvas(tk, width=300, height=595, highlightthickness=0)


# говорим холсту, что у каждого видимого элемента будут свои отдельные координаты
canvas.pack()


# обновляем окно с холстом
tk.update()

#картинки
miner_img = ImageTk.PhotoImage(Image.open('steve.png'))
stone = ImageTk.PhotoImage(Image.open('stone.jpg'))
diamond = ImageTk.PhotoImage(Image.open('diamond.png'))
dirt = ImageTk.PhotoImage(Image.open('dirt.png'))
coal = ImageTk.PhotoImage(Image.open('coal.png'))
gold = ImageTk.PhotoImage(Image.open('gold.png'))
iron = ImageTk.PhotoImage(Image.open('iron_ore.png'))
grass = ImageTk.PhotoImage(Image.open('grass.png'))
b_g = ImageTk.PhotoImage(Image.open('bg1.png'))
st = ImageTk.PhotoImage(Image.open('startmenu.png'))
canvas.create_image(0, 0, image=st)

#счет
score = 0

#шахтер
class Miner:
    def __init__(self, canvas):
        self.score = 0
        self.sc = canvas.create_text(260, 20, text=self.score, font=('Comic Sans MS', 15), fill='white')
        self.canvas = canvas
        # создаем шахтера
        self.id = canvas.create_image(0,0,image=miner_img)
        # создаем стартовую надпись
        self.sm = canvas.create_image(150, 150, image=st)
        #удаленные блоки
        self.deleted = []

        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

        self.canvas.move(self.id, 135, 210)
        self.x = 0
        self.y = 0

        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Down>', self.down)
        self.started = False
        self.finished = False
        self.finished_ai = False
        self.ai = False
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)


    def turn_right(self, event):
        if self.y == 0 and self.started:
            self.x = 30

    def turn_left(self, event):
        if self.y == 0 and self.started:
            self.x = -30

    def down(self, event):
        if self.x == 0 and self.started:
            self.y = 30


    # игра начинается

    def start_game(self, event):
        self.started = True
        self.canvas.delete(self.sm)

    # конец игры
    def end_game(self):
        self.canvas.itemconfig(self.sc, text='Weight: {}'.format(self.score), font=('Comic Sans MS', 20))
        self.canvas.move(self.sc, -110, 100)

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        self.x = 0
        self.y = 0
        pos = self.canvas.coords(self.id)
        
        

        for i in range(len(cave.ls)):
            if pos[0]-cave.ls[i][0] == 15 and pos[1]-cave.ls[i][1] == 5:
                self.score += cave.blocks[i][1]
                self.canvas.itemconfig(self.sc, text=self.score)
                cave.blocks[i][1] = 0
                self.deleted.append(cave.blocks[i][0])
                self.canvas.delete(cave.blocks[i][0])
        for i in range(len(cave.dirt)):
            if pos[0]-cave.dirt[i][0] == 15 and pos[1]-cave.dirt[i][1] == 5:
                self.deleted.append(cave.dirty[i])
                self.canvas.delete(cave.dirty[i]) 

        if pos[0]-10 <= 0:
            self.x = 30
        elif pos[0] >= self.canvas_width:
            self.x = -30
        elif pos[1]+10 >= self.canvas_height:
            self.y = -30
            self.finished = True
            self.canvas.unbind_all("<KeyPress-Right>")
            self.canvas.unbind_all("<KeyPress-Left>")
            self.canvas.unbind_all("<KeyPress-Down>")
            
        
    #искусственный интеллект
    def AI(self, weight):
        
        node_ls = []
        for i in range(1, 101):
            node_ls.append(Node(i))
        edge_ls = []
        vert_ls = []
        way = []
        for i in range(len(weight)):
            edge_ls.append(Edge(weight[i][0], node_ls[weight[i][1]-1], node_ls[weight[i][2]-1]))
            vert_ls.append(weight[i][1]-1)
        for x in range(len(edge_ls)):
            node_ls[vert_ls[x]].adjacenciesList.append(edge_ls[x])

        vertexlist = tuple(node_ls)
        calculateshortestpath(vertexlist, node_ls[0])
        getshortestpath(node_ls[99], way)
        print(way)
        if cave.recover_blocks(self.deleted):
            self.canvas.delete(self.id)
            self.id = canvas.create_image(15,290,image=miner_img)
            
        score = way[-1]
        self.canvas.itemconfig(self.sc, text="NOW IT'S MY TURN!", font=('Comic Sans MS', 12))
        way.pop()
        way.reverse()
        print(way)
        for i in range(len(way)-1):
            print(len(way))
            self.x, self.y = 0, 0
            if way[i+1] - way[i] == 10:
                self.down(None)
                print(self.x, self.y, 1)
                
            if way[i+1] - way[i] == 1:
                self.turn_right(None)
                print(self.x, self.y, 2)

            if way[i+1] - way[i] == -1:
                self.turn_left(None)
                print(self.x, self.y, 3)
            tk.after(500, ai_call.__next__)
            yield
            self.canvas.itemconfig(self.sc, text='', font=('Comic Sans MS', 20))
        self.canvas.itemconfig(self.sc, text='Weight: {}'.format(score), font=('Comic Sans MS', 20))
        self.down(None)
        self.finished_ai = True
        
              


            
            

        
        


# пещера
class Cave:
    def __init__(self, canvas):
        self.canvas = canvas
        canvas.create_image(150, 300, image=b_g)
        #координаты и данные блоков
        self.dirt = [[0, 235], [30, 235], [60, 235], [90, 235], [120, 235], [150, 235], [180, 235], [210, 235], [240, 235], [270, 235],
                     [0, 265], [30, 265], [60, 265], [90, 265], [120, 265], [150, 265], [180, 265], [210, 265], [240, 265], [270, 265]]

        self.ls  =  [[0, 295], [30, 295], [60, 295], [90, 295], [120, 295], [150, 295], [180, 295], [210, 295], [240, 295], [270, 295],
                    [0, 325], [30, 325], [60, 325], [90, 325], [120, 325], [150, 325], [180, 325], [210, 325], [240, 325], [270, 325],
                    [0, 355], [30, 355], [60, 355], [90, 355], [120, 355], [150, 355], [180, 355], [210, 355], [240, 355], [270, 355],
                    [0, 385], [30, 385], [60, 385], [90, 385], [120, 385], [150, 385], [180, 385], [210, 385], [240, 385], [270, 385],
                    [0, 415], [30, 415], [60, 415], [90, 415], [120, 415], [150, 415], [180, 415], [210, 415], [240, 415], [270, 415],
                    [0, 445], [30, 445], [60, 445], [90, 445], [120, 445], [150, 445], [180, 445], [210, 445], [240, 445], [270, 445],
                    [0, 475], [30, 475], [60, 475], [90, 475], [120, 475], [150, 475], [180, 475], [210, 475], [240, 475], [270, 475],
                    [0, 505], [30, 505], [60, 505], [90, 505], [120, 505], [150, 505], [180, 505], [210, 505], [240, 505], [270, 505],
                    [0, 535], [30, 535], [60, 535], [90, 535], [120, 535], [150, 535], [180, 535], [210, 535], [240, 535], [270, 535],
                    [0, 565], [30, 565], [60, 565], [90, 565], [120, 565], [150, 565], [180, 565], [210, 565], [240, 565], [270, 565]]

        self.dirty = []
        self.blocks = []
        self.generated_weight = []
        
    def ore_generate(self):
        for i in range(100):
            weight_generation = choices([0, 1, 2, 3, 4], weights=[55, 25, 20, 10, 2])[0]
            self.ls[i].append(weight_generation)
            self.generated_weight.append(weight_generation)

            if self.ls[i][2] == 0:
                self.blocks.append([canvas.create_image(self.ls[i][0]+15, self.ls[i][1]+15, image=stone), 1000])
            elif self.ls[i][2] == 1:
                self.blocks.append([canvas.create_image(self.ls[i][0]+15, self.ls[i][1]+15, image=coal), 700])
            elif self.ls[i][2] == 2:
                self.blocks.append([canvas.create_image(self.ls[i][0]+15, self.ls[i][1]+15, image=iron), 500])
            elif self.ls[i][2] == 3:
                self.blocks.append([canvas.create_image(self.ls[i][0]+15, self.ls[i][1]+15, image=gold), 100])
            elif self.ls[i][2] == 4:
                self.blocks.append([canvas.create_image(self.ls[i][0]+15, self.ls[i][1]+15, image=diamond), 0])

        for x in range(10):
            self.dirty.append(canvas.create_image(self.dirt[x][0]+15, self.dirt[x][1]+15, image=grass))
        for x in range(10, 20):
            self.dirty.append(canvas.create_image(self.dirt[x][0]+15, self.dirt[x][1]+15, image=dirt))
    
    def recover_blocks(self, block):
        for i in block:
            if i > 112:
                self.dirty.append(canvas.create_image(self.dirt[i-103][0]+15, self.dirt[i-103][1]+15, image=dirt))
            elif 103 <= i <= 112:
                self.dirty.append(canvas.create_image(self.dirt[i-103][0]+15, self.dirt[i-103][1]+15, image=grass))
            else:
                i -= 3
                if self.ls[i][2] == 0:
                    self.blocks.append([canvas.create_image(self.ls[i][0]+15, self.ls[i][1]+15, image=stone), 1000])
                elif self.ls[i][2] == 1:
                    self.blocks.append([canvas.create_image(self.ls[i][0]+15, self.ls[i][1]+15, image=coal), 700])
                elif self.ls[i][2] == 2:
                    self.blocks.append([canvas.create_image(self.ls[i][0]+15, self.ls[i][1]+15, image=iron), 500])
                elif self.ls[i][2] == 3:
                    self.blocks.append([canvas.create_image(self.ls[i][0]+15, self.ls[i][1]+15, image=gold), 100])
                elif self.ls[i][2] == 4:
                    self.blocks.append([canvas.create_image(self.ls[i][0]+15, self.ls[i][1]+15, image=diamond), 0])
        return True

                
                
        



class Graph:
    def __init__(self, weight):
        self.canvas = canvas
        self.generated_weight = weight
        self.weight2 = []

    #создаем граф, получая данные из сгенерированных блоков
    def graph_creation(self):
        for i in range(len(self.generated_weight)):
            if self.generated_weight[i] == 0:
                self.generated_weight[i] = 1000
            elif self.generated_weight[i] == 1:
                self.generated_weight[i] = 700
            elif self.generated_weight[i] == 2:
                self.generated_weight[i] = 500
            elif self.generated_weight[i] == 3:
                self.generated_weight[i] = 100
            elif self.generated_weight[i] == 4:
                self.generated_weight[i] = 0
            
            adjacency = []
        for i in range(1, 101):
            if i < 91 and i > 10:
                if (i-1) % 10 != 0 and i % 10 != 0:
                    adjacency.append([i-1, i+1, i+10])
                elif i % 10 == 0:
                    adjacency.append([i-1, i+10])
                elif (i-1) % 10 == 0:
                    adjacency.append([i+1, i+10])
            elif i == 10:
                adjacency.append([9, 20])
            elif i < 10 and i>1:
                adjacency.append([i-1, i+1, i+10])
            elif i == 1:
                adjacency.append([2, 11])
            elif i == 91:
                adjacency.append([81, 92])
            elif i > 91 and i < 100:
                adjacency.append([i-1, i+1])
            elif i == 100:
                adjacency.append([90, 99])
        wt = []

        for i in range(1, 101):
            for x in range(1, 101):
                if i != x:
                    wt.append([i, x])

        weight = {}
        weight2 = []
        for i in wt:
            weight[tuple(i)] = -1
        for i in range(len(adjacency)):
            for x in range(len(adjacency[i])):
                try:
                    weight[i+1, adjacency[i][x]] = self.generated_weight[adjacency[i][x]-1]
                    lol = []
                    lol.append(adjacency[i][x])
                    lol.append(i+1)
                    lol.append(weight[i+1, adjacency[i][x]])
                    weight2.append(lol[::-1])
                except:
                    pass
        return weight2


class Node:
     def __init__(self, name):
        self.name = name
        self.visited = False
        self.adjacenciesList = []
        self.predecessor = None
        self.mindistance = sys.maxsize
           

     def __lt__(self, other):
        return self.mindistance < other.mindistance



class Edge:
    def __init__(self, weight, startvertex, endvertex):
        self.weight = weight
        self.startvertex = startvertex
        self.endvertex = endvertex

def calculateshortestpath(vertexlist, startvertex):
    q = []
    startvertex.mindistance = 0
    heapq.heappush(q, startvertex)

    while q:
        actualnode = heapq.heappop(q)
        for edge in actualnode.adjacenciesList:
            tempdist = edge.startvertex.mindistance + edge.weight
            if tempdist < edge.endvertex.mindistance:
                edge.endvertex.mindistance = tempdist
                edge.endvertex.predecessor = edge.startvertex
                heapq.heappush(q,edge.endvertex)
def getshortestpath(targetvertex, way):
    node = targetvertex
    while node:
        way.append(node.name)
        node = node.predecessor
    way.append(targetvertex.mindistance)


    





    




cave = Cave(canvas)
cave.ore_generate()

miner = Miner(canvas)
score = miner.score



while not miner.finished:
    if miner.started == True:
        miner.draw()
        
    tk.update_idletasks()
    tk.update()

miner.end_game()

tk.update()
tk.update_idletasks()

time.sleep(2)

#ии
graph = Graph(cave.generated_weight)
weight = graph.graph_creation()
ai_call = miner.AI(weight)
ai_call.__next__()

while not miner.finished_ai:
    miner.draw()
    
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)

time.sleep(6)
    