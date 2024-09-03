import gym
import numpy as np

class MountainCar:
    def __init__(self):
        self.env = gym.make("MountainCar-v0")
        self.current_state = self.env.reset() # [position, velocity]

    def step(self, action_idx):
        pass

    def reset(self):
        self.current_state = self.env.reset()
