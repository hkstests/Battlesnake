import string
from typing import List

import numpy as np
from classes.Snake import Snake
from classes.GameData import GameData
from logic.human.Action import Action
from logic.enums.move import Move


previous_move: Move = Move.left


def handle_move(gamedata: GameData) -> string:
    global previous_move

    # get actions left, right, up, down with their respective position (with respect to the head position)
    possible_actions = get_initial_actions(gamedata)

    # remove actions that would lead to a collision (with itself or other snakes)
    collision_free_actions = get_collision_free_actions(gamedata, possible_actions)

    # just go left if you'd die anyway due to collision
    if len(collision_free_actions) == 0:
        return handle_return_move(Move.left)

    # if only one move is possible, simply do it
    if len(collision_free_actions) == 1:
        return handle_return_move(collision_free_actions[0].get_move())

    # get hazard free actions
    hazard_free_actions = get_hazard_free_actions(gamedata, collision_free_actions)

    # if there is only one way to prevent a hazard, simply go it
    if len(hazard_free_actions) == 1:  # TODO weakness, since a way through the hazard field is not considered as potentually better
        return handle_return_move(hazard_free_actions[0].get_move())

    last_selection_actions = hazard_free_actions

    if len(hazard_free_actions) == 0:  # TODO another weakness, since the snake immediately tries to escape the hazard. It might be better to simply go straight through it
        # Note : escape actions will contain always more than 0 actions, since collision_free_actions has at least 2 actions
        # at this point due to the previous if clauses
        escape_actions = get_escape_actions(collision_free_actions)

        # if there is only one direction to escape the hazards, simply go it
        if len(escape_actions) == 1:
            return handle_return_move(escape_actions[0].get_move())

        last_selection_actions = escape_actions

    # prevent head to head collision
    headless_free_actions = get_head_collision_free_actions(gamedata, last_selection_actions)
    if len(headless_free_actions) != 0:
        last_selection_actions = headless_free_actions

    # get food maps
    food_maps = get_food_maps(gamedata)

    best_move_idx = 0
    min_cost = 10000

    for i in range(len(food_maps)):
        food_map = food_maps[i]
        for j in range(len(last_selection_actions)):
            action = last_selection_actions[j]
            cost = food_map[action.get_position()["x"], action.get_position()["y"]]
            if cost < min_cost:
                min_cost = cost
                best_move_idx = j

    return handle_return_move(last_selection_actions[best_move_idx].get_move())


def get_head_collision_free_actions(gamedata: GameData, actions: List[Action]):
    head_collision_free_actions = []
    for action in actions:
        if is_action_head_collision_free(gamedata, action):
            head_collision_free_actions.append(action)

    return head_collision_free_actions


def is_action_head_collision_free(gamedata: GameData, action: Action):
    if is_snake_collision_space_free(gamedata.get_enemy_snakes(), action):
        return True

    if is_action_continuing(gamedata.get_my_snake(), action):
        # no enemy snake should get to the same position by following its current direction
        return (not is_continuing_head_collision_possible(gamedata.get_enemy_snakes(), action))

    return False


def is_continuing_head_collision_possible(enemy_snakes: List[Snake], action: Action):
    for enemy_snake in enemy_snakes:
        head_position = enemy_snake.get_head_position()
        if (abs(head_position["x"] - action.get_position()["x"]) + abs(head_position["y"] - action.get_position()["y"]) <= 1):
            return is_action_continuing(enemy_snake, action)
    return False


def is_snake_collision_space_free(enemy_snakes: List[Snake], action: Action):
    for enemy_snake in enemy_snakes:
        head_position = enemy_snake.get_head_position()
        if (abs(head_position["x"] - action.get_position()["x"]) + abs(head_position["y"] - action.get_position()["y"]) <= 1):
            return False
    return True


def is_action_continuing(snake: Snake, action: Action):
    neck_position = snake.get_body_positions()[1]
    return neck_position["x"] == action.get_position()["x"] or neck_position["y"] == action.get_position()["y"]


def handle_return_move(move: Move) -> string:
    global previous_move
    previous_move = move
    return move.value


def get_initial_actions(gamedata: GameData) -> List[dict]:
    my_head = gamedata.get_my_snake().get_head_position()
    board_width = gamedata.get_board_width()
    board_height = gamedata.get_board_height()

    left = Action({"x": (my_head["x"] - 1) % board_width, "y": my_head["y"]}, Move.left)
    right = Action({"x": (my_head["x"] + 1) % board_width, "y": my_head["y"]}, Move.right)
    up = Action({"x": my_head["x"], "y": (my_head["y"] + 1) % board_height}, Move.up)
    down = Action({"x": my_head["x"], "y": (my_head["y"] - 1) % board_height}, Move.down)

    return [left, right, up, down]


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


def get_hazard_free_actions(gamedata: GameData, actions: List[Action]) -> List[Action]:
    hazard_free_actions = []
    for action in actions:
        if is_hazard_free(gamedata, action.get_position()):
            hazard_free_actions.append(action)

    return hazard_free_actions


def is_hazard_free(gamedata: GameData, new_position: dict) -> bool:
    for position in gamedata.get_hazard_positions():
        if position["x"] == new_position["x"] and position["y"] == new_position["y"]:
            return False

    return True


def get_collision_free_actions(gamedata: GameData, actions: List[Action]) -> List[Action]:
    collision_free_actions = []
    for action in actions:
        if is_collision_free(gamedata, action.get_position()):
            collision_free_actions.append(action)
    return collision_free_actions


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


def get_escape_actions(actions: List[Action]) -> List[Action]:
    global previous_move

    escape_actions = []
    for action in actions:
        if action.get_move().value != previous_move.value:
            escape_actions.append(action)

    return escape_actions


def get_food_maps(gamedata: GameData):
    food_maps = []
    for food_position in gamedata.get_food_positions():
        food_map = get_food_map(gamedata, food_position)
        food_maps.append(food_map)
    return food_maps


def get_food_map(gamedata: GameData, food_position: dict):
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
