import random
from tkinter import *
import time
 
LEFT = 0
 
RIGHT = 20
 
UPPER = 0
 
LOWER = 30
 

class Map:
 
    def __init__(self,root):
        self.canvas = Canvas(root, height = 600, width = 600, bg='black')
        self.canvas.pack()
 
    def paint(self,x,y,text,font = None):
        if font == None:
            self.canvas.create_text(y * 20, x * 20, text = text, fill = 'white')
        else:
            self.canvas.create_text(y * 20, x * 20, text=text, fill='white',font=font)
 
    def create(self,snake,food,score):
        for i in range(21):
            self.paint(0,i,text = '█')
 
        for i in range(1,30):
            self.paint(i,0, text='█')
            self.paint(i,20,text='█')
 
        for i in range(21):
            self.paint(30,i,text='█')
 
        self.paint(*food, text = '█')
 
        for item in snake:
            self.paint(*item,text='█')
 
        self.paint(15, 23, text='Score', font=('Couried', 14))
        self.paint(15, 25, text=':',font=('Couried', 14))
        self.paint(15, 27, text=f'{score}', font=('Couried', 14))
 
    def clear(self):
        self.canvas.delete(ALL)
 
 
class Snake:
 
    def __init__(self,root):
        self.body = [(1,1),(1,2),(1,3),(1,4)]
        self.vx = 0
        self.vy = 1
        root.bind('<Up>',self.up)
        root.bind('<Down>',self.down)
        root.bind('<Left>',self.left)
        root.bind('<Right>',self.right)
        root.focus_set()
 
    def __contains__(self, item):
        return item in self.body
 
    def __iter__(self):
        return iter(self.body)
 
    def __getitem__(self, item):
        return self.body[item]
 
    def move(self):
        self.body.pop(0)
        new_x = self.body[-1][0] + self.vx
        new_y = self.body[-1][1] + self.vy
        self.body.append((new_x, new_y))
 
    def up(self,event):
        self.vx = -1
        self.vy = 0
 
    def down(self,event):
        self.vx = 1
        self.vy = 0
 
    def right(self,event):
        self.vx = 0
        self.vy = 1
 
    def left(self,event):
        self.vx = 0
        self.vy = -1
 
    def eat(self,event):
        new_x = self.body[-1][0] + self.vx
        new_y = self.body[-1][1] + self.vy
        self.body.append((new_x, new_y))
 
 
def alive(snake):
    condition1 = snake[-1][0] > UPPER and snake[-1][0] < LOWER
    condition2 = snake[-1][1] > LEFT and snake[-1][1] < RIGHT
    condition3 = snake[-1] not in snake[:-1]
    return condition1 and condition2 and condition3
 

def game():
    root = Tk()
    map = Map(root)
    snake = Snake(root)
    food = (5, 8)
    score = 0
    map.create(snake, food, score)
    time.sleep(0.2)
    root.update()
 
    while alive(snake):
        map.clear()
        if food in snake:
            snake.eat(food)
            food = (random.randint(1,20), random.randint(1,20))
            score += 100
        else:
            snake.move()
        map.create(snake, food, score)
        time.sleep(0.1)
        root.update()
 
    mainloop()

if __name__ == "__main__":
    
    game()