from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from game.core.game_state import GameState
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.entities.empty import Empty
from game.entities.items import Item


class GameGrid(GridLayout):
    def __init__(self, *kwargs):
        super().__init__()
        self.cols = 5

        self.game_state = GameState(5, 5)
        self.game_state.initialise_grid()
        self._draw()

    def _draw(self):
        self.clear_widgets()

        grid = self.game_state.grid

        for (y, row) in enumerate(grid):
            for (x, tile) in enumerate(row):
                entity = tile.entity

                button = Button()
                button.grid_position = (x, y)
                button.bind(on_release=self._interact_with_tile)

                if isinstance(entity, Player):
                    button.background_color = (1, 0, 0, 1)
                elif isinstance(entity, Empty):
                    button.background_color = (0, 1, 0, 1)
                elif isinstance(entity, Item):
                    button.background_color = (0, 0, 1, 1)
                elif isinstance(entity, Enemy):
                    button.background_color = (1, 1, 0, 1)

                self.add_widget(button)

    def _interact_with_tile(self, button):
        self.game_state.interact_with_tile(button.grid_position)
        self.game_state.refresh_grid()

        self._draw()
