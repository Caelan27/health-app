from game.entities.base import Entity


class Item(Entity):
    def __init__(self):
        super().__init__()


class Food(Item):
    def __init__(self):
        super().__init__()


class HealthyFood(Food):
    def __init__(self):
        super().__init__()


class UnhealthyFood(Food):
    def __init__(self):
        super().__init__()
