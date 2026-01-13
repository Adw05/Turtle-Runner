from turtle import Screen
from components.snake import Snake
from components.food import Food
from components.scoreboard import Scoreboard
import numpy as np
import time


class SnakeEnv:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=600, height=600)
        self.screen.bgcolor("black")
        self.screen.title("Snake RL")
        self.screen.tracer(0)  # Turn off animation for speed

        self.snake = Snake()
        self.food = Food()
        self.screen.listen()
        self.screen.onkey(self.food.move_left,"Left")
        self.screen.onkey(self.food.move_right, "Right")
        self.scoreboard = Scoreboard()
        self.done = False
        self.start_time=time.time()

    def reset(self):
        self.snake.reset()  # Assuming you added a reset method to snake.py, or recreate it:
        self.screen.clear()
        self.screen.bgcolor("black")
        self.screen.tracer(0)
        self.snake = Snake()
        self.food = Food()
        self.scoreboard = Scoreboard()
        self.food.refresh()
        self.done = False
        self.start_time=time.time()
        return self.get_state()

    def step(self, action):
        # Action List: [Straight, Right Turn, Left Turn]
        # index 0 = Straight, 1 = Right, 2 = Left

        clock_wise = [0, 270, 180, 90]  # Right, Down, Left, Up
        current_heading = self.snake.head.heading()
        idx = clock_wise.index(current_heading)

        # Calculate new direction based on relative action
        if action == 1:  # Right Turn
            new_dir = clock_wise[(idx + 1) % 4]
            self.snake.head.setheading(new_dir)
        elif action == 2:  # Left Turn
            new_dir = clock_wise[(idx - 1) % 4]
            self.snake.head.setheading(new_dir)
        # if action == 0, we do nothing (keep going straight)

        self.snake.move()
        self.food.move_forward() #Not learned during training

        # --- Rewards & Game Over Logic ---
        reward = 0
        game_over = False

        # 1. Collision (Wall or Self)
        if self.is_collision():
            game_over = True
            reward = -10
            return self.get_state(), reward, game_over, {}

        # 2. Food Logic

        if self.snake.head.distance(self.food) < 15:
            self.food.refresh()
            #self.snake.extend()
            #self.scoreboard.score += 1  # Update internal score
            #self.scoreboard.update_scoreboard()
            reward = 10

        if self.scoreboard.score%20==0:
            self.snake.extend()

        # 3. Optional: Time penalty to prevent looping
        reward -= 0.01

        elapsed = time.time() - self.start_time
        self.scoreboard.score = round(elapsed, 1)
        self.scoreboard.update_scoreboard()

        self.screen.update()

        return self.get_state(), reward, game_over, {}

    def is_collision(self, point=None):
        if point is None:
            point = self.snake.head

        # Wall
        if point.xcor() > 280 or point.xcor() < -280 or point.ycor() > 280 or point.ycor() < -280:
            return True

        # Tail (skip head)
        for segment in self.snake.segments[3:]:
            if point.distance(segment) < 20:
                return True
        return False

    def get_state(self):
        head = self.snake.head

        # Points to check around the head
        point_l = (head.xcor() - 20, head.ycor())
        point_r = (head.xcor() + 20, head.ycor())
        point_u = (head.xcor(), head.ycor() + 20)
        point_d = (head.xcor(), head.ycor() - 20)

        dir_l = head.heading() == 180
        dir_r = head.heading() == 0
        dir_u = head.heading() == 90
        dir_d = head.heading() == 270

        # Helper: Checks for ANY collision (Wall OR Tail)
        def check_collision(pt):
            class Pt:
                def xcor(self): return pt[0]

                def ycor(self): return pt[1]

                def distance(self, o):
                    return ((self.xcor() - o.xcor()) ** 2 + (self.ycor() - o.ycor()) ** 2) ** 0.5

            return self.is_collision(Pt())

        # Helper: Checks ONLY for Wall collision
        def check_wall(pt):
            return pt[0] > 280 or pt[0] < -280 or pt[1] > 280 or pt[1] < -280

        state = [
            # 1. Danger Straight (Any Danger)
            (dir_r and check_collision(point_r)) or
            (dir_l and check_collision(point_l)) or
            (dir_u and check_collision(point_u)) or
            (dir_d and check_collision(point_d)),

            # 2. Danger Right (Any Danger)
            (dir_u and check_collision(point_r)) or
            (dir_d and check_collision(point_l)) or
            (dir_l and check_collision(point_u)) or
            (dir_r and check_collision(point_d)),

            # 3. Danger Left (Any Danger)
            (dir_d and check_collision(point_r)) or
            (dir_u and check_collision(point_l)) or
            (dir_r and check_collision(point_u)) or
            (dir_l and check_collision(point_d)),

            # --- NEW: SPECIFIC WALL CHECKS ---
            # 4. Wall Straight
            (dir_r and check_wall(point_r)) or
            (dir_l and check_wall(point_l)) or
            (dir_u and check_wall(point_u)) or
            (dir_d and check_wall(point_d)),

            # 5. Wall Right
            (dir_u and check_wall(point_r)) or
            (dir_d and check_wall(point_l)) or
            (dir_l and check_wall(point_u)) or
            (dir_r and check_wall(point_d)),

            # 6. Wall Left
            (dir_d and check_wall(point_r)) or
            (dir_u and check_wall(point_l)) or
            (dir_r and check_wall(point_u)) or
            (dir_l and check_wall(point_d)),
            # ---------------------------------

            # 7-10. Move Direction
            dir_l, dir_r, dir_u, dir_d,

            # 11-14. Food Location
            self.food.xcor() < head.xcor(),  # Food Left
            self.food.xcor() > head.xcor(),  # Food Right
            self.food.ycor() > head.ycor(),  # Food Up
            self.food.ycor() < head.ycor()  # Food Down
        ]

        return np.array(state, dtype=int)