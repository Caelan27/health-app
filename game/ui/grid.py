from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from game.core.game_state import GameState


class GameGrid(GridLayout):
    """
    A subclass of GridLayout in charge of drawing the game grid

    Attributes:
        - game_state (GameState):
            The current game state
    """

    def __init__(self, width, height):
        """
        Initialises the grid.

        Args:
            - width (int):
                The number of columns in the grid
            - height (int):
                The number of rows in the grid

        Actions:
            - Initialises the GridLayout with the right number of columns
            - Creates the game state
            - Draws the grid
        """
        super().__init__(cols=width)

        self.game_state = GameState(width, height)
        self.draw()

    def draw(self):
        """
        Draws the grid on the screen.

        Actions:
            - Clears all widgets from the screen.
            - Goes through each tile in the grid:
                - Creates a button bound to self.interact_with_tile function
                - If the tile is empty, keep the default button background
                - If the tile is not empty, set its background to sprite image
                - Add the button the GridLayout
        """
        self.clear_widgets()

        grid = self.game_state.grid

        for (y, row) in enumerate(grid):
            for (x, tile) in enumerate(row):
                entity = tile.entity

                button = Button()
                button.grid_position = (x, y)
                button.bind(on_release=self.interact_with_tile)

                if entity.sprite != "empty":
                    button.background_normal = "game/img/" + entity.sprite
                    button.background_down = "game/img/" + entity.sprite

                self.add_widget(button)

    def interact_with_tile(self, button):
        """
        Handles the player interacting with a tile.

        Args:
            - button (Button):
                The button representing the tile interacted with

        Actions:
            - Calls the game state logic to interact with the tile
            - Removes dead entities
            - Redraws the screen
        """
        self.game_state.interact_with_tile(button.grid_position)
        self.game_state.remove_dead()

        self.draw()
