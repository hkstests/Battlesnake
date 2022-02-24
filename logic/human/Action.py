from logic.enums.move import Move


class Action:

    def __init__(self, position: dict, move: Move):
        self._position = position
        self._move = move

    def get_position(self):
        return self._position

    def get_move(self):
        return self._move
