from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from game.ui.grid import GameGrid
from kivy.core.audio import SoundLoader


class GameScreen(Screen):
    """
    A subclass of Screen for the app's game

    Attributes:
        - gridlayout (GridLayout):
            The game grid UI

        - health_label (Label):
            The label displaying the player's health
        - speed_label (Label):
            The label displaying the player's speed
        - attack_damage_label (Label):
            The label displaying the player's attack damage
        - score_label (Label):
            The label displaying the player's score

        - game_over_sound (Sound):
            The sound to play when the game ends
    """

    game_over_sound = SoundLoader.load("game/audio/game_over.wav")

    def __init__(self, **kwargs):
        """
        Initialises the game screen.

        Args:
            - **kwargs:
                Keyword arguments for the parent Screen class

        Actions:
            - Initialises the gridlayout and labels with empty values
            - Starts the game
        """
        super().__init__(**kwargs)

        self.gridlayout = None

        self.health_label = None
        self.speed_label = None
        self.attack_damage_label = None
        self.score_label = None

        self.start_game()

    def update_labels(self, *args):
        """
        Updates the text on all the stat labels

        Actions:
            - Goes through each label, updating their text
        """
        curr_health = self.gridlayout.game_state.player.curr_health
        max_health = self.gridlayout.game_state.player.max_health
        self.health_label.text = f"Health: {curr_health} / {max_health}"

        score = self.gridlayout.game_state.score
        self.score_label.text = f"Score: {score}"

        attack_damage = self.gridlayout.game_state.player.attack_damage
        self.attack_damage_label.text = f"Attack damage: {attack_damage}"

        speed = self.gridlayout.game_state.player.speed
        self.speed_label.text = f"Speed: {speed}"

    def display_game_over_screen(self, instance, value):
        """
        Displays the game over screen.

        Actions:
            - Plays the game over sound effect
            - Clears all widgets from the screen
            - Creates a box layout
            - Adds a button to return to the home screen
            - Adds a label saying "Game Over!"
            - Adds a label showing the player's score
            - Adds a button to restart the game
            - Adds the box layout to the screen
        """
        if not self.gridlayout.game_state.player.is_alive:
            self.game_over_sound.play()

            self.clear_widgets()

            boxlayout = BoxLayout(orientation="vertical",
                                  spacing=30,
                                  padding=[20, 20, 20, 20])

            home_button = Button(
                text="Home", size_hint_x=0.2, size_hint_y=0.15)
            home_button.bind(on_release=self._go_home)
            boxlayout.add_widget(home_button)

            game_over_label = Label(text="Game Over!")
            boxlayout.add_widget(game_over_label)

            score_label = Label(text="Your score was: " +
                                str(self.gridlayout.game_state.score))
            boxlayout.add_widget(score_label)

            play_again_button = Button(text="Play again", size_hint_y=0.3)
            play_again_button.bind(on_release=self.start_game)

            boxlayout.add_widget(play_again_button)

            self.add_widget(boxlayout)

    def start_game(self, *args):
        """
        Starts the game.

        Actions:
            - Clears the screen
            - Creates a box layout
            - Adds a home button
            - Creates a GameGrid
            - Creates labels for the player's stats
            - Binds the stats changing to updating the labels
            - Binds the player dying to displaying game over screen
        """
        self.clear_widgets()

        boxlayout = BoxLayout(orientation="vertical",
                              spacing=30,
                              padding=[20, 20, 20, 20])

        home_button = Button(text="Home", size_hint_x=0.2, size_hint_y=0.15)
        home_button.bind(on_release=self._go_home)

        boxlayout.add_widget(home_button)

        self.gridlayout = GameGrid(5, 5)

        stat_label_size_hint_y = 0.02

        self.health_label = Label(size_hint_y=stat_label_size_hint_y)
        self.attack_damage_label = Label(size_hint_y=stat_label_size_hint_y)
        self.speed_label = Label(size_hint_y=stat_label_size_hint_y)
        self.score_label = Label(size_hint_y=stat_label_size_hint_y)
        self.update_labels()

        self.gridlayout.game_state.player.bind(
            attack_damage=self.update_labels,
            speed=self.update_labels,
            max_health=self.update_labels,
            curr_health=self.update_labels,
            is_alive=self.display_game_over_screen
        )

        self.gridlayout.game_state.bind(score=self.update_labels)

        boxlayout.add_widget(self.health_label)
        boxlayout.add_widget(self.speed_label)
        boxlayout.add_widget(self.attack_damage_label)
        boxlayout.add_widget(self.score_label)

        boxlayout.add_widget(self.gridlayout)

        self.add_widget(boxlayout)

    def _go_home(self, *args):
        """Moves to the homepage."""
        self.manager.current = "HomeScreen"
