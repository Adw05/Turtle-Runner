from agent import Agent
from enviroment import SnakeEnv
from helper import plot


def train():
    env = SnakeEnv()
    agent = Agent(state_size=14, action_size=3)

    scores = []
    plot_mean_scores = []
    total_games = 0

    while True:
        # 1. Get Old State
        state_old = env.get_state()

        # 2. Get Move
        action = agent.choose_action(state_old)

        # 3. Perform Move
        state_new, reward, done, _ = env.step(action)

        # 4. Train Short Term (for this one step)
        agent.remember(state_old, action, reward, state_new, done)
        agent.learn(batch_size=64)

        if done:
            # --- CORRECT WAY TO GET SCORE ---
            # Retrieve the score from the environment's internal scoreboard
            game_score = env.scoreboard.score

            env.reset()
            total_games += 1

            scores.append(game_score)
            mean_score = sum(scores) / len(scores)
            plot_mean_scores.append(mean_score)
            target_score=1.1
            if mean_score>=target_score:
                agent.save(file_name='final_model.pth')
                print(f"Target reached! Final mean score:{mean_score}")
                break

            # Decay Epsilon (Curiosity) only after a game ends
            if agent.epsilon > agent.epsilon_min:
                agent.epsilon *= agent.epsilon_decay

            # Update the graph
            plot(scores, plot_mean_scores)

            print(f'Game {total_games} Score: {game_score} Mean: {mean_score:.2f} Epsilon: {agent.epsilon:.2f}')


if __name__ == '__main__':
    train()