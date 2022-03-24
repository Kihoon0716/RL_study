# DQN main
# coded by St.Watermelon

from dqn_learn import DQNagent
import gym


def main():

    max_episode_num = 10000
    env_name = "CartPole-v1"
    env = gym.make(env_name)
    env.max_episode_steps = 2000
    agent = DQNagent(env)
    agent.load_weights("./save_weights/")

    agent.train(max_episode_num)

    agent.plot_result()


if __name__ == "__main__":
    main()
