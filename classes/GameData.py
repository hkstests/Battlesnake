
from typing import List
from classes.Snake import Snake


class GameData():
    def __init__(self, data):
        self._game = data

        # your snake
        self._my_snake = Snake(self._game["you"])

        _snakes = self._game["snakes"]

        # team snakes (will be empty if squad is not set)
        self._team_snakes = extract_team_snakes(self._my_snake, _snakes)

        # add enemy snakes
        self._enemy_snakes = extract_enemy_snakes(self._my_snake, _snakes)

    def is_standard_mode(self) -> bool:
        """
            Returns true if the game is in standard mode, else false
        """
        return self._game["game"]["ruleset"]["name"] == "standard"

    def is_royal_mode(self) -> bool:
        """
            Returns true if the game is in royal mode, else false
        """
        return self._game["game"]["ruleset"]["name"] == "royal"

    def is_squad_mode(self) -> bool:
        """
            Returns true if the game is in squad mode, else false
        """
        return self._game["game"]["ruleset"]["name"] == "squad"

    def is_constrictor_mode(self) -> bool:
        """
            Returns true if the game is in constrictor mode, else false
        """
        return self._game["game"]["ruleset"]["name"] == "constrictor"

    def is_wrapped_mode(self) -> bool:
        """
            Returns true if the game is in wrapped mode, else false
        """
        return self._game["game"]["ruleset"]["name"] == "wrapped"

    def get_board_width(self) -> int:
        """
            Returns the width of the board
        """
        return self._game["board"]["width"]

    def get_board_height(self) -> int:
        """
            Returns the height of the board
        """
        return self._game["board"]["height"]

    def get_food_positions(self) -> List[dict]:
        """
            Array of coordinates representing food locations on the game board.
            Example: [{"x": 5, "y": 5}, ..., {"x": 2, "y": 6}]
        """
        return self._game["board"]["food"]

    def get_hazard_positions(self) -> List[dict]:
        """
            Array of coordinates representing hazardous locations on the game board. These will only appear in some game modes.
            Example: [{"x": 0, "y": 0}, ..., {"x": 0, "y": 1}]
        """
        return self._game["board"]["hazards"]

    def get_food_spawn_chance(self) -> int:
        """
            Percentage chance (value in range of (0,100] ) of spawning a new food every round.
        """
        return self._game["ruleset"]["settings"]["foodSpawnChance"]

    def get_minimum_food_count(self) -> int:
        """
            Minimum food to keep on the board every turn.
        """
        return self._game["ruleset"]["settings"]["minimumFood"]

    def get_hazard_damage(self) -> int:
        """
            Health damage a snake will take when ending its turn in a hazard. This stacks on top of the regular 1 damage a snake takes per turn.
        """
        return self._game["ruleset"]["settings"]["hazardDamagePerTurn"]

    def get_royal_shrink_n_turns(self) -> int:
        """
            In Royale mode, the number of turns between generating new hazards (shrinking the safe board space).
        """
        return self._game["ruleset"]["settings"]["royal"]["shrinkEveryNTurns"]

    def is_squad_body_collision_allowed(self) -> bool:
        """
            In Squad mode, it is true if members of the same squad are allowed to move over each other without dying.
        """
        return self._game["ruleset"]["settings"]["squad"]["allowBodyCollisions"]

    def is_squad_shared_elimination_on(self) -> bool:
        """
            In Squad mode, it is true if all squad members are eliminated when one is eliminated.
        """
        return self._game["ruleset"]["settings"]["squad"]["sharedElimination"]

    def is_squad_shared_health_on(self) -> bool:
        """
            In Squad mode, it is true if all squad members share health.
        """
        return self._game["ruleset"]["settings"]["squad"]["sharedHealth"]

    def is_squad_shared_length_on(self) -> bool:
        """
            In Squad mode, it is true if all squad members share length.
        """
        return self._game["ruleset"]["settings"]["squad"]["sharedLength"]

    def get_my_snake(self) -> Snake:
        """
            Returns a snake object representing your own snake
        """
        return self._my_snake

    def get_team_snakes(self) -> List[Snake]:
        """
            Returns a list of snake objects representing your team snakes. This list is empty when the game mode is not squad
        """
        return self._team_snakes

    def get_enemy_snakes(self) -> List[Snake]:
        """
            Returns a list of snake objects representing your enemy snakes.
        """
        return self._enemy_snakes


def extract_team_snakes(my_snake, snakes):
    team_snakes = []
    if my_snake.get_squad() == "":
        return team_snakes

    for i in range(0, len(snakes)):
        if snakes[i]["id"] != my_snake.get_id() and snakes[i]["squad"] == my_snake.get_squad():
            team_snakes.append(Snake(snakes[i]))

    return team_snakes


def extract_enemy_snakes(my_snake, snakes):
    enemy_snakes = []

    for i in range(0, len(snakes)):
        if snakes[i]["id"] != my_snake.get_id():
            if (my_snake.get_squad() == "") or my_snake.get_squad() == snakes[i]["squad"]:
                enemy_snakes.append(Snake(snakes[i]))

    return enemy_snakes
