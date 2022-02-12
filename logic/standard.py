import string
from typing import List
from classes import Snake
from classes.GameData import GameData
from logic.enums.move import Move


def handle_move(gamedata: GameData) -> string:

    my_head = gamedata.get_my_snake().get_head_position()
    board_width = gamedata.get_board_width()
    board_height = gamedata.get_board_height()

    final_move = ""

    left = {
        "position": {"x": (my_head["x"] - 1) % board_width, "y": my_head["y"]},
        "move": Move.left.value
    }
    right = {
        "position": {"x": (my_head["x"] + 1) % board_width, "y": my_head["y"]},
        "move": Move.right.value
    }
    up = {
        "position": {"x": my_head["x"], "y": (my_head["y"] + 1) % board_height},
        "move": Move.up.value
    }
    down = {
        "position": {"x": my_head["x"], "y": (my_head["y"] - 1) % board_height},
        "move": Move.down.value
    }

    possible_moves = [left, right, up, down]

    collision_free_moves = []

    for move in possible_moves:
        if is_collision_free(gamedata, move["position"]):
            collision_free_moves.append(move)

    # just go left if you'd die anyway due to collision
    if len(collision_free_moves) == 0:
        final_move = Move.left.value
        print(f"{gamedata.get_my_snake().get_id()} : {final_move}")
        return final_move

    hazard_free_moves = []

    for move in hazard_free_moves:
        if is_hazard_free(gamedata, move["position"]):
            hazard_free_moves.append(move)

    # just enter the hazard if there is no other chance to prevent it
    if len(hazard_free_moves) == 0:
        final_move = get_closest_move_to_food(gamedata, collision_free_moves)["move"]
    else:
        final_move = get_closest_move_to_food(gamedata, hazard_free_moves)["move"]

    print(f"{gamedata.get_my_snake().get_id()} : {final_move}")
    return final_move


def get_closest_move_to_food(gamedata: GameData, moves: List[dict]) -> dict:
    food_positions = gamedata.get_food_positions()

    closest_move_to_food = moves[0]
    closest_distance = compute_distance(gamedata, moves[0]["position"], food_positions[0])

    for move in moves:
        for food_position in food_positions:
            distance = compute_distance(gamedata, move["position"], food_position)
            if distance < closest_distance:
                closest_move_to_food = move
                closest_distance = distance

    return closest_move_to_food


def compute_distance(gamedata: GameData, position0: dict, position1: dict) -> int:
    board_width = gamedata.get_board_width()
    board_height = gamedata.get_board_height()

    horizontal_distance = min(abs(position0["x"] - position1["x"]), board_width - 1 - position0["x"] + position1["x"] + 1)
    vertical_distance = min(abs(position0["y"] - position1["y"]), board_height - 1 - position0["y"] + position1["y"] + 1)

    return horizontal_distance + vertical_distance


def is_hazard_free(gamedata: GameData, new_position: dict) -> bool:
    for position in gamedata.get_hazard_positions():
        if position["x"] == new_position["x"] and position["y"] == new_position["y"]:
            return False

    return True


def is_collision_free(gamedata: GameData, new_position: dict) -> bool:

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
