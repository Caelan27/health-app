from game.entities.base import Entity


class Empty(Entity):
    def __init__(self):
        super().__init__()
        self.sprite_name = "empty"
