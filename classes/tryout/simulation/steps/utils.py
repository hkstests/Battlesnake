

from classes.tryout.Gamedata import Gamedata
from classes.tryout.Snake import Snake


def get_snake_by_id(gamedata: Gamedata, id: str) -> Snake:
    for snake in gamedata.snakes:
        if snake.id == id:
            return snake

    return None
