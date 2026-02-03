from game.entities.base import Entity


class Item(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.stats = kwargs["stats"]
        self.sprite = kwargs["sprite"]

        self.max_health_boost = self.stats["max_health"]["boost"]
        self.max_health_decay = self.stats["max_health"]["decay"]

        self.speed_boost = self.stats["speed"]["boost"]
        self.speed_decay = self.stats["speed"]["decay"]

        self.attack_boost = self.stats["attack"]["boost"]
        self.attack_decay = self.stats["attack"]["decay"]

        self.score_boost = self.stats["score_boost"]

        self.curr_health_boost = self.stats["curr_health_boost"]
        self.decay_duration = self.stats["decay_duration"]

        print(self.sprite)


class Food(Item):
    def __init__(self):
        super().__init__()


class HealthyFood(Food):
    def __init__(self):
        super().__init__()


class UnhealthyFood(Food):
    def __init__(self):
        super().__init__()
