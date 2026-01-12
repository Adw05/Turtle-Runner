from turtle import Turtle
FONT="Arial"
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score=0
        self.color("white")
        self.penup()
        self.goto(0,280)
        self.hideturtle()
        self.update_scoreboard()
    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score}",align="Center",font=(FONT,12,"normal"))

    def add_score(self):
        self.score+=1
    def game_over(self):
        self.goto(0,0)
        self.write(f"GAME OVER!",align="Center",font=(FONT,40,"normal"))
    def food_escaped_game_over(self):
        self.goto(0, 0)
        self.write(f"Food escaped!", align="Center", font=(FONT, 40, "normal"))
