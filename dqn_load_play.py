# DQN load and play
# coded by St.Watermelon

import gym
import numpy as np
import tensorflow as tf
from dqn_learn import DQNagent
from snake_game.envs.snake_env import SnakeEnv
from snake_game.envs.bug_env import BugEnv


def main():
    # env = SnakeEnv()
    env = BugEnv()
    # env = gym.make("CartPole-v1")

    agent = DQNagent(env)

    agent.load_weights("./save_weights/")
    for i in range(100):
        time = 0
        state = env.reset()

        while True:
            qs = agent.dqn(tf.convert_to_tensor([state], dtype=tf.float32))
            action = np.argmax(qs.numpy())
            state, reward, done, _ = env.step(action)
            env.render()

            time += 1

            print("Time: ", time, "Reward: ", reward, "action: ", action)
            if done:
                break

    env.close()


if __name__ == "__main__":
    main()
