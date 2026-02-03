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

        curr_health = self.gridlayout.game_state.curr_player_health
        max_health = self.gridlayout.game_state.max_player_health

        stat_label_size_hint_y = 0.02

        self.health_label = Label(
            text=f"Health: {curr_health} / {max_health}", size_hint_y=stat_label_size_hint_y)

        self.gridlayout.game_state.bind(
            curr_player_health=self._update_health_label)

        self.gridlayout.game_state.bind(
            max_player_health=self._update_health_label)

        speed = self.gridlayout.game_state.player_speed
        self.speed_label = Label(
            text=f"Speed: {speed}", size_hint_y=stat_label_size_hint_y)

        self.gridlayout.game_state.bind(
            player_speed=self._update_speed_label)

        attack_damage = self.gridlayout.game_state.player_attack_damage
        self.attack_damage_label = Label(
            text=f"Attack damage: {attack_damage}", size_hint_y=stat_label_size_hint_y)

        self.gridlayout.game_state.bind(
            player_attack_damage=self._update_attack_damage_label)

        self.gridlayout.game_state.bind(
            game_over=self.display_game_over_screen)

        score = self.gridlayout.game_state.score
        self.score_label = Label(
            text=f"Score: {score}", size_hint_y=stat_label_size_hint_y)

        self.gridlayout.game_state.bind(
            score=self._update_score_label)

        boxlayout.add_widget(self.health_label)
        boxlayout.add_widget(self.speed_label)
        boxlayout.add_widget(self.attack_damage_label)
        boxlayout.add_widget(self.score_label)

        boxlayout.add_widget(self.gridlayout)

        self.add_widget(boxlayout)

    def _update_health_label(self, instance, value):
        curr_health = self.gridlayout.game_state.curr_player_health
        max_health = self.gridlayout.game_state.max_player_health

        self.health_label.text = f"Health: {curr_health} / {max_health}"

    def _update_score_label(self, instance, value):
        score = self.gridlayout.game_state.score

        self.score_label.text = f"Score: {score}"

    def _update_attack_damage_label(self, instance, value):
        attack_damage = self.gridlayout.game_state.player_attack_damage

        self.attack_damage_label.text = f"Attack damage: {attack_damage}"

    def _update_speed_label(self, instance, value):
        speed = self.gridlayout.game_state.player_speed

        self.speed_label.text = f"Speed: {speed}"

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
