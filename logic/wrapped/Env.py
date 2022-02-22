
import numpy as np
from classes import Snake
from classes.GameData import GameData

# values for specific properties inside the gamestate
my_snake_head = 0.1
my_snake_body = 0.5

enemy_snake_head = 0.6
enemy_snake_body = 0.7

hazard = 0.4
food = 0.2


def assemble_gamestate(gamedata: GameData):
    board_width = gamedata.get_board_width()
    board_height = gamedata.get_board_height()

    # init board
    gamestate = np.zeros([board_width, board_height])

    # set values of enemy snakes
    enemy_snakes = gamedata.get_enemy_snakes()
    for enemy_snake in enemy_snakes:
        _set_snake_values(gamestate, enemy_snake, enemy_snake_head, enemy_snake_body)

    # set values of my snake
    my_snake = gamedata.get_my_snake()
    _set_snake_values(gamestate, my_snake, my_snake_head, my_snake_body)

    hazard_positions = gamedata.get_hazard_positions()
    _set_values(gamestate, hazard_positions, hazard)

    food_positions = gamedata.get_food_positions()
    _set_values(gamestate, food_positions, food)

    return gamestate


def _set_snake_values(gamestate: np.ndarray, snake: Snake, head_value: float, body_value: float):
    body_positions = snake.get_body_positions()
    for position in body_positions:
        gamestate[position["x"], position["y"]] = body_value

    head_position = snake.get_head_position()
    gamestate[head_position["x"], head_position["y"]] = head_value


def _set_values(gamestate: np.ndarray, positions, value: float):
    for position in positions:
        gamestate[position["x"], position["y"]] = value
