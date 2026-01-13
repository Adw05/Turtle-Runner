from turtle import Turtle
import random
import random
class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.color("red")
        self.shapesize(stretch_len=0.5,stretch_wid=0.5)
        self.speed("fastest")
        self.escape_count=0
    def refresh(self):
        random_cordx=random.randint(-210,210)
        random_cordy=random.randint(-210,210)
        self.goto(random_cordx,random_cordy)

    '''def move_food(self):
        random.choice([
            self.forward,
            self.left,
            self.right
        ])(10)
'''
    def add_escape(self):
        self.escape_count+=1
    def move_forward(self):
        self.forward(10)

    def move_left(self):
        self.left(90)
    def move_right(self):
        self.right(90)



    