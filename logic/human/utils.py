from pydoc import visiblename
import numpy as np
from classes.GameData import GameData
from classes.Snake import Snake


def map_direction(snake: Snake, move_direction: string) -> string:
    # get snake direction

    # map left/right/further to left/right/up/down accordingly

    return ""


def get_food_matrix(gamedata: GameData, food_position: dict):
    invalid = 1000
    unvisited = 999

    board_width = gamedata.get_board_width()
    board_height = gamedata.get_board_height()

    board = np.ones([board_width, board_height])
    board *= unvisited

    for position in gamedata.get_my_snake().get_body_positions():
        board[position["x"], position["y"]] = invalid

    for enemy_snake in gamedata.get_enemy_snakes():
        for position in enemy_snake.get_body_positions():
            board[position["x"], position["y"]] = invalid

    board[food_position["x"], food_position["y"]] = 0

    changed = True
    while changed:
        changed = False
        for x in range(0, board_width):
            for y in range(0, board_height):
                val = board[x, y]
                if val == invalid or val != unvisited:
                    continue
                surrounding_positions = [
                    {"x": (x - 1) % board_width, "y": y},
                    {"x": (x + 1) % board_width, "y": y},
                    {"x": x, "y": (y - 1) % board_height},
                    {"x": x, "y": (y + 1) % board_height},
                ]
                min_value = invalid
                for sp in surrounding_positions:
                    sp_val = board[sp["x"], sp["y"]]
                    if sp_val != invalid and sp_val != unvisited and sp_val < min_value:
                        min_value = sp_val

                if min_value != invalid:
                    board[x, y] = min_value + 1
                    changed = True

    return board
