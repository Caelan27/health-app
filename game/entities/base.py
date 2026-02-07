from kivy.event import EventDispatcher


class Entity(EventDispatcher):
    """
    An object (e.g. an enemy or an item) in the game
    """

    def __init__(self):
        super().__init__()
        pass
