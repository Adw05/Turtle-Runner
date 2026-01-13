from turtle import Turtle, Screen
from components.food import Food
import time


screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.tracer(0)
food=Food()
screen.listen()

screen.onkey(food.p_right,"Right")
screen.onkey(food.p_left,"Left")
while True:
    screen.update()
    time.sleep(0.1)
    food.forward(10)
