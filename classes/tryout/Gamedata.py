

import TestRequestBody
from typing import List
from classes.tryout.Position import Position
from classes.tryout.Snake import Snake


class Gamedata():
    """A bird with a flight speed exceeding that of an unladen swallow.

    Attributes:
        flight_speed :    The maximum speed that such a bird can attain.
        nesting_grounds  The locale where these birds congregate to reproduce.
    """

    def __init__(self, data: dict):

        self.id: str = data["game"]["id"]
        "A unique identifier for this Game. Example: 'totally-unique-game-id'"

        self.name: str = data["game"]["ruleset"]["name"]
        "Name of the ruleset being used to run this game. Possible values include: standard, solo, royale, squad, constrictor, wrapped. Example: 'standard'"

        self.version: str = data["game"]["ruleset"]["version"]
        "The release version of the Rules module used in this game. Example: 'version': 'v1.2.3'"

        self.timeout: int = data["game"]["timeout"]
        "(milliseconds) - How much time your snake has to respond to requests for this Game. Example: 500"

        self.turn: int = data["turn"]
        "Turn number of the game being played (0 for new games)."

        self.food_spawn_chance: int = data["game"]["ruleset"]["settings"]["foodSpawnChance"]
        "[0-100] - Percentage chance of spawning a new food every round."

        self.minimum_food: int = data["game"]["ruleset"]["settings"]["minimumFood"]
        "Minimum food to keep on the board every turn."

        self.hazard_damage_per_turn: int = data["game"]["ruleset"]["settings"]["hazardDamagePerTurn"]
        "Health damage a snake will take when ending its turn in a hazard. This stacks on top of the regular 1 damage a snake takes per turn."

        self.royale_shrink_every_n_turns: int = data["game"]["ruleset"]["settings"]["royale"]["shrinkEveryNTurns"]
        "In Royale mode, the number of turns between generating new hazards (shrinking the safe board space)."

        self.squad_allow_body_collisions: bool = data["game"]["ruleset"]["settings"]["squad"]["allowBodyCollisions"]
        "In Squad mode, allow members of the same squad to move over each other without dying."

        self.squad_shared_elimination: bool = data["game"]["ruleset"]["settings"]["squad"]["sharedElimination"]
        "In Squad mode, all squad members are eliminated when one is eliminated."

        self.squad_shared_health: bool = data["game"]["ruleset"]["settings"]["squad"]["sharedHealth"]
        "In Squad mode, all squad members share health."

        self.squad_shared_length: bool = data["game"]["ruleset"]["settings"]["squad"]["sharedLength"]
        "In Squad mode, all squad members share length."

        self.source: str = data["game"]["source"]
        "The source of this game, e.g. 'league' or 'custom'. The values for this field may change in the near future."

        self.board_height: int = data["board"]["height"]
        "The number of rows in the y-axis of the game board. Example: 11"

        self.board_width: int = data["board"]["width"]
        "The number of columns in the x-axis of the game board. Example: 11"

        # set food position list
        data_food = data["board"]["food"]
        food: List[Position] = []
        for f in data_food:
            food.append(Position(f["x"], f["y"]))

        self.food: List[Position] = food
        "List of food positions"

        # set hazard position list
        data_hazards = data["board"]["hazards"]
        hazards: List[Position] = []
        for h in data_hazards:
            hazards.append(Position(h["x"], h["y"]))

        self.hazards: List[Position] = hazards
        "List of hazard positions"

        # set snakes
        data_snakes = data["board"]["snakes"]
        snakes: List[Snake] = []
        for data_snake in data_snakes:
            snakes.append(Snake(data_snake))

        self.snakes: List[Snake] = snakes
        "List of all existing snakes"

        self.my_snake: Snake = Snake(data["you"])
        "My snake"

    def print(self):
        print("+++++++++++++++++++++++++++++++++++")
        print(f"Game id : {self.id}")
        print(f"Version : {self.version}")
        print(f"Timeout : {self.timeout}")
        print(f"Turn : {self.turn}")
        print(f"Source : {self.source}")
        print(f"Food spawn chance : {self.food_spawn_chance}")
        print(f"Minimum food : {self.minimum_food}")
        print(f"Hazard damage per turn : {self.hazard_damage_per_turn}")
        print(f"Royal shrink every n turns : {self.royale_shrink_every_n_turns}")
        print(f"Squad allow body collision : {self.squad_allow_body_collisions}")
        print(f"Squad shared elimination : {self.squad_shared_elimination}")
        print(f"Squad shared health : {self.squad_shared_health}")
        print(f"Squad shared length : {self.squad_shared_length}")
        print(f"Board width : {self.board_width}")
        print(f"Board height : {self.board_height}")
        print("--------------------")
        print("## Food positions ##")
        for food_position in self.food:
            print(f"x:{food_position.x} - y:{food_position.y}")
        print("--------------------")
        print("## Hazard positions ##")
        for hazard_position in self.hazards:
            print(f"x:{hazard_position.x} - y:{hazard_position.y}")
        print("--------------------")
        print("## All snakes ##")
        for snake in self.snakes:
            print("--------------------")
            snake.print()
        print("--------------------")
        print("## My snake ##")
        self.my_snake.print()
        print("+++++++++++++++++++++++++++++++++++")
