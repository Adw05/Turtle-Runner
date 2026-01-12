from enviroment import SnakeEnv
from scoreboard import Scoreboard


board=Scoreboard()
board.add_score()
print(board.score)
env=SnakeEnv()

state=env.get_state()
print(len(state))
