from game.entities.base import Entity


class Creature(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.stats = kwargs.get("stats", {})
        self.sprite = kwargs.get("sprite", None)

        self.base_health = self.stats.get("health", {}).get("base", 10)
        self.base_attack = self.stats.get("attack", {}).get("base", 1)
        self.base_speed = self.stats.get("speed", {}).get("base", 10)

        self.health_scale = self.stats.get("health", {}).get("scale", 0)
        self.attack_scale = self.stats.get("attack", {}).get("scale", 0)
        self.speed_scale = self.stats.get("speed", {}).get("scale", 0)

        self.max_health = self.base_health
        self.curr_health = self.max_health
        self.attack_damage = self.base_attack
        self.speed = self.base_speed

        print(self.sprite)
        print(self.speed)

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
