from typing import List
from classes.tryout.Gamedata import Gamedata
from classes.tryout.Snake import Snake


def remove_starved_snakes(gamedata: Gamedata):
    for i in range(0, len(gamedata.snakes)):
        if gamedata.snakes[i].health <= 0:
            gamedata.snakes.pop(i)
            i -= 1


def remove_self_collided_snakes(gamedata: Gamedata):
    snakes_alive: List[Snake] = []

    for snake in gamedata.snakes:
        stays_alive = True
        for i in range(1, len(snake.body)):
            if snake.head.x == snake.body[i].x and snake.head.y == snake.body[i].y:
                stays_alive = False
        if stays_alive:
            snakes_alive.append(snake)

    gamedata.snakes = snakes_alive


def remove_snake_collided_snakes(gamedata: Gamedata):
    snakes_alive: List[Snake] = []
    for s1 in gamedata.snakes:
        stays_alive = True
        for s2 in gamedata.snakes:
            if s1.id == s2.id:
                continue
            for i in range(0, len(s2.body)):
                pos = s2.body[i]
                if s1.head.x == pos.x and s1.head.y == pos.y:
                    # check if it is head to head collision and let snake with more health survive
                    if i == 0:
                        stays_alive = s1.health > s2.health
                    else:
                        stays_alive = False
        if stays_alive:
            snakes_alive.append(s1)

    gamedata.snakes = snakes_alive


def remove_wall_collided_snakes(gamedata: Gamedata):
    snakes_alive: List[Snake] = []
    for snake in gamedata.snakes:
        if snake.head.x >= 0 and snake.head.x <= gamedata.board_width and snake.head.y >= 0 and snake.head.y <= gamedata.board_height:
            snakes_alive.append(snake)
    gamedata.snakes = snakes_alive
