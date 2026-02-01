from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from game.ui.ui import GameGrid


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        boxlayout = BoxLayout(orientation="vertical",
                              spacing=30,
                              padding=[20, 20, 20, 20])

        home_button = Button(text="Home", size_hint_x=0.2, size_hint_y=0.15)
        home_button.bind(on_release=self._go_home)

        boxlayout.add_widget(home_button)

        self.gridlayout = GameGrid()

        health = self.gridlayout.game_state.player_health

        self.health_label = Label(text=str(health), size_hint_y=0.05)

        self.health_label.text = "Health: " + \
            str(self.gridlayout.game_state.player_health)

        self.gridlayout.game_state.bind(
            player_health=self._update_health_label)

        self.gridlayout.game_state.bind(
            game_over=self.display_game_over_screen)

        boxlayout.add_widget(self.health_label)

        boxlayout.add_widget(self.gridlayout)

        self.add_widget(boxlayout)

    def _update_health_label(self, instance, value):
        self.health_label.text = "Health: " + str(value)

    def display_game_over_screen(self, instance, value):
        if self.gridlayout.game_state.game_over:
            self.clear_widgets()
            game_over_label = Label(text="Game Over!")
            self.add_widget(game_over_label)

    def button_press_reaction(self, button):
        self.move_player(button)
        self.display_grid()

    def _go_home(self, *args):
        """Moves to the homepage."""
        self.manager.current = "HomeScreen"
