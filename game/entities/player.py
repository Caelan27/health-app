from game.entities.creature import Creature


class Player(Creature):
    def __init__(self, position, **kwargs):
        super().__init__(**kwargs)

        self.position = position
        self.on_health_changed = None

    def take_turn(self):
        print("Player taking turn")

    def take_damage(self, amount):
        super().take_damage(amount)
        if self.on_health_changed:
            self.on_health_changed()

    def heal(self, amount):
        super().heal(amount)
        if self.on_health_changed:
            self.on_health_changed()
