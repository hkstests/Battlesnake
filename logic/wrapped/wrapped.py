import string

import numpy as np
import os

from classes.GameData import GameData
from classes.Snake import Snake
from logic.enums.move import Move
from logic.wrapped.DQN import DQN
from logic.wrapped.Env import assemble_gamestate
from logic.wrapped.caches.SnakeCache import SnakeCache
from logic.wrapped.caches.SnakeCaches import SnakeCaches
import os
from dotenv import load_dotenv
load_dotenv()

is_local = os.getenv('IS_LOCAL') == "True"

dqn = DQN()

if os.path.isdir("logic/wrapped/mymodel"):
    print("load models")
    dqn.load_model("logic/wrapped/mymodel/model")
    dqn.load_target_model("logic/wrapped/mymodel/target-model")
    dqn.load_values("logic/wrapped/mymodel/values.pickle")

# will be reset in prepare function - see below
snake_caches = SnakeCaches("")
latest_trained_turn = 0
first_turn = 0  # can be either 0 or 1, dunno why


def handle_move(gamedata: GameData) -> string:
    global snake_caches
    global latest_trained_turn
    global first_turn
    global is_local

    # get corresponding snake cache
    snake_cache = snake_caches.get_snake_cache(gamedata.get_my_snake().get_id())

    # handle first turn
    # print(f"turn gamedata {gamedata.get_turn()} - turn first {first_turn}")
    if gamedata.get_turn() == first_turn:
        game_state = assemble_gamestate(gamedata)
        action = dqn.act(game_state)

        # cache values
        snake_cache.set_gamestate(game_state)
        snake_cache.set_gamedata(gamedata)
        snake_cache.set_action(action)

        return parse_action(action, gamedata.get_my_snake().get_direction())

    # handle later turns

    # compute properties
    new_gamestate = assemble_gamestate(gamedata)
    reward = _get_reward(gamedata, snake_cache)
    done = False

    # TODO dont know if that is wise
    # if np.random.random() < 0.55:
    dqn.remember(snake_cache.get_gamestate(), snake_cache.get_action(), reward, new_gamestate, done)

    if is_local and latest_trained_turn <= gamedata.get_turn():
        latest_trained_turn = gamedata.get_turn() + 1
        dqn.replay()
        dqn.target_train()

    action = dqn.act(new_gamestate)

    # cache values
    snake_cache.set_gamestate(new_gamestate)
    snake_cache.set_gamedata(gamedata)
    snake_cache.set_action(action)

    return parse_action(action, gamedata.get_my_snake().get_direction())


def _get_reward(gamedata: GameData, snake_cache: SnakeCache) -> float:
    reward = -0.75
    # TODO set good reward parameters
    if gamedata.is_game_over():
        if gamedata.has_my_snake_won():
            print(f"snake {gamedata.get_my_snake().get_id()} has won")
            return 20
        else:
            print(f"snake {gamedata.get_my_snake().get_id()} has lost")
            return -20
    if _has_enemy_snake_died(gamedata, snake_cache):
        reward = 10
    if _has_my_snake_eaten(gamedata, snake_cache):
        reward = 7
    if _has_my_snake_touched_hazard(gamedata, snake_cache):
        reward = -1
    return reward


def _has_enemy_snake_died(gamedata: GameData, snake_cache: SnakeCache):
    # check if number snake decreased which implies that at least one snake died
    return len(snake_cache.get_gamedata().get_enemy_snakes()) > len(gamedata.get_enemy_snakes())


def _has_my_snake_eaten(gamedata: GameData, snake_cache: SnakeCache):
    # compare health of my snake to the previous gamestate. if it increased, my snake must have eaten then
    return snake_cache.get_gamedata().get_my_snake().get_health() > gamedata.get_my_snake().get_health()


def _has_my_snake_touched_hazard(gamedata: GameData, snake_cache: SnakeCache):
    # compare health of my snake to previous gamestate. if it decreased more than 1, then my snake must have passed an hazard
    return snake_cache.get_gamedata().get_my_snake().get_health() >= gamedata.get_my_snake().get_health() + gamedata.get_hazard_damage()


# create Unofficial GameData class
def handle_end(gamedata: GameData):
    global snake_caches
    global is_local

    # extract corresponding snake_cache
    snake_cache = snake_caches.get_snake_cache(gamedata.get_my_snake().get_id())
    if snake_cache is None:
        return

    # values of new state does not matter since it is not used during the calculation anyway
    new_gamestate = np.zeros([0, 0])
    reward = _get_reward(gamedata, snake_cache)
    done = True

    # rememer state and train
    dqn.remember(snake_cache.get_gamestate(), snake_cache.get_action(), reward, new_gamestate, done)

    if is_local:
        dqn.replay()
        dqn.target_train()

    if is_local and snake_caches.get_open_saves() == 1:
        print("SAVE MODEL AND VALUES")
        dqn.save_model("logic/wrapped/mymodel/model")
        dqn.save_target_model("logic/wrapped/mymodel/target-model")
        dqn.save_values("logic/wrapped/mymodel/values.pickle")

    snake_cache.set_open_save(False)


def prepare(gamedata: GameData):
    global latest_trained_turn
    global first_turn
    global snake_caches
    global dqn
    global is_local

    latest_trained_turn = gamedata.get_turn()
    first_turn = gamedata.get_turn()

    if is_local:
        latest_trained_turn += 1
        first_turn += 1

    # if the current snake caches correspond to an older game, reset it
    if gamedata.get_id() != snake_caches.get_game_id():
        snake_caches = SnakeCaches(gamedata.get_id())
        dqn._initpredict(dqn.model)
        dqn._initpredict(dqn.target_model)

    # add one snake cache for the current snake
    snake_caches.add_snake_cache(gamedata.get_my_snake().get_id())

    print(f"number of snake caches : {len(snake_caches._snake_caches)}")


def parse_action(action, snake_direction: string):
    # action 0 = follow, 1 = turn left, 2 = turn right

    if snake_direction == "left":
        if action == 0:
            return "left"
        elif action == 1:
            return "down"
        else:  # action==2
            return "up"
    elif snake_direction == "right":
        if action == 0:
            return "right"
        elif action == 1:
            return "up"
        else:  # action==2
            return "down"
    elif snake_direction == "up":
        if action == 0:
            return "up"
        elif action == 1:
            return "left"
        else:  # action==2
            return "right"
    else:  # direction down
        if action == 0:
            return "down"
        elif action == 1:
            return "right"
        else:  # action==2
            return "left"
