# DQN learn (tf2 subclassing API version)
# coded by St.Watermelon

import random
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from tensorflow.keras.optimizers import Adam
import tensorflow as tf

from replay_buffer import ReplayBuffer

# from backend import Tetris
# from front import Front
from colorama import Fore

# Q network
class DQN(Model):
    def __init__(self, action_n):
        super(DQN, self).__init__()
        self.conv1 = Conv2D(32, (3, 3), padding="same", activation="relu")
        self.pooling1 = MaxPooling2D((2, 2))
        self.conv2 = Conv2D(64, (3, 3), padding="same", activation="relu")
        self.pooling2 = MaxPooling2D((2, 2))
        self.conv3 = Conv2D(64, (3, 3), padding="same", activation="relu")
        self.pooling3 = MaxPooling2D()
        self.flatten = Flatten()
        self.h1 = Dense(512, activation="relu")
        self.h2 = Dense(256, activation="relu")
        self.h3 = Dense(128, activation="relu")
        self.h4 = Dense(64, activation="relu")
        self.h5 = Dense(32, activation="relu")
        self.h6 = Dense(16, activation="relu")
        self.q = Dense(action_n, activation="linear")

    def call(self, x):
        # x = self.conv1(x)
        # x = self.pooling1(x)
        # x = self.conv2(x)
        # x = self.pooling2(x)
        # x = self.conv3(x)
        # x = self.pooling3(x)
        x = self.flatten(x)
        x = self.h1(x)
        x = self.h2(x)
        x = self.h3(x)
        x = self.h4(x)
        x = self.h5(x)
        x = self.h6(x)
        a = self.q(x)
        return a


