
import numpy as np
from classes import Snake
from classes.GameData import GameData

# values for specific properties inside the gamestate
snake_head = 5
snake_body = 1

hazard = 0.4
food = 1


def assemble_gamestate(gamedata: GameData):
    board_width = gamedata.get_board_width()
    board_height = gamedata.get_board_height()

    # init board
    # gamestate = np.zeros([board_width, board_height])
    food_state = np.zeros([board_width, board_height])
    my_snake_state = np.zeros([board_width, board_height])
    enemy_snakes_state = np.zeros([board_width, board_height])

    # set values of enemy snakes
    enemy_snakes = gamedata.get_enemy_snakes()
    for enemy_snake in enemy_snakes:
        _set_snake_values(enemy_snakes_state, enemy_snake, snake_head, snake_body)

    # set values of my snake
    my_snake = gamedata.get_my_snake()
    _set_snake_values(my_snake_state, my_snake, snake_head, snake_body)

    # hazard_positions = gamedata.get_hazard_positions()
    # _set_values(gamestate, hazard_positions, hazard)

    food_positions = gamedata.get_food_positions()
    _set_values(food_state, food_positions, food)

    gamestate = np.array([food_state, my_snake_state, enemy_snakes_state])
    gamestate = np.reshape(gamestate, (11, 11, 3))

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
