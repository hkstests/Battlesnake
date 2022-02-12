import string
from turtle import right
from classes import Snake
from classes.GameData import GameData
from logic.enums.move import Move
import random


def handle_move(gamedata: GameData) -> string:

    my_head = gamedata.get_my_snake().get_head_position()

    left_position = {"x": (my_head["x"] - 1), "y": my_head["y"]}
    right_position = {"x": (my_head["x"] + 1), "y": my_head["y"]}
    up_position = {"x": my_head["x"], "y": (my_head["y"] + 1)}
    down_position = {"x": my_head["x"], "y": (my_head["y"] - 1)}

    possible_moves = []

    if(is_position_free(gamedata, left_position) and is_hazard_free(gamedata, left_position)):
        possible_moves.append(Move.left.value)
    if(is_position_free(gamedata, right_position) and is_hazard_free(gamedata, right_position)):
        possible_moves.append(Move.right.value)
    if(is_position_free(gamedata, up_position) and is_hazard_free(gamedata, up_position)):
        possible_moves.append(Move.up.value)
    if(is_position_free(gamedata, down_position) and is_hazard_free(gamedata, down_position)):
        possible_moves.append(Move.down.value)

    # just return smth when your destiny is to die anyway
    if len(possible_moves) == 0:
        return Move.left.value

    move = random.choice(possible_moves)

    print(f"{gamedata.get_my_snake().get_id()} : {move}")
    return move


def is_hazard_free(gamedata: GameData, new_position: dict) -> bool:
    for position in gamedata.get_hazard_positions():
        if position["x"] == new_position["x"] and position["y"] == new_position["y"]:
            return False

    return True


def is_position_free(gamedata: GameData, new_position: dict) -> bool:
    # board_width = gamedata.get_board_width()
    # board_height = gamedata.get_board_height()

    # # check board collision
    # if new_position["x"] < 0 or new_position["x"] >= board_width:
    #     return False

    # if new_position["y"] < 0 or new_position["y"] >= board_height:
    #     return False

    # check collisions with snakes
    if collides_with_snake(gamedata.get_my_snake(), new_position):
        return False

    for snake in gamedata.get_team_snakes():
        if collides_with_snake(snake, new_position):
            return False

    for snake in gamedata.get_enemy_snakes():
        if collides_with_snake(snake, new_position):
            return False

    return True


def collides_with_snake(snake: Snake, new_position: dict):
    for position in snake.get_body_positions():
        if position["x"] == new_position["x"] and position["y"] == new_position["y"]:
            return True