class DQNagent(object):
    def __init__(self, env):

        ## hyperparameters
        self.GAMMA = 0.95
        self.BATCH_SIZE = 32
        self.BUFFER_SIZE = 20000
        self.DQN_LEARNING_RATE = 0.001
        # self.DQN_LEARNING_RATE = 0.001
        self.TAU = 0.001
        self.EPSILON = 0.2
        self.EPSILON_DECAY = 0.995
        self.EPSILON_MIN = 0.05

        self.env = env
        # self.front = Front()

        # get state dimension and action number
        self.state_dim = self.env.reset().shape
        self.action_n = self.env.action_space.n

        ## create Q networks
        self.dqn = DQN(self.action_n)
        self.target_dqn = DQN(self.action_n)

        self.dqn.build(input_shape=(None, *self.state_dim))
        self.target_dqn.build(input_shape=(None, *self.state_dim))

        self.dqn.summary()

        # optimizer
        self.dqn_opt = Adam(self.DQN_LEARNING_RATE)

        ## initialize replay buffer
        self.buffer = ReplayBuffer(self.BUFFER_SIZE)

        # save the results
        self.save_epi_reward = []

    ## get action
    def choose_action(self, state):
        if np.random.random() <= self.EPSILON:
            return random.randint(0, self.action_n - 1)
        else:
            qs = self.dqn(tf.convert_to_tensor([state], dtype=tf.float32))
            return np.argmax(qs.numpy())

    ## transfer actor weights to target actor with a tau
    def update_target_network(self, TAU):
        phi = self.dqn.get_weights()
        target_phi = self.target_dqn.get_weights()
        for i in range(len(phi)):
            target_phi[i] = TAU * phi[i] + (1 - TAU) * target_phi[i]
        self.target_dqn.set_weights(target_phi)

    ## single gradient update on a single batch data
    def dqn_learn(self, states, actions, td_targets):
        with tf.GradientTape() as tape:
            one_hot_actions = tf.one_hot(actions, self.action_n)
            q = self.dqn(states, training=True)
            q_values = tf.reduce_sum(one_hot_actions * q, axis=1, keepdims=True)
            loss = tf.reduce_mean(tf.square(q_values - td_targets))

        grads = tape.gradient(loss, self.dqn.trainable_variables)
        self.dqn_opt.apply_gradients(zip(grads, self.dqn.trainable_variables))

    ## computing TD target: y_k = r_k + gamma* max Q(s_k+1, a)
    def td_target(self, rewards, target_qs, dones):
        max_q = np.max(target_qs, axis=1, keepdims=True)
        y_k = np.zeros(max_q.shape)
        for i in range(max_q.shape[0]):  # number of batch
            if dones[i]:
                y_k[i] = rewards[i]
            else:
                y_k[i] = rewards[i] + self.GAMMA * max_q[i]
        return y_k

    ## load actor weights
    def load_weights(self, path):
        self.dqn.load_weights(path + "cartpole_dqn.h5")

    ## train the agent
    def train(self, max_episode_num):

        # initial transfer model weights to target model network
        self.update_target_network(1.0)

        for ep in range(int(max_episode_num)):

            # reset episode
            time, episode_reward, done = 0, 0, False
            # reset the environment and observe the first state
            state = self.env.reset()
            # state = state.reshape(25, 10, 1)
            # decaying EPSILON
            if self.EPSILON > self.EPSILON_MIN:
                self.EPSILON *= self.EPSILON_DECAY

            while not done and time < 1000:
                # visualize the environment
                # self.env.render()
                # pick an action
                action = self.choose_action(state)
                # observe reward, new_state
                next_state, reward, done, _ = self.env.step(action)
                # self.front.show(next_state)
                # next_state = next_state.reshape(25, 10, 1)

                train_reward = reward + time * 0.01

                # add transition to replay buffer
                self.buffer.add_buffer(state, action, train_reward, next_state, done)

                if (
                    self.buffer.buffer_count() > 1000
                ):  # start train after buffer has some amounts

                    # sample transitions from replay buffer
                    (
                        states,
                        actions,
                        rewards,
                        next_states,
                        dones,
                    ) = self.buffer.sample_batch(self.BATCH_SIZE)

                    # predict target Q-values
                    target_qs = self.target_dqn(
                        tf.convert_to_tensor(next_states, dtype=tf.float32)
                    )

                    # compute TD targets
                    y_i = self.td_target(rewards, target_qs.numpy(), dones)

                    # train critic using sampled batch
                    self.dqn_learn(
                        tf.convert_to_tensor(states, dtype=tf.float32),
                        actions,
                        tf.convert_to_tensor(y_i, dtype=tf.float32),
                    )

                    # update target network
                    self.update_target_network(self.TAU)

                # update current state
                state = next_state
                episode_reward += reward
                time += 1

            ## display rewards every episode
            print(
                Fore.WHITE + "Episode: ",
                ep + 1,
                "Time: ",
                time,
                "Reward: ",
                episode_reward,
                "self.EPSILON",
                self.EPSILON,
            )
            # if (
            #     self.buffer.buffer_count() > 1000
            # ):  # start train after buffer has some amounts
            #     for i in range(30):
            #         # sample transitions from replay buffer
            #         (
            #             states,
            #             actions,
            #             rewards,
            #             next_states,
            #             dones,
            #         ) = self.buffer.sample_batch(self.BATCH_SIZE)

            #         # predict target Q-values
            #         target_qs = self.target_dqn(
            #             tf.convert_to_tensor(next_states, dtype=tf.float32)
            #         )
            #         # # predict target Q-values
            #         # target_qs = self.target_dqn(
            #         #     tf.convert_to_tensor(next_states, dtype=tf.float32)
            #         # )

            #         # compute TD targets
            #         y_i = self.td_target(rewards, target_qs.numpy(), dones)

            #         # train critic using sampled batch
            #         self.dqn_learn(
            #             tf.convert_to_tensor(states, dtype=tf.float32),
            #             actions,
            #             tf.convert_to_tensor(y_i, dtype=tf.float32),
            #         )

            #         # update target network
            #         self.update_target_network(self.TAU)

            self.save_epi_reward.append(episode_reward)

            ## save weights every episode
            self.dqn.save_weights("./save_weights/cartpole_dqn.h5")

        np.savetxt("./save_weights/cartpole_epi_reward.txt", self.save_epi_reward)

    ## save them to file if done
    def plot_result(self):
        plt.plot(self.save_epi_reward)
        plt.show()
