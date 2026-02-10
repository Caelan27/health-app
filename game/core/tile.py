class Tile:
    """
    A space on the game grid that can contain an entity

    Attributes:
        - entity (Entity):
            The entity taking up the tile
    """

    def __init__(self, entity):
        self.entity = entity
