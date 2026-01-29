from game.entities.creature import Creature


class Enemy(Creature):
    def __init__(self, position):
        super().__init__(10, 10, 1, 6)
        self.position = position
        self.sprite_name = "enemy"

    def handle_death(self):
        super().handle_death()

    def take_turn(self):
        print("Enemy taking turn")
