import gym
from minesweeper_env import MinesweeperEnv

env = MinesweeperEnv()
observation = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    if done:
        env.reset()
