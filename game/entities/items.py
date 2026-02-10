from game.entities.base import Entity


class Item(Entity):
    """
    An entity representing a consumable item.

    Attributes:
        - sprite (str):
            The filename of the sprite image

        - max_health_boost (int):
            The amount it adds to the player's max health
        - max_health_decay (int):
            The amount it removes from the player's max health each turn

        - speed_boost (int):
            The amount it adds to the player's speed
        - speed_decay (int):
            The amount it removes from the player's speed each turn

        - attack_boost (int):
            The amount it adds to the player's attack damage
        - attack_decay (int):
            The amount it removes from the player's attack damage each turn

        - score_boost (int):
            The amount it adds to the player's score

        - curr_health_boost (int):
            The amount it adds to the player's current health

        - decay_duration (int):
            The number of turns it takes for the decay to wear off
    """

    def __init__(self, **kwargs):
        """
        Initialises the item.

        Args:
            - **kwargs:
                - stats:
                    The item's stats
                - sprite:
                    The item's sprite name
        """
        super().__init__()
        stats = kwargs["stats"]
        self.sprite = kwargs["sprite"]

        self.max_health_boost = stats["max_health"]["boost"]
        self.max_health_decay = stats["max_health"]["decay"]

        self.speed_boost = stats["speed"]["boost"]
        self.speed_decay = stats["speed"]["decay"]

        self.attack_boost = stats["attack"]["boost"]
        self.attack_decay = stats["attack"]["decay"]

        self.score_boost = stats["score_boost"]

        self.curr_health_boost = stats["curr_health_boost"]

        self.decay_duration = stats["decay_duration"]


class Food(Item):
    """
    A subclass of Item representing an item of food.
    """

    def __init__(self):
        super().__init__()
