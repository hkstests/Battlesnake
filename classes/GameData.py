
import copy
import string
from typing import List
from classes.Snake import Snake
from classes.enums.mode import Mode


class GameData():
    def __init__(self, data):
        self._data = data

        # your snake
        self._my_snake = Snake(self._data["you"])

        # team snakes (will be empty if squad is not set)
        self._team_snakes = extract_team_snakes(
            self._my_snake, self._data["board"]["snakes"])

        # add enemy snakes
        self._enemy_snakes = extract_enemy_snakes(
            self._my_snake, self._data["board"]["snakes"])

    def get_id(self) -> string:
        return self._data["game"]["id"]

    def is_game_over(self) -> string:
        draw = self._data["board"]["snakes"] is None
        if draw:
            return True

        living_snakes_count = len(self._data["board"]["snakes"])
        return (living_snakes_count == 0 or living_snakes_count == 1)

    def has_my_snake_won(self) -> bool:
        my_snake_id = self.get_my_snake().get_id()
        draw = self._data["board"]["snakes"] is None
        if draw:
            return False

        living_snakes = self._data["board"]["snakes"]
        return (len(living_snakes) == 1 and living_snakes[0]["id"] == my_snake_id)

    def get_turn(self) -> int:
        return self._data["turn"]

    def is_standard_mode(self) -> bool:
        """
            Returns true if the game is in standard mode, else false
        """
        # print(Mode.standard)
        return self._data["game"]["ruleset"]["name"] == Mode.standard.value

    def is_royale_mode(self) -> bool:
        """
            Returns true if the game is in royale mode, else false
        """
        return self._data["game"]["ruleset"]["name"] == Mode.royale.value

    def is_squad_mode(self) -> bool:
        """
            Returns true if the game is in squad mode, else false
        """
        return self._data["game"]["ruleset"]["name"] == Mode.squad.value

    def is_constrictor_mode(self) -> bool:
        """
            Returns true if the game is in constrictor mode, else false
        """
        return self._data["game"]["ruleset"]["name"] == Mode.constrictor.value

    def is_wrapped_mode(self) -> bool:
        """
            Returns true if the game is in wrapped mode, else false
        """
        return self._data["game"]["ruleset"]["name"] == Mode.wrapped.value

    def get_board_width(self) -> int:
        """
            Returns the width of the board
        """
        return self._data["board"]["width"]

    def get_board_height(self) -> int:
        """
            Returns the height of the board
        """
        return self._data["board"]["height"]

    def get_food_positions(self) -> List[dict]:
        """
            Array of coordinates representing food locations on the game board.
            Example: [{"x": 5, "y": 5}, ..., {"x": 2, "y": 6}]
        """
        return self._data["board"]["food"]

    def get_hazard_positions(self) -> List[dict]:
        """
            Array of coordinates representing hazardous locations on the game board. These will only appear in some game modes.
            Example: [{"x": 0, "y": 0}, ..., {"x": 0, "y": 1}]
        """
        return self._data["board"]["hazards"]

    def get_food_spawn_chance(self) -> int:
        """
            Percentage chance (value in range of (0,100] ) of spawning a new food every round.
        """
        return self._data["game"]["ruleset"]["settings"]["foodSpawnChance"]

    def get_minimum_food_count(self) -> int:
        """
            Minimum food to keep on the board every turn.
        """
        return self._data["game"]["ruleset"]["settings"]["minimumFood"]

    def get_hazard_damage(self) -> int:
        """
            Health damage a snake will take when ending its turn in a hazard. This stacks on top of the regular 1 damage a snake takes per turn.
        """
        return self._data["game"]["ruleset"]["settings"]["hazardDamagePerTurn"]

    def get_royal_shrink_n_turns(self) -> int:
        """
            In Royale mode, the number of turns between generating new hazards (shrinking the safe board space).
        """
        return self._data["game"]["ruleset"]["settings"]["royale"]["shrinkEveryNTurns"]

    def is_squad_body_collision_allowed(self) -> bool:
        """
            In Squad mode, it is true if members of the same squad are allowed to move over each other without dying.
        """
        return self._data["game"]["ruleset"]["settings"]["squad"]["allowBodyCollisions"]

    def is_squad_shared_elimination_on(self) -> bool:
        """
            In Squad mode, it is true if all squad members are eliminated when one is eliminated.
        """
        return self._data["game"]["ruleset"]["settings"]["squad"]["sharedElimination"]

    def is_squad_shared_health_on(self) -> bool:
        """
            In Squad mode, it is true if all squad members share health.
        """
        return self._data["game"]["ruleset"]["settings"]["squad"]["sharedHealth"]

    def is_squad_shared_length_on(self) -> bool:
        """
            In Squad mode, it is true if all squad members share length.
        """
        return self._data["game"]["ruleset"]["settings"]["squad"]["sharedLength"]

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

    def print(self):
        print(f"is standard mode : {self.is_standard_mode()}")
        print(f"is royale mode : {self.is_royale_mode()}")
        print(f"is squad mode : {self.is_squad_mode()}")
        print(f"is constrictor mode : {self.is_constrictor_mode()}")
        print(f"is wrapped mode : {self.is_wrapped_mode()}")
        print("---------------------------------------------------")
        print(f"board width : {self.get_board_width()}")
        print(f"board height : {self.get_board_height()}")
        print(f"food spawn chance : {self.get_food_spawn_chance()}")
        print(f"food minimum count : {self.get_minimum_food_count()}")
        print(f"hazard damage {self.get_hazard_damage()}")
        print("---------------------------------------------------")
        print(f"royale shrink n turns {self.get_royal_shrink_n_turns()}")
        print("---------------------------------------------------")
        print(
            f"is squad body collision allowed {self.is_squad_body_collision_allowed()}")
        print(
            f"is squad shared elimination on : {self.is_squad_shared_elimination_on()}")
        print(
            f"is squad shared health on : {self.is_squad_shared_health_on()}")
        print(
            f"is squad shared length on : {self.is_squad_shared_length_on()}")
        print("---------------------------------------------------")
        print(f"food positions : {self.get_food_positions()}")
        print(f"hazard positions : {self.get_hazard_positions()}")
        print("---------------------------------------------------")
        print("---------------------------------------------------")
        self.get_my_snake().print("my snake")
        print("---------------------------------------------------")
        for team_snake in self.get_team_snakes():
            team_snake.print("team snake")
        print("---------------------------------------------------")
        for enemy_snake in self.get_enemy_snakes():
            enemy_snake.print("enemy snake")


def extract_team_snakes(my_snake, snakes):
    team_snakes = []
    if my_snake.get_squad() == "" or snakes == None:
        return team_snakes

    for i in range(0, len(snakes)):
        if snakes[i]["id"] != my_snake.get_id() and snakes[i]["squad"] == my_snake.get_squad():
            team_snakes.append(Snake(snakes[i]))

    return team_snakes


def extract_enemy_snakes(my_snake, snakes):
    enemy_snakes = []

    if snakes == None:
        return enemy_snakes

    for i in range(0, len(snakes)):
        if snakes[i]["id"] != my_snake.get_id():
            if (my_snake.get_squad() == "") or my_snake.get_squad() == snakes[i]["squad"]:
                enemy_snakes.append(Snake(snakes[i]))

    return enemy_snakes
