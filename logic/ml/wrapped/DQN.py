import os
import numpy as np
import random
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, Conv2D, Flatten
from tensorflow.keras import Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
import tensorflow as tf

from collections import deque
import pickle

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class DQN:
    def __init__(self):
        self.env = None
        self.memory = deque(maxlen=5000)

        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.998
        self.learning_rate = 0.01
        self.tau = .125

        self.model = self.create_model()

        print(self.model.summary())

        self._initpredict(self.model)

    def _initpredict(self, model):
        # do that when you start the program (predict seems to need to do some setup stuff during the first call)
        temp_state = np.zeros([11, 11, 3])
        temp_state_tensor = self._parse_state_to_tensor(temp_state)

        model.predict(x=temp_state_tensor)

    def create_model(self):
        model = Sequential()
        model.add(Conv2D(filters=64, strides=2, kernel_size=(5, 5), activation="relu", input_shape=(11, 11, 3)))
        model.add(Conv2D(filters=64, kernel_size=(3, 3), activation="relu", input_shape=(11, 11, 3)))
        model.add(Flatten())
        model.add(Dense(3, activation="relu"))
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def act(self, state):

        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return random.randint(0, 2)

        state_tensor = self._parse_state_to_tensor(state)

        res = self.model.predict(x=state_tensor)[0]  # get field 0 due to the output format [[ ... ]]
        return np.argmax(res)

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def _parse_state_to_tensor(self, state):
        # adapt shape so it fits to the model
        state = self._extend_state(state)
        # parse state to tensor for better performance
        state = tf.constant(state)
        return state

    def _extend_state(self, state):
        state = np.expand_dims(state, axis=0)
        state = np.expand_dims(state, axis=-1)
        return state

    def _extend_state_right(self, state):
        state = np.expand_dims(state, axis=-1)
        return state

    def _extend_state_left(self, state):
        state = np.expand_dims(state, axis=0)
        return state

    def train_short_memory(self, state, action, reward, new_state, done):
        state_tensor = self._parse_state_to_tensor(state)
        new_state_tensor = self._parse_state_to_tensor(new_state)

        target = self.model.predict(state_tensor)
        if done:
            target[0][action] = reward
        else:
            Q_future = max(self.model.predict(new_state_tensor)[0])
            target[0][action] = reward + Q_future * self.gamma

        self.model.fit(self._extend_state(state), target, epochs=1, verbose=0)

    def train_long_memory(self):
        batch_size = 500
        samples = []
        if len(self.memory) < batch_size:
            samples = self.memory
        else:
            samples = random.sample(self.memory, batch_size)

        states, actions, rewards, new_states, dones = zip(*samples)
        states = np.asarray(states)
        actions = np.asarray(actions)
        rewards = np.asarray(rewards)
        new_states = np.asarray(new_states)
        dones = np.asarray(dones)

        states = np.array([self._extend_state_right(xi) for xi in states])
        new_states = np.array([self._extend_state_right(xi) for xi in new_states])

        targets = []
        for idx in range(len(states)):
            state = self._extend_state_left(states[idx])
            target = self.model.predict(state)
            targets.append(target)

        targets = np.array(targets)

        for idx in range(len(dones)):
            targets[idx][0][actions[idx]] = rewards[idx]
            if not dones[idx]:
                new_state = self._extend_state_left(new_states[idx])
                Q_future = max(self.model.predict(new_state)[0])
                targets[idx][0][actions[idx]] = rewards[idx] + Q_future * self.gamma

        self.model.fit(states, targets, epochs=1, verbose=0, batch_size=50)

    def save_model(self, fn):
        self.model.save(fn)

    def load_model(self, fn):
        self.model = keras.models.load_model(fn)
        self._initpredict(self.model)

    def save_values(self, fn):
        input_dictionary = {"epsilon": self.epsilon, "memory": self.memory}
        print(f"loaded epsilon {self.epsilon}")
        print(f"memory length {len(self.memory)}")
        with open(fn, 'wb') as handle:
            pickle.dump(input_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_values(self, fn):
        with open(fn, 'rb') as f:
            dict = pickle.load(f)
            self.epsilon = dict["epsilon"]
            self.memory = dict["memory"]
            print(f"loaded epsilon {self.epsilon}")
            print(f"memory length {len(self.memory)}")
