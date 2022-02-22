import os
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
from tensorflow.keras import backend as K

from collections import deque
import pickle

from dotenv import load_dotenv
load_dotenv()

is_local = os.getenv('IS_LOCAL') == "True"

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class DQN:
    def __init__(self):
        self.env = None
        self.memory = deque(maxlen=1000)

        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9985
        self.learning_rate = 0.005
        self.tau = .125

        self.model = self.create_model()
        self.target_model = self.create_model()

        self._initpredict(self.model)
        self._initpredict(self.target_model)

    def _initpredict(self, model):
        global is_local

        temp_state = np.zeros([11, 11])
        temp_state_tensor = self._parse_state_to_tensor(temp_state)

        if is_local:
            model.predict(x=temp_state_tensor)
        else:
            model.predict_on_batch(x=temp_state_tensor)

    def create_model(self):
        model = Sequential()
        model.add(Conv2D(filters=2, kernel_size=(3, 3), activation="relu", input_shape=(11, 11, 1), padding="same"))
        model.add(Conv2D(filters=2, kernel_size=(3, 3), activation="relu", input_shape=(11, 11, 1), padding="same"))
        model.add(Conv2D(filters=2, kernel_size=(3, 3), activation="relu", input_shape=(11, 11, 1), padding="same"))
        model.add(Conv2D(filters=2, kernel_size=(3, 3), activation="relu", input_shape=(11, 11, 1), padding="same"))
        model.add(Conv2D(filters=2, kernel_size=(3, 3), activation="relu", input_shape=(11, 11, 1), padding="same"))
        model.add(Conv2D(filters=2, kernel_size=(3, 3), activation="relu", input_shape=(11, 11, 1), padding="same"))
        model.add(Conv2D(filters=1, kernel_size=(3, 3), activation="relu", input_shape=(11, 11, 1), padding="same"))
        model.add(Flatten())
        model.add(Dense(9, activation="relu"))
        model.add(Dense(3, activation="relu"))
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def act(self, state):
        global is_local
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return random.randint(0, 2)

        state_tensor = self._parse_state_to_tensor(state)

        if is_local:
            res = self.model.predict(x=state_tensor)[0]  # get field 0 due to the output format [[ ... ]]
        else:
            res = self.model.predict_on_batch(x=state_tensor)[0]  # get field 0 due to the output format [[ ... ]]
        return np.argmax(res)

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def _parse_state_to_tensor(self, state):
        # adapt shape so it fits to the model
        state = self._extend_state(state)
        # parse state to tensor for better performance
        state = K.constant(state)
        return state

    def _extend_state(self, state):
        state = np.expand_dims(state, axis=0)
        state = np.expand_dims(state, axis=-1)
        return state

    def replay(self):
        batch_size = 120
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample

            state_tensor = self._parse_state_to_tensor(state)
            target = self.target_model.predict(state_tensor)

            if done:
                target[0][action] = reward
            else:
                new_state_tensor = self._parse_state_to_tensor(new_state)
                Q_future = max(self.target_model.predict(new_state_tensor)[0])
                target[0][action] = reward + Q_future * self.gamma
            # parse target to tensor
            # target = K.constant(target)
            self.model.fit(self._extend_state(state), target, epochs=1, verbose=0)

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
        self._initpredict(self.model)

    def load_target_model(self, fn):
        self.target_model = keras.models.load_model(fn)
        self._initpredict(self.target_model)

    def save_values(self, fn):
        input_dictionary = {"epsilon": self.epsilon}
        with open(fn, 'wb') as handle:
            pickle.dump(input_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_values(self, fn):
        with open(fn, 'rb') as f:
            dict = pickle.load(f)
            self.epsilon = dict["epsilon"]
            print(f"loaded epsilon {self.epsilon}")
