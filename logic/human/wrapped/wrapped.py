from math import floor
import string
from typing import List

import numpy as np
from classes.Snake import Snake
from classes.GameData import GameData
from logic.human.Action import Action
from logic.enums.move import Move


def handle_move(gamedata: GameData) -> string:
    # get actions left, right, up, down with their respective position (with respect to the head position)
    possible_actions = get_initial_actions(gamedata)

    # print(f"possible_actions {len(possible_actions)}")

    # remove actions that would lead to a collision (with itself or other snakes)
    collision_free_actions = get_collision_free_actions(gamedata, possible_actions)
    # print(f"collision_free_actions {len(collision_free_actions)}")

    # just go left if you'd die anyway due to collision
    if len(collision_free_actions) == 0:
        return Move.left.value

    # if only one move is possible, simply do it
    if len(collision_free_actions) == 1:
        return collision_free_actions[0].get_move().value

    last_selection_actions = collision_free_actions

    headless_free_actions = get_head_collision_save_actions(gamedata, last_selection_actions)
    # print(f"headless_free_actions {len(headless_free_actions)}")
    if len(headless_free_actions) == 1:
        return headless_free_actions[0].get_move().value
    elif len(headless_free_actions) >= 2:
        last_selection_actions = headless_free_actions

    open_space_actions = get_open_space_actions(gamedata, last_selection_actions)

    if len(open_space_actions) == 1:
        return open_space_actions[0].get_move().value
    elif len(open_space_actions) >= 2:
        last_selection_actions = open_space_actions

    save_mode = len(gamedata.get_hazard_positions())/(gamedata.get_board_width() * gamedata.get_board_height()) <= 0.6

    # get hazard free actions
    hazard_free_actions = get_hazard_free_actions(gamedata, last_selection_actions)
    # print(f"hazard_free_actions {len(hazard_free_actions)}")

    # if there is only one way to prevent a hazard, simply go it
    if len(hazard_free_actions) == 1:  # TODO weakness, since a way through the hazard field is not considered as potentually better
        return hazard_free_actions[0].get_move().value

    elif len(hazard_free_actions) == 0 and save_mode:  # TODO another weakness, since the snake immediately tries to escape the hazard. It might be better to simply go straight through it
        # Note : escape actions will contain always more than 0 actions, since collision_free_actions has at least 2 actions
        # at this point due to the previous if clauses

        escape_actions = get_hazard_escape_actions(gamedata, gamedata.get_hazard_positions(), last_selection_actions)
        # print(f"escape_actions {len(escape_actions)}")

        # if there is only one direction to escape the hazards, simply go it
        if len(escape_actions) == 1:
            return escape_actions[0].get_move().value

        last_selection_actions = escape_actions

    else:
        last_selection_actions = hazard_free_actions

    # get food positions outside of hazards
    food_positions = []
    for food_position in gamedata.get_food_positions():
        is_food_in_hazard = False
        for hazard_position in gamedata.get_hazard_positions():
            if food_position["x"] == hazard_position["x"] and food_position["y"] == hazard_position["y"]:
                is_food_in_hazard = True
                break
        if not is_food_in_hazard:
            food_positions.append(food_position)

    if len(food_positions) == 0:
        food_positions = gamedata.get_food_positions()

    # get food maps
    food_maps = get_food_maps(gamedata, food_positions)

    min_cost = 10000
    best_actions = []

    # print(food_maps[0])

    for i in range(len(food_maps)):
        food_map = food_maps[i]
        for j in range(len(last_selection_actions)):
            action = last_selection_actions[j]
            cost = food_map[action.get_position()["x"], action.get_position()["y"]]
            if cost < min_cost:
                best_actions = [action]
                min_cost = cost
            elif cost == min_cost:
                best_actions.append(action)

    if len(best_actions) == 1:
        return best_actions[0].get_move().value

    return get_targeted_kill_action(gamedata, best_actions).get_move().value


def get_targeted_kill_action(gamedata: GameData, actions: List[Action]) -> Action:
    for action in actions:
        if is_targeted_kill_action(gamedata, action):
            return action
    return actions[0]


def is_targeted_kill_action(gamedata: GameData, action: Action) -> bool:
    for enemy_snake in gamedata.get_enemy_snakes():
        if is_enemy_snake_close_to_action(gamedata, enemy_snake, action):
            enemy_smaller = len(enemy_snake.get_body_positions()) < len(gamedata.get_my_snake().get_body_positions())
            return enemy_smaller
    return False


def get_open_space_actions(gamedata: GameData, actions: List[Action]) -> List[Action]:
    invalid = 1000
    board = np.ones([gamedata.get_board_width(), gamedata.get_board_height()])

    for position in gamedata.get_my_snake().get_body_positions():
        board[position["x"], position["y"]] = invalid

    for enemy_snake in gamedata.get_enemy_snakes():
        for position in enemy_snake.get_body_positions():
            board[position["x"], position["y"]] = invalid

    open_space_actions = []

    for action in actions:
        space = floodFill(action.get_position(), board, [action.get_position()], invalid, 6, 0)
        # print(f"space {space}")
        if space >= 6:
            open_space_actions.append(action)

    return open_space_actions


