

import copy
from typing import Callable, List

from classes.tryout.Gamedata import Gamedata
from classes.tryout.simulation.Moverequest import Moverequest

# import (sub)steps
from classes.tryout.simulation.steps.move_snakes import *
from classes.tryout.simulation.steps.update_health import *
from classes.tryout.simulation.steps.remove_snakes import *
from classes.tryout.simulation.steps.add_hazard import *
from classes.tryout.simulation.steps.spawn_food import *


def wrapped_spiral_simulator(gamedata: Gamedata, moverequests: List[Moverequest], should_update_turn=True) -> Gamedata:
    return _simulate_step(
        gamedata=gamedata,
        should_update_turn=should_update_turn,
        moverequests=moverequests,
        move_snakes=move_snakes_wrapped,
        substeps=[
            remove_self_collided_snakes,
            remove_snake_collided_snakes,
            add_hazard_spiral,
            update_health_standard_move,
            update_health_through_hazard,
            update_health_through_food,
            remove_starved_snakes,
            spawn_food
        ]
    )


def standard_simulator(gamedata: Gamedata, moverequests: List[Moverequest], should_update_turn=True) -> Gamedata:
    return _simulate_step(
        gamedata=gamedata,
        should_update_turn=should_update_turn,
        moverequests=moverequests,
        move_snakes=move_snakes_standard,
        substeps=[
            remove_wall_collided_snakes,
            remove_self_collided_snakes,
            remove_snake_collided_snakes,
            update_health_standard_move,
            update_health_through_food,
            remove_starved_snakes,
            spawn_food
        ]
    )


def _simulate_step(gamedata: Gamedata, moverequests: List[Moverequest], move_snakes: Callable[[Gamedata, List[Moverequest]], Gamedata], substeps: List[Callable], should_update_turn=True) -> Gamedata:
    gamedata = copy.deepcopy(gamedata)

    _update_turn(gamedata, should_update_turn)
    move_snakes(gamedata, moverequests)
    # gamedata.print()

    for substep in substeps:
        substep(gamedata)

    my_snake = get_snake_by_id(gamedata, gamedata.my_snake.id)
    if my_snake is not None:
        gamedata.my_snake = my_snake

    return gamedata


def _update_turn(gamedata: Gamedata, should_update_turn=True):
    if should_update_turn:
        gamedata.turn += 1
