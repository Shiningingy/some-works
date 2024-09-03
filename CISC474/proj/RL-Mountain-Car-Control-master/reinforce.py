# REINFORCE or Monte Carlo Policy Gradient
# tensorflow r1.14

import gym
import numpy as np
from datetime import datetime
from tensorflow.keras import backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.utils import to_categorical

class REINFORCE:
    def __init__(self, gamma=0.9):
        self.gamma = gamma
        self.env = gym.make("MountainCar-v0")
        self.current_state = self.env.reset() # [position, velocity]
        self.prods = Input(shape=(1, ))
        self.model = self.init_model()

    def init_model(self):
        state_input = Input(shape=self.current_state.shape)
        hidden = Dense(16, activation="relu")(state_input)
        output = Dense(self.env.action_space.n, activation="softmax")(hidden)
        model = Model(inputs=[state_input, self.prods], outputs=[output])
        model.compile("adam", loss=self.loss(self.prods))
        return model

    def loss(self, prods):
        def loss(y_true, y_pred):
            return K.categorical_crossentropy(y_true, y_pred) * prods
        return loss

    def select_action(self):
        current_state = np.expand_dims(self.current_state, 0)
        prob = self.model.predict([current_state, np.zeros((1))]).squeeze()
        action = np.random.choice(np.arange(0, self.env.action_space.n), p=prob)
        log_prob = np.log(prob[action])
        return action, log_prob

    def discount(self, rewards):
        discounted_rewards, cumulative_reward = np.zeros_like(rewards), 0.
        for t in reversed(range(len(rewards))):
            cumulative_reward = rewards[t] + cumulative_reward * self.gamma
            discounted_rewards[t] = cumulative_reward
        return discounted_rewards

    def run_one_episode(self):
        done = False
        states, actions, rewards, log_probs = [self.current_state], [], [], []
        while not done:
            action, log_prob = self.select_action()
            self.current_state, reward, done, _ = self.env.step(action)
            states.append(self.current_state)
            actions.append(action)
            rewards.append(reward)
            log_probs.append(log_prob)
        states = states[: -1] # remove end state
        self.current_state = self.env.reset()
        return np.asarray(states), np.asarray(actions), np.asarray(rewards), np.asarray(log_probs)

    def train(self, episodes=5000):
        losses = []
        for e in range(episodes):
            states, actions, rewards, log_probs = self.run_one_episode()
            discounted_rewards = self.discount(rewards)
            prods = -discounted_rewards * log_probs
            actions = to_categorical(actions, num_classes=self.env.action_space.n) # `y_true`
            loss = self.model.test_on_batch([states, prods], actions)
            losses.append(loss)
            if e % 500 == 0:
                print(e)
        return losses

    def save_model(self, name):
        current_time = datetime.now()
        self.model.save(f"{name}_{current_time.strftime('%Y_%m_%d_%H_%M_%S')}.h5")

    def test(self):
        done = False
        while not done:
            self.env.render()
            action, _ = self.select_action()
            self.current_state, reward, done, _ = self.env.step(action)
        self.current_state = self.env.reset()

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    re0 = REINFORCE()
    losses = re0.train(10000)
    plt.plot(list(range(len(losses))), losses)
    plt.show()
    re0.test()
