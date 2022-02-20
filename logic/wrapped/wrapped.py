import string

import numpy as np

from classes.GameData import GameData
from logic.enums.move import Move
from logic.wrapped.DQN import DQN
from logic.wrapped.Env import assemble_gamestate
from logic.wrapped.caches.SnakeCache import SnakeCache
from logic.wrapped.caches.SnakeCaches import SnakeCaches

dqn = DQN()
# TODO
# check if model weights exist and load them respectively

# will be reset in prepare function - see below
snake_caches = SnakeCaches("")
latest_trained_turn = 0
first_turn = 0  # can be either 0 or 1, dunno why


def handle_move(gamedata: GameData) -> string:
    global snake_caches
    global latest_trained_turn
    global first_turn

    # get corresponding snake cache
    snake_cache = snake_caches.get_snake_cache(gamedata.get_my_snake().get_id())

    # handle first turn
    if gamedata.get_turn() == first_turn:
        game_state = assemble_gamestate(gamedata)
        action = dqn.act(game_state)

        # cache values
        snake_cache.set_gamestate(game_state)
        snake_cache.set_gamedata(gamedata)
        snake_cache.set_action(action)

        # TODO parse action and return it respectively
        return Move.left.value

    # handle later turns

    # compute properties
    new_gamestate = assemble_gamestate(gamedata)
    # gamedata.print()
    # print("hihi")
    reward = _get_reward(gamedata, snake_cache)
    done = False

    dqn.remember(snake_cache.get_gamestate(), snake_cache.get_action(), reward, new_gamestate, done)

    if latest_trained_turn <= gamedata.get_turn():
        latest_trained_turn = gamedata.get_turn() + 1
        dqn.replay()
        dqn.target_train()

    action = dqn.act(new_gamestate)

    # cache values
    snake_cache.set_gamestate(new_gamestate)
    snake_cache.set_gamedata(gamedata)
    snake_cache.set_action(action)

    # TODO parse action and return it respectively

    return Move.left.value


def _get_reward(gamedata: GameData, snake_cache: SnakeCache) -> float:
    reward = 0
    # TODO set good reward parameters
    if gamedata.is_game_over():
        if gamedata.has_my_snake_won():
            return 10
        else:
            return -10
    if _has_enemy_snake_died(gamedata, snake_cache):
        reward = 3
    if _has_my_snake_eaten(gamedata, snake_cache):
        reward = 2
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
    return snake_cache.get_gamedata().get_my_snake().get_health() > gamedata.get_my_snake().get_health() + 5  # TODO include hazard dmg


# create Unofficial GameData class
def handle_end(gamedata: GameData):
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
    dqn.replay()
    dqn.target_train()


def prepare(gamedata: GameData):
    global latest_trained_turn
    global first_turn
    global snake_caches

    latest_trained_turn = gamedata.get_turn() + 1
    first_turn = gamedata.get_turn() + 1

    # if the current snake caches correspond to an older game, reset it
    if gamedata.get_id() != snake_caches.get_game_id():
        snake_caches = SnakeCaches(gamedata.get_id())

    # add one snake cache for the current snake
    snake_caches.add_snake_cache(gamedata.get_my_snake().get_id())

    print(f"number of snake caches : {len(snake_caches._snake_caches)}")
