import json
from game.entities.enemy import Enemy
from game.entities.player import Player
from game.entities.items import Item
from random import choice


class EntityFactory:
    """
    A class that handles the creation of entities.

    Attributes:
        - data (dict[str: dict]):
            Contains the data for each type of entity
    """

    def __init__(self):
        """
        Initialises the EntityFactory

        Actions:
            - Loads the data for enemies, the player, and items
            - Initialises self.data with that data
        """
        enemies = parse_json("enemies.json")
        player = parse_json("player.json")
        items = parse_json("items.json")
        self.data = {"enemies": enemies, "player": player, "items": items}

    def random_enemy(self, position):
        """
        Creates a random enemy at a specific position.

        Actions:
            - Chooses a random enemy type
            - Returns an instance of that enemy at the specified position

        Args:
            - position (tuple[int, int]):
                The position to spawn the enemy at

        Returns:
            - Enemy:
                The enemy that was created
        """
        (enemy_name, enemy_data) = choice(list(self.data["enemies"].items()))
        return self.create_enemy(position, enemy_name)

    def random_item(self):
        """
        Creates a random item

        Actions:
            - Chooses a random item type
            - Returns an instance of that item

        Returns:
            - Item:
                The item that was created
        """
        (item_name, item_data) = choice(list(self.data["items"].items()))
        return self.create_item(item_name)

    def parse_entity_data(self, entity_type, entity_name):
        """
        Gets an entities stats and its sprite.

        Args:
            - entity_type (str):
                The type of entity (e.g. player, enemies, items)
            - entity_name (str):
                The name of the specific entity (e.g. orc, chicken)

        Returns:
            - stats (dict):
                The entities stats
            - sprite (str):
                The filename of the entity's sprite
        """
        entity_data = self.data[entity_type][entity_name]

        stats = entity_data.copy()
        sprite = stats.pop("sprite")

        return (stats, sprite)

    def create_enemy(self, position, enemy_name):
        """
        Creates an instance of a specific enemy.

        Args:
            - position (tuple[int, int]):
                The position to create the enemy at
            - enemy_name (str):
                The type of enemy it is

        Actions:
            - Gets the enemy's stats and sprite
            - Creates an enemy with that data

        Returns:
            - Enemy:
                The enemy that was created
        """
        (stats, sprite) = self.parse_entity_data("enemies", enemy_name)

        return Enemy(position=position, stats=stats, sprite=sprite)

    def create_item(self, item_name):
        """
        Creates an instance of a specific item.

        Args:
            - item_name (str):
                The type of item it is

        Actions:
            - Gets the item's stats and sprite
            - Creates an item with that data

        Returns:
            - Item:
                The item that was created
        """
        (stats, sprite) = self.parse_entity_data("items", item_name)

        return Item(stats=stats, sprite=sprite)

    def create_player(self, position):
        """
        Creates the player entity

        Actions:
            - Gets the player's stats and sprite
            - Creates the player with that data

        Returns:
            - Player:
                The player that was created
        """
        (stats, sprite) = self.parse_entity_data("player", "player")

        return Player(position=position, stats=stats, sprite=sprite)


def parse_json(filename):
    """
    Parses the data in a JSON file.

    Args:
        filename (str):
            The name of the JSON file

    Returns:
        dict:
            The data contained in the JSON file.
    """
    path = "game/data/" + filename
    with open(path, "r") as json_file:
        return json.load(json_file)
