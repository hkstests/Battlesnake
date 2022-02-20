import numpy as np
import random
# from keras.models import Sequential
# from keras.layers import Dense, Dropout
# from keras.optimizers import Adam

from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, Conv2D, Flatten
from tensorflow.keras import Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential

from collections import deque
import pickle


class DQN:
    def __init__(self):
        self.env = None
        self.memory = deque(maxlen=2000)

        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125

        self.model = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model = Sequential()
        # state_shape = self.env.observation_space.shape
        # model.add(Dense(24, input_dim=state_shape[0], activation="relu"))
        model.add(Conv2D(filters=3, kernel_size=3, activation="relu", input_shape=(11, 11, 1), padding="same"))
        model.add(Conv2D(filters=3, kernel_size=3, activation="relu", padding="same"))
        model.add(Flatten())
        model.add(Dense(24, activation="relu"))
        model.add(Dense(12, activation="relu"))
        model.add(Dense(3, activation="relu"))
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return random.randint(0, 2)
        res = self.model.predict(x=state)[0]  # get field 0 due to the output format [[ ... ]]
        return np.argmax(res)

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 2
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)

    def save_target_model(self, fn):
        self.target_model.save(fn)

    def load_model(self, fn):
        self.model = keras.models.load_model(fn)

    def load_target_model(self, fn):
        self.target_model = keras.models.load_model(fn)

    def save_values(self, fn):
        input_dictionary = {"epsilon": self.epsilon}
        with open(fn, 'wb') as handle:
            pickle.dump(input_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_values(self, fn):
        with open(fn, 'rb') as f:
            dict = pickle.load(f)
            self.epsilon = dict["epsilon"]
            print(f"loaded epsilon {self.epsilon}")
