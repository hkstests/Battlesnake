import string
from classes import Snake
from classes.GameData import GameData
from logic.enums.move import Move


def handle_move(gamedata: GameData) -> string:

    my_head = gamedata.get_my_snake().get_head_position()

    left_position = {"x": (my_head["x"] - 1), "y": my_head["y"]}
    right_position = {"x": (my_head["x"] + 1), "y": my_head["y"]}
    up_position = {"x": my_head["x"], "y": (my_head["y"] + 1)}
    down_position = {"x": my_head["x"], "y": (my_head["y"] - 1)}

    move = ""

    if(is_position_free(gamedata, left_position)):
        move = Move.left.value
    elif(is_position_free(gamedata, right_position)):
        move = Move.right.value
    elif(is_position_free(gamedata, up_position)):
        move = Move.up.value
    elif(is_position_free(gamedata, down_position)):
        move = Move.down.value
    else:
        move = Move.up.value

    print(f"{gamedata.get_my_snake().get_id()} : {move}")
    return move


def is_position_free(gamedata: GameData, new_position: dict) -> bool:
    board_width = gamedata.get_board_width()
    board_height = gamedata.get_board_height()

    # check board collision
    if new_position["x"] < 0 or new_position["x"] >= board_width:
        return False

    if new_position["y"] < 0 or new_position["y"] >= board_height:
        return False

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
