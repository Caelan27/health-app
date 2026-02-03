import os
import json
from game.entities.enemy import Enemy
from game.entities.player import Player
from random import choice

CURRENT_DIR = os.path.dirname(__file__)


class EntityFactory:
    def __init__(self):
        enemies = parse_json("enemies.json")
        player = parse_json("player.json")
        # items = parse_json("data/items.json") -- not yet implemented
        self.data = {"enemies": enemies, "player": player}

    def random_enemy(self, position):
        (enemy_name, enemy_data) = choice(list(self.data["enemies"].items()))
        return self.create_enemy(position, enemy_name)

    def create_enemy(self, position, enemy_name):
        enemy_data = self.data["enemies"][enemy_name]

        stats = enemy_data.copy()
        sprite = stats.pop("sprite")

        enemy = Enemy(position=position, stats=stats, sprite=sprite)

        return enemy

    def create_item(self, item_name):
        # TODO: Make this method
        pass

    def create_player(self, position):
        player_data = self.data["player"]["player"]

        stats = player_data.copy()
        print(stats)
        sprite = stats.pop("sprite")

        player = Player(position=position, stats=stats, sprite=sprite)

        return player


def parse_json(filename):
    """
    Parses the data in a JSON file.

    Args:
        file_path (str):
            The path to the JSON file.

    Returns:
        dict:
            The data contained in the JSON file.
    """
    path = os.path.join(CURRENT_DIR, "../data", filename)
    with open(path, "r") as json_file:
        return json.load(json_file)
