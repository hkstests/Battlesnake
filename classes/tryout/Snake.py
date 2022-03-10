
from typing import List

from classes.tryout.Position import Position


class Snake:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        "Unique identifier for this Battlesnake in the context of the current Game. Example: 'totally-unique-snake-id'"

        self.name: str = data["name"]
        "Name given to this Battlesnake by its author.Example: 'Sneky McSnek Face'"

        self.health: int = data["health"]
        "Health value of this Battlesnake, between 0 and 100 inclusively. Example: 54"

        self.body: List[Position] = []
        "Array of positions representing this Battlesnake's location on the game board. This array is ordered from head to tail."

        for p in data["body"]:
            self.body.append(Position(p["x"], p["y"]))

        self.latency: str = data["latency"]
        "The previous response time of this Battlesnake, in milliseconds. '0' means the Battlesnake timed out and failed to respond. Example: '450'"

        self.head: Position = Position(data["head"]["x"], data["head"]["y"])
        "Position for this Battlesnake's head. Equivalent to the first element of the body array."

        self.length: int = data["length"]
        "Length of this Battlesnake from head to tail. Equivalent to the length of the body array. Example: 3"

        self.shout: str = data["shout"]
        "Message shouted by this Battlesnake on the previous turn. Example: 'why are we shouting??'"

        self.squad: str = data["squad"]
        "The squad that the Battlesnake belongs to. Used to identify squad members in Squad Mode games. Example: '1'"

        self.color: str = data["customizations"]["color"]
        "Hex color code used to display this Battlesnake. Must start with '#' and be 7 characters long. Example: '#888888'"

        self.headstyle: str = data["customizations"]["head"]
        "Displayed head of this Battlesnake. See Personalization Docs for available options Example: 'default'"

        self.tailstyle: str = data["customizations"]["tail"]
        "Displayed tail of this Battlesnake. See Personalization Docs for available options. Example: 'default'"

    def print(self):
        print(f"Id : {self.id}")
        print(f"Name : {self.name}")
        print(f"Health : {self.health}")
        print(f"Latency : {self.latency}")
        print(f"Shout : {self.shout}")
        print(f"Squad : {self.squad}")
        print(f"Color : {self.color}")
        print(f"Headstyle : {self.headstyle}")
        print(f"Tailstyle : {self.tailstyle}")
        print(f"Head position : x:{self.head.x} - y:{self.head.y}")
        print(f"Body positions : ")
        for body_position in self.body:
            print(f"x:{body_position.x} - y:{body_position.y}")
