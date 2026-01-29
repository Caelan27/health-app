from game.entities.creature import Creature


class Player(Creature):
    def __init__(self, position):
        super().__init__(10, 10, 1, 2)
        self.position = position
        self.sprite_name = "player"

    def take_turn(self):
        print("Player taking turn")
