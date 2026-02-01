from game.entities.base import Entity


class Creature(Entity):
    def __init__(self, curr_health, max_health, attack_damage, speed):
        super().__init__()
        self.curr_health = curr_health
        self.max_health = max_health
        self.attack_damage = attack_damage
        self.speed = speed
        self.is_alive = True
        self.turn_meter = 0

    def deal_damage(self, target):
        target.take_damage(self.attack_damage)

    def take_damage(self, amount):
        self.curr_health -= amount
        if self.curr_health <= 0:
            self.curr_health = 0
            self.handle_death()

    def heal(self, amount):
        self.curr_health += amount
        if self.curr_health > self.max_health:
            self.curr_health = self.max_health

    def is_alive(self):
        return self.curr_health > 0

    def handle_death(self):
        self.is_alive = False
