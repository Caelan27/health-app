from game.entities.creature import Creature


class Player(Creature):
    """
    A subclass of Creature representing the player.

    Attributes:
        - position (tuple[int, int]):
            The player's position
        - on_stats_changed (function):
            The function to be called when the player's stats change


        The following are parallel lists:

        - max_health_decay (list[int]):
            The amount of decay to max health from each consumed item in effect
        - speed_decay (list[int]):
            The amount of decay to speed from each consumed item in effect
        - attack_damage_decay (list[int]):
            The amount of decay to attack dmg from each consumed item in effect
        - decay_duration_left(list[int]):
            How long is left on each consumed item's decay
    """

    def __init__(self, position, **kwargs):
        """
        Initialises the player.

        Args:
            - position (tuple[int, int]):
                The player's initial position
            - **kwargs:
                The keyword arguments for the parent Creature class

        Actions:
            - Sets the player's position
            - Initialises all attributes with empty values
        """
        super().__init__(**kwargs)

        self.position = position

        self.max_health_decay = []

        self.speed_decay = []

        self.attack_damage_decay = []

        self.decay_duration_left = []

    def decay(self):
        """
        Decays the player's stats.

        Actions:
            - Calculates the sum of the decay amounts in each list
            - Removes each stat's decay amount
            - Sets the stat to the higher of calculated amount and a min value
            - Handles the stats being changed

        """
        max_health_decay = sum(self.max_health_decay)
        speed_decay = sum(self.speed_decay)
        attack_damage_decay = sum(self.attack_damage_decay)

        self.max_health = max(self.max_health - max_health_decay, 5)
        self.speed = max(self.speed - speed_decay, 5)
        self.attack_damage = max(self.attack_damage - attack_damage_decay, 2)

        if self.curr_health > self.max_health:
            self.curr_health = self.max_health

    def decay_countdown(self):
        """
        Counts down the decays from each consumed item.

        Actions:
            - Goes through each decay item
            - Removes one from the remaining duration
            - If the duration reaches 0:
                - Remove the entries from each of the decay lists
        """
        for decay_index in range(len(self.decay_duration_left) - 1, -1, -1):
            self.decay_duration_left[decay_index] -= 1

            if self.decay_duration_left[decay_index] <= 0:
                self.decay_duration_left.pop(decay_index)
                self.speed_decay.pop(decay_index)
                self.max_health_decay.pop(decay_index)
                self.attack_damage_decay.pop(decay_index)
