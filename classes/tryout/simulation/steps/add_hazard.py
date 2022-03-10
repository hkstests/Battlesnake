

from typing import List
from classes.tryout.Gamedata import Gamedata
from classes.tryout.Position import Position


_spiral_hazard_map: List[Position] = []


def add_hazard_spiral(gamedata: Gamedata):
    global _spiral_hazard_map

    # prebuild spiral hazard map as soon as the first hazard position is known
    if len(gamedata.hazards) == 1 and len(_spiral_hazard_map) == 0:
        _prebuild_spiral_hazard_map(gamedata)

    # hazards only appear every 3 rounds
    if gamedata.turn % 3 != 0:
        return

    x_th_hazard = int(gamedata.turn / 3) - 1
    new_hazard = _spiral_hazard_map[x_th_hazard]

    # check if new hazard position is on board. If so, add it
    if x_th_hazard > 0 and new_hazard.x >= 0 and new_hazard.x <= gamedata.board_width and new_hazard.y >= 0 and new_hazard.y <= gamedata.board_height:
        gamedata.hazards.append(new_hazard)


def add_hazard_scatter(gamedata: Gamedata):
    pass


def add_hazard_royal(gamedata: Gamedata):
    pass


def _prebuild_spiral_hazard_map(gamedata: Gamedata):
    global _spiral_hazard_map

    up_right_size = 0
    down_left_size = 0

    _spiral_hazard_map.append(gamedata.hazards[0])

    for i in range(0, 5):

        # add positions towards top
        up_right_size = down_left_size + 1
        last_hazard = _spiral_hazard_map[-1]
        for y in range(1, up_right_size + 1):
            _spiral_hazard_map.append(Position(last_hazard.x, last_hazard.y + y))

        # add positions towards right
        last_hazard = _spiral_hazard_map[-1]
        for x in range(1, up_right_size + 1):
            _spiral_hazard_map.append(Position(last_hazard.x + x, last_hazard.y))

        # add positions towards down
        down_left_size = up_right_size + 1
        last_hazard = _spiral_hazard_map[-1]
        for y in range(1, down_left_size + 1):
            _spiral_hazard_map.append(Position(last_hazard.x, last_hazard.y - y))

        # add positions towards left
        last_hazard = _spiral_hazard_map[-1]
        for x in range(1, down_left_size + 1):
            _spiral_hazard_map.append(Position(last_hazard.x - x, last_hazard.y))
