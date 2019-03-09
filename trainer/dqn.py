import os
import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from .minesweeper_env import MinesweeperEnv, GRID_SIZE

IS_LOCAL = os.getenv("LOCALTRAIN")
print("local train: {}".format(IS_LOCAL))

# Get the environment and extract the number of actions.
env = MinesweeperEnv()
np.random.seed(123)
env.seed(123)
nb_actions = GRID_SIZE * GRID_SIZE

# Next, we build a very simple model.
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=1000,
               target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
if IS_LOCAL:
    dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)
else:
    dqn.fit(env, nb_steps=1000000, visualize=False, verbose=0)

# After training is done, we save the final weights.
dqn.save_weights('dqn_weights_{}.h5f'.format(GRID_SIZE), overwrite=True)

# Finally, evaluate our algorithm for x episodes.
dqn.test(env, nb_episodes=10, visualize=True, verbose=2)
