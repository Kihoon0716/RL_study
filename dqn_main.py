# DQN main
# coded by St.Watermelon

from dqn_learn import DQNagent
import gym

# from backend import Tetris
from snake_game.envs.snake_env import SnakeEnv
from snake_game.envs.bug_env import BugEnv


def main():

    max_episode_num = 10000
    # env = Tetris()
    # env = gym.make("CartPole-v1")
    # env.max_episode_steps = 2000
    env = BugEnv()
    # env = SnakeEnv()
    agent = DQNagent(env)
    agent.load_weights("./save_weights/")

    agent.train(max_episode_num)

    agent.plot_result()


if __name__ == "__main__":
    main()
