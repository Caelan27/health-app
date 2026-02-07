from game.entities.base import Entity


class Empty(Entity):
    """
    An entity representing an empty space on the grid.

    Attributes:
        - sprite_name (str):
            The filename of the sprite image

    """

    def __init__(self):
        """
        Initialises the entity.

        Actions:
            - Sets the sprite name
        """
        super().__init__()
        self.sprite = "empty"
