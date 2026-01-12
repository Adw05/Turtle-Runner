from turtle import Turtle, Screen
from components.food import Food
import time


screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.listen()
food=Food()
screen.onkey(food.up(),"Up")
screen.onkey(food.down(),"Down")
screen.onkey(food.p_right(),"Right")
screen.onkey(food.p_left(),"Left")


screen.exitonclick()