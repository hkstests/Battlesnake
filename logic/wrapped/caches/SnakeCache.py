import string
from classes.GameData import GameData
import numpy as np


class SnakeCache:
    def __init__(self, id: string):
        self._id = id
        self._action = 0
        self._gamestate = []
        self._gamedata: GameData = None

    def get_id(self):
        return self._id

    def get_action(self):
        return self._action

    def get_health(self):
        return self._gamedata.get_my_snake().get_health()

    def get_gamestate(self):
        return self._gamestate

    def get_gamedata(self):
        return self._gamedata

    def get_turn(self):
        return self._gamedata.get_turn()

    def set_action(self, action: float):
        self._action = action

    def set_gamestate(self, gamestate: np.ndarray):
        self._gamestate = gamestate

    def set_gamedata(self, gamedata: GameData):
        self._gamedata = gamedata
