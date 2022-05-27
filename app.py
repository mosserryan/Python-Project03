#!/usr/bin/python3

import json
from unicodedata import name
from flask import Flask, jsonify
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
import requests
import character

app = Flask(__name__)

game = {
    "gameover": False,
    "turn": 1,
    "player": {},
    "validMoves": [],
    "validItem": None,
    "lastAction": "Game Started!",
    "playerInventory": [],
    "currentRoom": 'Hall',
    "rooms": {
        'Hall': {
            'south': 'Kitchen',
            'east': 'Dining Room',
            'west': 'Basement',
            'monster': False
        },
        'Kitchen': {
            'north': 'Hall',
            'items' : "",
            'monster': True,
        },
        'Dining Room': {
            'west': 'Hall',
            'south': 'Garden',
            'north': 'Pantry',
            'items': 'potion',
            'monster': False
            
        },
        'Garden': {
            'north': 'Dining Room',
            'items': 'sword',
            'monster': False
        },
        'Pantry': {
            'south': 'Dining Room',
            'items': 'cookie',
            'monster': False
        },
        'Basement': {
            'items': 'Treasure'
        }
    }
}

@app.route("/gamedata", methods=["GET", "POST"])
def jsondata():
    if request.method == 'POST':
        data = request.json
        if data:
            data = json.loads(data)
            global game
            game = data    

    return redirect(url_for("start"))

@app.route("/DungeonBunkers/<name>/<race>/<profession>/<strength>/<intelligence>/<stamina>/")
def play(name, race, profession, strength, intelligence, stamina):
    validMoves = game['rooms'][game['currentRoom']]
    return render_template("game.html", name=name, race=race, profession=profession, strength=strength, intelligence=intelligence, stamina=stamina, **validMoves, inventory=game["playerInventory"], currentRoom=game["currentRoom"], turn=game["turn"], lastAction=game["lastAction"])

@app.route("/")
def start():
    return render_template("create_character.html")

@app.route("/create", methods=["POST"])
def createCharacter():
    if request.method == "POST":
        if request.form:
            name = request.form["name"]
            race = request.form["race"]
            profession = request.form["profession"]
            player = character.create(name, race, profession)
            game['player'] = player
            return redirect(url_for("play", name=player.name, race=player.race, profession=player.profession, strength=player.stats['strength'], intelligence=player.stats['intelligence'], stamina=player.stats['stamina']))

@app.route("/action", methods=["POST"])
def action():
    currentRoom = game['currentRoom']
    if request.method == "POST":
        print(request.form)
        if request.form.get("north"):
            direction = request.form.get("north")
            if direction == "north":
                game['currentRoom'] = game['rooms'][currentRoom]["north"]
                game['turn'] += 1
                game['lastAction'] = f"You go {direction} into the {game['currentRoom']}"
        elif request.form.get("east"):
            direction = request.form.get("east")
            if direction == "east":
                game["currentRoom"] = game['rooms'][currentRoom]["east"]
                game['turn'] += 1
                game['lastAction'] = f"You go {direction} into the {game['currentRoom']}"
        elif request.form.get("south"):
            direction = request.form.get("south")
            if direction == "south":
                game["currentRoom"] = game['rooms'][currentRoom]["south"]
                game['turn'] += 1
                game['lastAction'] = f"You go {direction} into the {game['currentRoom']}"
        elif request.form.get("west"):
            direction = request.form.get("west")
            if direction == "west":
                if(game["currentRoom"] == 'Hall' and 'key' in game['playerInventory']):
                    game["currentRoom"] = game['rooms'][currentRoom]["west"]
                    game['turn'] += 1
                    game['lastAction'] = f"You go {direction} into the {game['currentRoom']}, you find a treasure chest. Use the key!"
                elif(game["currentRoom"] == 'Hall' and 'key' not in game['playerInventory']):
                    game['lastAction'] = f"You try to {direction} but the door is locked. Looks like you need to find a key!"
                else:
                    game["currentRoom"] = game['rooms'][currentRoom]["west"]
                    game['turn'] += 1
                    game['lastAction'] = f"You go {direction} into the {game['currentRoom']}"
        elif request.form.get("getItem"):
            game['playerInventory'].append(game['rooms'][currentRoom]['items'])
            game['lastAction'] = f"You pick up a {game['rooms'][currentRoom]['items']}"
            game['turn'] += 1
            del game['rooms'][currentRoom]['items']
        elif request.form.get("attack"):
            if(game["rooms"][currentRoom]['monster'] == True):
                if("sword" in game['playerInventory']):
                    game['lastAction'] = f"Swing your sword at the Monster! The monster has been defeated! The monster dropped a key!"
                    game['rooms'][currentRoom]['items'] = 'key'
                    game["rooms"][currentRoom]['monster'] = False
                    game['turn'] += 1
                else:
                    game['lastAction'] = f"Swing your fists at the Monster! That was embarassing, the monster one shots you, you are D E D ded. GAME OVER."
                    game['gameover'] = True
            else:
                game['lastAction'] = f"There is nothing to attack in this room."
                game['turn'] += 1
        elif request.form.get("reset"):
            resetGame()
        return redirect(url_for("play", name=game["player"].name, race=game["player"].race, profession=game["player"].profession, strength=game["player"].stats['strength'], intelligence=game["player"].stats['intelligence'], stamina=game["player"].stats['stamina']))

def resetGame():
    URL= "http://127.0.0.1:2224/gamedata"
    game = {
    "gameover": False,
    "turn": 1,
    "player": {},
    "validMoves": [],
    "validItem": None,
    "lastAction": "Game Started!",
    "playerInventory": [],
    "currentRoom": 'Hall',
    "rooms": {
        'Hall': {
            'south': 'Kitchen',
            'east': 'Dining Room',
            'west': 'Basement',
            'monster': False
        },
        'Kitchen': {
            'north': 'Hall',
            'items' : "",
            'monster': True,
        },
        'Dining Room': {
            'west': 'Hall',
            'south': 'Garden',
            'north': 'Pantry',
            'items': 'potion',
            'monster': False
            
        },
        'Garden': {
            'north': 'Dining Room',
            'items': 'sword',
            'monster': False
        },
        'Pantry': {
            'south': 'Dining Room',
            'items': 'cookie',
            'monster': False
        },
        'Basement': {
            'items': 'Treasure'
        }
    }
}
    game = json.dumps(game)
    requests.post(URL, json=game)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=2224)  # runs the application


