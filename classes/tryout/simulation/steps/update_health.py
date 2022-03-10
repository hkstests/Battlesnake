

from classes.tryout.Gamedata import Gamedata
from classes.tryout.Position import Position


def update_health_standard_move(gamedata: Gamedata):
    for snake in gamedata.snakes:
        snake.health -= 1


def update_health_through_hazard(gamedata: Gamedata):
    for snake in gamedata.snakes:
        for hazard in gamedata.hazards:
            if snake.head.x == hazard.x and snake.head.y == hazard.y:
                snake.health -= gamedata.hazard_damage_per_turn
                break


def update_health_through_food(gamedata: Gamedata):
    for snake in gamedata.snakes:
        for food_position in gamedata.food:
            if snake.head.x == food_position.x and snake.head.y == food_position.y:
                gamedata.food.remove(food_position)
                snake.health = 100
                tail = snake.body[-1]
                snake.body.append(Position(tail.x, tail.y))
