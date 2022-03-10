

from typing import List
from classes.tryout.Snake import Snake
from classes.tryout.Gamedata import Gamedata
from classes.tryout.Position import Position
from classes.tryout.simulation.Moverequest import Moverequest
from classes.tryout.simulation.steps.utils import get_snake_by_id


def move_snakes_standard(gamedata: Gamedata, moverequests: List[Moverequest]):
    for moverequest in moverequests:
        snake = get_snake_by_id(gamedata, moverequest.id)
        next_head_position = _compute_next_head_position(snake, moverequest)
        _move_snake(snake, next_head_position)


def move_snakes_wrapped(gamedata: Gamedata, moverequests: List[Moverequest]):
    for moverequest in moverequests:
        snake = get_snake_by_id(gamedata, moverequest.id)
        next_head_position = _compute_next_head_position(snake, moverequest)
        # use mod for wrapped movement
        next_head_position = Position(next_head_position.x % gamedata.board_width, next_head_position.y % gamedata.board_height)
        _move_snake(snake, next_head_position)


def _compute_next_head_position(snake: Snake, moverequest: Moverequest) -> Position:
    next_head_position = Position(0, 0)
    if moverequest.move == "left":
        next_head_position = Position(snake.head.x - 1, snake.head.y)
    elif moverequest.move == "right":
        next_head_position = Position(snake.head.x + 1, snake.head.y)
    elif moverequest.move == "up":
        next_head_position = Position(snake.head.x, snake.head.y + 1)
    elif moverequest.move == "down":
        next_head_position = Position(snake.head.x, snake.head.y - 1)
    return next_head_position


def _move_snake(snake: Snake, next_head_position: Position):
    # iterate through all except the head (start with 1 because the iteration goes backwards)
    for i in range(1, len(snake.body)):

        next_position = snake.body[-i - 1]
        # the inequality check is necessary for 2 cases
        #   - if snake has eaten smth, the last part of the snake should remain
        #   - at the beginning of the game, all 3 parts of the snake are at the same position -> move them subsequently
        if next_position.x != snake.body[-i].x or next_position.y != snake.body[-i].y:
            snake.body[-i] = Position(next_position.x, next_position.y)

    snake.head = next_head_position
    snake.body[0] = Position(snake.head.x, snake.head.y)
