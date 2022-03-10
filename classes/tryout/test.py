

from typing import List
from classes.tryout.Gamedata import Gamedata
from classes.tryout.Position import Position
from classes.tryout.TestRequestBody import testdata1
from classes.tryout.simulation.Moverequest import Moverequest
from classes.tryout.simulation.Simulator import wrapped_spiral_simulator

data = testdata1

gamedata = Gamedata(data)

moverequests: List[Moverequest] = []

for snake in gamedata.snakes:
    moverequests.append(Moverequest(snake.id, "up"))

gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata.hazards.append(Position(5, 5))
gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata = wrapped_spiral_simulator(gamedata, moverequests)

moverequests: List[Moverequest] = []
for snake in gamedata.snakes:
    moverequests.append(Moverequest(snake.id, "right"))

gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata = wrapped_spiral_simulator(gamedata, moverequests)
gamedata = wrapped_spiral_simulator(gamedata, moverequests)

gamedata.print()
