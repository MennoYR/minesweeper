# core modules
import sys
import math
import pkg_resources
import random
import logging

# 3rd party modules
from gym import spaces
from gym.spaces import Discrete
from gym.spaces.tuple_space import Tuple
import gym
import numpy as np

from .minesweeper import Game, Move, MoveResult


GRID_SIZE = 8
MINE_COUNT = 10


class MinesweeperEnv(gym.Env):
    def __init__(self):
        self.game = Game(grid_size=GRID_SIZE, mine_count=MINE_COUNT)
        # self.action_space = Tuple((Discrete(GRID_SIZE), Discrete(GRID_SIZE)))
        self.observation_space = spaces.Box(low=-1, high=8, shape=(GRID_SIZE, GRID_SIZE), dtype=np.int8)

    def step(self, action):
        episode_done = False

        x = math.floor(action / GRID_SIZE)
        y = action % GRID_SIZE

        move = Move(action='flag', x=x, y=y)
        result = self.game.run_move(move)
        if result == MoveResult.GAME_WIN or result == MoveResult.GAME_LOSS or result == MoveResult.INVALID_MOVE:
            episode_done = True

        reward = float(result)

        return self._observation_space(), reward, episode_done, {}

    def reset(self):
        self.game = Game(grid_size=GRID_SIZE, mine_count=MINE_COUNT)
        return self._observation_space()

    def render(self, mode='human'):
        if (mode == 'human'):
            self.game.grid.show_grid()

    def seed(self, seed):
        random.seed(seed)
        np.random.seed

    def _observation_space(self):
        matrix = self.game.grid.matrix
        values = [[c.numerical_value() for c in row] for row in matrix]
        space = np.array(values, dtype=np.int8)
        return space
