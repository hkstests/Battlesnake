import string
from typing import List


class Snake:
    def __init__(self, snake):
        self._snake = snake

    def get_id(self) -> string:
        """
            Unique identifier for this Battlesnake in the context of the current Game.
            Example: "totally-unique-snake-id"
        """
        return self._snake["id"]

    def get_health(self) -> int:
        """
            Health value of this Battlesnake, between 0 and 100 inclusively.
            Example: 54
        """
        return self._snake["health"]

    def get_body_positions(self) -> List[dict]:
        """
            Array of coordinates representing this Battlesnake's location on the game board. This array is ordered from head to tail.
            Example: [{"x": 0, "y": 0}, ..., {"x": 2, "y": 0}]
        """
        return self._snake["body"]

    def get_head_position(self) -> dict:
        """
            Coordinates for this Battlesnake's head. Equivalent to the first element of the body array.
            Example: {"x": 0, "y": 0}
        """
        return self._snake["head"]

    def get_direction(self) -> string:
        body_positions = self.get_body_positions()
        head = body_positions[0]
        neck = body_positions[1]

        if head["y"] == neck["y"]:
            if abs(head["x"] - neck["x"]) > 1:
                # snake is moving to the left (through the wall (e.g. in wrapped mode))
                if head["x"] > neck["x"]:
                    return "left"
                return "right"
            # else jsut follow the dir
            if head["x"] > neck["x"]:
                return "right"
            return "left"
        else:  # x must be equal
            if abs(head["y"] - neck["y"]) > 1:
                # snake is moving down (through the wall (e.g. in wrapped mode))
                if head["y"] > neck["y"]:
                    return "down"
                return "up"
            # else jsut follow the dir
            if head["y"] > neck["y"]:
                return "up"
            return "down"

    def get_squad(self) -> string:
        """
            The squad that the Battlesnake belongs to. Used to identify squad members in Squad Mode games.
            Example: "1"
        """
        return self._snake["squad"]

    def print(self, snake_type):
        print(f"{snake_type} id {self.get_id()}")
        print(f"{snake_type} squad {self.get_squad()}")
        print(f"{snake_type} health {self.get_health()}")
        print(
            f"{snake_type} head position {self.get_head_position()}")
        print(
            f"{snake_type} body positions {self.get_body_positions()}")
