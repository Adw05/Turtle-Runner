import time
from agent import Agent
from enviroment import SnakeEnv


def play():
    env = SnakeEnv()

    agent = Agent(state_size=14, action_size=3)

    # Load the model
    agent.load('./final_model.pth')

    # Disable randomness
    agent.epsilon = 0

    print("Game Started!")

    while True:
        state = env.get_state()
        action = agent.choose_action(state)
        _, _, done, _ = env.step(action)

        time.sleep(0.1)

        if done:
            head = env.snake.head
            score = env.scoreboard.score

            # --- DIAGNOSE DEATH ---
            # [cite_start]We check the exact same boundaries as enviroment.py [cite: 28]
            if (head.xcor() > 280 or head.xcor() < -280 or
                    head.ycor() > 280 or head.ycor() < -280):
                print(f"Game Over: Wall hit")
            else:
                print(f"Game Over: Tail bitten")

            print(f"Final Score: {score}")


            break


    print("Click the game window to close it...")
    env.screen.exitonclick()


if __name__ == '__main__':
    play()