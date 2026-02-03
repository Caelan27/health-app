from game.entities.creature import Creature


class Player(Creature):
    def __init__(self, position, **kwargs):
        super().__init__(**kwargs)

        self.position = position
        self.on_stats_changed = None

        self.max_health_decay = []

        self.speed_decay = []

        self.attack_damage_decay = []

        self.decay_duration_left = []

    def decay(self):
        max_health_decay = sum(self.max_health_decay)
        speed_decay = sum(self.speed_decay)
        attack_damage_decay = sum(self.attack_damage_decay)

        print(max_health_decay, speed_decay,
              attack_damage_decay, self.decay_duration_left)

        new_max_health = self.max_health - max_health_decay

        if new_max_health <= 5:
            new_max_health = 5

        self.max_health = new_max_health

        if self.curr_health > self.max_health:
            self.curr_health = self.max_health

        new_speed = self.speed - speed_decay

        if new_speed <= 5:
            new_speed = 5

        self.speed = new_speed

        new_attack_damage = self.attack_damage - attack_damage_decay

        if new_attack_damage <= 2:
            new_attack_damage = 2

        self.attack_damage = new_attack_damage
        self.on_stats_changed()

    def decay_countdown(self):
        for decay_index in range(len(self.decay_duration_left) - 1, -1, -1):
            self.decay_duration_left[decay_index] -= 1

            if self.decay_duration_left[decay_index] <= 0:
                self.decay_duration_left.pop(decay_index)
                self.speed_decay.pop(decay_index)
                self.max_health_decay.pop(decay_index)
                self.attack_damage_decay.pop(decay_index)

    def take_turn(self):
        print("Player taking turn")

    def take_damage(self, amount):
        super().take_damage(amount)
        if self.on_stats_changed:
            self.on_stats_changed()

    def heal(self, amount):
        super().heal(amount)
        if self.on_stats_changed:
            self.on_stats_changed()
