import gym
import numpy as np
from pyglet.text import Label

class Text:
    def __init__(self, text, x, y, font_size=12, anchor_x="center", anchor_y="center", color=(0, 0, 0, 255)):
        self.text = text
        self.label = Label(text, font_size=font_size, x=x, y=y, anchor_x=anchor_x, anchor_y=anchor_y, color=color, bold=True)

    def render(self):
        self.label.draw()
        
class MountainCar:
    def __init__(self):
        self.done = False
        self.env = gym.make("MountainCar-v0")
        self.current_state = self.env.reset() # [position, velocity]
        self.action_space_size = self.env.action_space.n

    def step(self, action, render=False):
        self.current_state, reward, self.done, _ = self.env.step(action)
        if render:
            geom = Text(f"Reward: {reward:.2f}", 5, 400, font_size=20, anchor_x="left", anchor_y="top")
            self.env.render()
            self.env.viewer.add_onetime(geom)
        return reward

    def reset(self):
        self.done = False
        self.current_state = self.env.reset()

    def close(self):
        self.env.close()
