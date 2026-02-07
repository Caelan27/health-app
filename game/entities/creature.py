from game.entities.base import Entity
from game.helpers import is_adjacent


class Creature(Entity):
    """
    An animal-like entity capable of taking damage, dealing damage and moving

    Attributes:
        - base_health (int):
            The creature's max health with no modifiers
        - base_damage (int):
            The creature's attack damage with no modifiers
        - base_speed (int):
            The creature's speed with no modifiers

        - health_scale (float):
            The amount of max health gained for each point of score
        - attack_scale (float):
            The amount of attack damage gained for each point of score
        - speed_scale (float):
            The amount of speed gained for each point of score

        - max_health (int):
            The creature's maximum health with modifiers applied
        - curr_health (int):
            The amount of health the creature currently has
        - attack_damage (int):
            The creature's attack damage with modifiers applied
        - speed (int):
            The creature's speed with modifiers applied

        - is_alive (boolean):
            Whether or not the player is alive
        - turn_meter (int):
            Measures how close the creature is to having their turn
    """

    def __init__(self, **kwargs):
        """
        Initialises the creature.

        Args:
            - **kwargs:
                - stats (dict):
                    The creature's stats
                - sprite (str):
                    The filename of the creature's sprite

        Actions:
            - Sets all of the creature's properties
        """
        super().__init__()
        stats = kwargs.get("stats", {})

        self.sprite = kwargs.get("sprite", "")

        self.base_health = stats.get("health", {}).get("base", 10)
        self.base_attack = stats.get("attack", {}).get("base", 1)
        self.base_speed = stats.get("speed", {}).get("base", 10)

        self.health_scale = stats.get("health", {}).get("scale", 0)
        self.attack_scale = stats.get("attack", {}).get("scale", 0)
        self.speed_scale = stats.get("speed", {}).get("scale", 0)

        self.max_health = self.base_health
        self.curr_health = self.max_health
        self.attack_damage = self.base_attack
        self.speed = self.base_speed

        self.is_alive = True
        self.turn_meter = 0

    def attack_creature(self, target):
        """
        Attacks a creature.

        Args:
            - target (Creature):
                The creature to attack

        Actions:
            - Checks the target is close enough and not this creature
            - Makes the target take damage

        Returns:
            - boolean:
                True if the target was successfully attacked
                False if not
        """
        (creature_x, creature_y) = target.position

        if (is_adjacent(self.position, target.position)
                and self.position != target.position):
            target.take_damage(self.attack_damage)

            return True
        else:
            return False

    def take_damage(self, amount):
        """
        Takes damage.

        Args:
            - amount (int):
                The amount of damage to take

        Actions:
            - Remove the specified amount from the current health
            - If the current health is below 0, handle the creature's death
        """
        self.curr_health -= amount
        if self.curr_health <= 0:
            self.handle_death()

    def heal(self, amount):
        """
        Heals damage.

        Args:
            - amount (int):
                The amount of health to be healed

        Actions:
            - Sets the current health to the lower of:
                - The current health plus the amount to heal
                - The creature's max health
        """
        self.curr_health = min(self.curr_health + amount, self.max_health)

    def handle_death(self):
        """
        Handles the creature's death.

        Actions:
            - Set is_alive to False
        """
        self.is_alive = False
