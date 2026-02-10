from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from game.ui.screen import GameScreen
from screens.home import HomeScreen
from screens.info import InfoScreen
from screens.quiz import QuizScreen


class HealthApp(App):
    def build(self):
        screen_manager = ScreenManager()

        # Adds screens to screen manager
        info_screen = InfoScreen(name="InfoScreen")
        screen_manager.add_widget(info_screen)

        home_screen = HomeScreen(name="HomeScreen")
        screen_manager.add_widget(home_screen)

        quiz_screen = QuizScreen(name="QuizScreen")
        screen_manager.add_widget(quiz_screen)

        game_screen = GameScreen(name="GameScreen")
        screen_manager.add_widget(game_screen)

        screen_manager.current = "HomeScreen"
        return screen_manager


if __name__ == "__main__":
    HealthApp().run()
