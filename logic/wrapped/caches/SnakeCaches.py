import string
from typing import List
from logic.wrapped.caches.SnakeCache import SnakeCache


class SnakeCaches:
    def __init__(self, game_id: string):
        self._snake_caches: List[SnakeCache] = []
        self._game_id = game_id

    def add_snake_cache(self, id: string):
        snake_cache = SnakeCache(id)
        self._snake_caches.append(snake_cache)

    def get_snake_cache(self, id: string):
        for snake_cache in self._snake_caches:
            if snake_cache.get_id() == id:
                return snake_cache

    def get_open_saves(self):
        count = 0
        for snake_cache in self._snake_caches:
            if snake_cache.get_open_save():
                count += 1
        return count

    def get_game_id(self):
        return self._game_id