def floodFill(position, board, visited_positions, invalid, max_iter, iter):
    if iter >= max_iter:
        return 0

    visited_positions.append(position)

    left = {"x": (position["x"] - 1) % board.shape[0], "y": position["y"]}
    right = {"x": (position["x"] + 1) % board.shape[0], "y": position["y"]}
    up = {"x": position["x"], "y": (position["y"] + 1) % board.shape[1]}
    down = {"x": position["x"], "y": (position["y"] - 1) % board.shape[1]}

    next_positions = []

    if board[left["x"], left["y"]] != invalid:
        next_positions.append(left)

    if board[right["x"], right["y"]] != invalid:
        next_positions.append(right)

    if board[up["x"], up["y"]] != invalid:
        next_positions.append(up)

    if board[down["x"], down["y"]] != invalid:
        next_positions.append(down)

    value = 1

    for next_position in next_positions:
        already_visited = False
        for visited_position in visited_positions:
            if next_position["x"] == visited_position["x"] and next_position["y"] == visited_position["y"]:
                already_visited = True

        if not already_visited:
            value += floodFill(next_position, board, visited_positions, invalid, max_iter, iter + 1)

    return value


def get_head_collision_save_actions(gamedata: GameData, actions: List[Action]) -> List[Action]:
    head_collision_free_actions = []
    for action in actions:
        if is_action_head_collision_save(gamedata, action):
            head_collision_free_actions.append(action)

    return head_collision_free_actions


def is_enemy_snake_close_to_action(gamedata: GameData, enemy_snake: Snake, action) -> bool:
    head_position = enemy_snake.get_head_position()
    is_horizontal_next = head_position["x"] == action.get_position()["x"] and ((head_position["y"] + 1) % gamedata.get_board_height() == action.get_position()
                                                                               ["y"] or (head_position["y"] - 1) % gamedata.get_board_height() == action.get_position()["y"])
    is_vertical_next = head_position["y"] == action.get_position()["y"] and ((head_position["x"] + 1) % gamedata.get_board_width() == action.get_position()
                                                                             ["x"] or (head_position["x"] - 1) % gamedata.get_board_width() == action.get_position()["x"])
    return is_horizontal_next or is_vertical_next


def is_action_head_collision_save(gamedata: GameData, action: Action):
    for enemy_snake in gamedata.get_enemy_snakes():
        if is_enemy_snake_close_to_action(gamedata, enemy_snake, action):
            enemy_smaller = len(enemy_snake.get_body_positions()) < len(gamedata.get_my_snake().get_body_positions())
            return enemy_smaller
    return True


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
    return False


def get_food_maps(gamedata: GameData, food_positions):
    food_maps = []

    for food_position in food_positions:
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

    for position in gamedata.get_hazard_positions():
        board[position["x"], position["y"]] = invalid

    board[food_position["x"], food_position["y"]] = 0

    compute_food_distance_board(board, food_position, unvisited, invalid)

    return board


def get_hazard_escape_actions(gamedata: GameData, hazard_positions: List[dict], actions: List[Action]):
    hazard_distance_board = get_hazard_distance_board(gamedata, hazard_positions)

    min_distance = 10000
    for action in actions:
        distance = hazard_distance_board[action.get_position()["x"], action.get_position()["y"]]
        if distance < min_distance:
            min_distance = distance

    hazard_escape_actions = []
    for action in actions:
        distance = hazard_distance_board[action.get_position()["x"], action.get_position()["y"]]
        if distance == min_distance:
            hazard_escape_actions.append(action)

    return hazard_escape_actions


def get_hazard_distance_board(gamedata: GameData, hazard_positions: List[dict]):
    invalid = 1000
    unvisited = 999

    board_width = gamedata.get_board_width()
    board_height = gamedata.get_board_height()

    board = np.ones([board_width, board_height])
    board *= unvisited

    for i in range(board_width):
        for j in range(board_height):
            is_hazard = False
            for hazard_position in hazard_positions:
                if i == hazard_position["x"] and j == hazard_position["y"]:
                    is_hazard = True
            if not is_hazard:
                board[i, j] = 0

    for position in gamedata.get_my_snake().get_body_positions():
        board[position["x"], position["y"]] = invalid

    for enemy_snake in gamedata.get_enemy_snakes():
        for position in enemy_snake.get_body_positions():
            board[position["x"], position["y"]] = invalid

    compute_hazard_distance_board(board, unvisited, invalid)

    return board


def compute_food_distance_board(board, position, unvisited, invalid):
    # TODO this implementation sucks, change it later

    board_width = board.shape[0]
    board_height = board.shape[1]

    filter_size = 3

    while filter_size <= board_width * 2:
        filter_start_x = (position["x"] - floor(filter_size/2)) % board_width
        filter_start_y = (position["y"] - floor(filter_size/2)) % board_height

        for i in range(0, filter_size):
            for j in range(0, filter_size):
                x = (filter_start_x + i) % board_width
                y = (filter_start_y + j) % board_height
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
            for j in range(filter_start_y, filter_size):
                x = (filter_start_x + i) % board_width
                y = (filter_start_y + j) % board_height
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

        filter_size += 2


def compute_hazard_distance_board(board, unvisited: float, invalid: float):
    board_width = board.shape[0]
    board_height = board.shape[1]

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
