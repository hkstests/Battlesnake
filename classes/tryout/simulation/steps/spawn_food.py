

from random import randint
from typing import List
import numpy as np
from classes.tryout.Position import Position
from classes.tryout.Gamedata import Gamedata


def spawn_food(gamedata: Gamedata):
    free_positions = _get_free_positions(gamedata)

    # if there is no food on the map, randomly set one
    if len(gamedata.food) == 0:
        random_index = randint(0, len(free_positions) - 1)
        gamedata.food.append(free_positions[random_index])

    if randint(0, 100) <= gamedata.food_spawn_chance:
        random_index = randint(0, len(free_positions) - 1)
        gamedata.food.append(free_positions[random_index])


def _get_free_positions(gamedata: Gamedata):
    occupancies = np.zeros([gamedata.board_width, gamedata.board_height])

    for snake in gamedata.snakes:
        for position in snake.body:
            occupancies[position.x, position.y] = 1

    free_positions: List[Position] = []

    for i in range(0, gamedata.board_width):
        for j in range(0, gamedata.board_height):
            if occupancies[i, j] == 0:
                free_positions.append(Position(i, j))

    return free_positions
