import threading
import server_logic
from logic import constrictor
from logic import royale
from logic import squad
from logic import standard
from logic.wrapped import wrapped
from threading import Thread
from classes.GameData import GameData
from flask import request
from flask import Flask
import time
import logging
import os

import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


app = Flask(__name__)


@app.get("/")
def handle_info():
    """
    This function is called when you register your Battlesnake on play.battlesnake.com
    See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake

    It controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    print("INFO")
    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#ff00ff",  # TODO: Personalize
        "head": "default",  # TODO: Personalize
        "tail": "default",  # TODO: Personalize
    }


@app.post("/start")
def handle_start():
    """
    This function is called everytime your snake is entered into a game.
    request.json contains information about the game that's about to be played.
    """
    data = request.get_json()
    gamedata = GameData(data)

    # prepare wrapped game
    wrapped.prepare(gamedata)

    # gamedata.get_f
    print(f"{data['game']['id']} START")
    return "ok"


@app.post("/move")
def handle_move():
    """
    This function is called on every turn of a game. It's how your snake decides where to move.
    Valid moves are "up", "down", "left", or "right".
    """
    data = request.get_json()
    gamedata = GameData(data)

    # move = ""

    # if gamedata.is_royale_mode():
    #     move = royale.handle_move(gamedata)
    # elif gamedata.is_constrictor_mode():
    #     move = constrictor.handle_move(gamedata)
    # elif gamedata.is_wrapped_mode():
    #     move = wrapped.handle_move(gamedata)
    # elif gamedata.is_squad_mode():
    #     move = squad.handle_move(gamedata)
    # else:
    #     move = standard.handle_move(gamedata)
    # gamedata.print()
    move = wrapped.handle_move(gamedata)
    print(f"move turn : {gamedata.get_turn()}")

    # TODO - look at the server_logic.py file to see how we decide what move to return!
    # move = server_logic.choose_move(data)

    return {"move": move}


@app.post("/end")
def end():
    """
    This function is called when a game your snake was in ends.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = request.get_json()
    gamedata = GameData(data)

    wrapped.handle_end(gamedata)

    # handle end (e.g. wrapped.handle_end(gamedata))

    print(f"{data['game']['id']} END")
    # print(data)
    print("----------------------------")
    print("----------------------------")
    return "ok"


@app.after_request
def identify_server(response):
    response.headers["Server"] = "BattlesnakeOfficial/starter-snake-python"
    return response


def keep_alive():
    server = Thread(target=run)
    server.start()


def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print("Starting Battlesnake Server...")

    home = True

    if home:
        port = int(os.environ.get("PORT", "8080"))
        app.run(host="0.0.0.0", port=port, debug=True)
    else:
        keep_alive()
