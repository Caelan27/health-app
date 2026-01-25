from kivy.uix.button import Button
from utils.widgets import CustomScreen


class QuizScreen(CustomScreen):
    """
    A subclass of CustomScreen to hold questions for a quiz.

    The JSON file should have the following structure:
    {
        "question": "Question",
        "answers": [
            "Incorrect Answer 1",
            "Correct answer",
            "Incorrect Answer 2",
            ...
        ],
        "correct_answer_index": 1    # Index of the correct answer in the list
    }

        Attributes:
            score (int):
                The number of questions the user has answered correct
            has_chosen_answer (bool):
                If the user has already picked an answer in the current page
            correct_index (int):
                The index of the correct answer in the current page
            buttons (list):
                A list of all of the buttons in the current page
            percentage (int):
                The percentage the user got on the quiz
            chosen_button (Button):
                The button for the answer the user chose

    """

    def __init__(self, **kwargs):
        """
        Initialises the QuizScreen.

        Args:
            **kwargs:
                Arguments passed to the parent CustomScreen class

        Actions:
            - Initialises the CustomScreen with the correct page type
            - Initialises score to 0
        """
        super().__init__(page_type="quiz", title_key="question", **kwargs)
        self.score = 0

    # -------------------------
    # LOADING METHODS (_load_*)
    # -------------------------

    def _load_page(self):
        """
        Loads the current page.

        Actions:
            - Sets self.has_chosen_answer to False
            - Assigns the correct answer's index to self.correct_index
            - Adds a home button, title label, and answer buttons
        """
        super()._load_page()

        self.has_chosen_answer = False

        self.correct_index = self.pages[self.curr_page_index][
            "correct_answer_index"]

        self._add_home_button()

        self._add_title_label()

        self._add_answer_buttons()

    def _load_results_page(self, *args):
        """
        Loads the page displaying the user's results.

        Actions:
            - Adds a home button and results title to the layout
            - Adds the user's score and percentage to the layout
            - Add a comment to the layout
            - Adds a restart button to the layout
        """
        super()._load_page()

        self._add_home_button()
        self._add_results_title()
        self._add_score()
        self._add_percentage()
        self._add_comment()
        self._add_restart_button()

    # ---------------------------
    # UI-BUILDER METHODS (_add_*)
    # ---------------------------

    def _add_answer_buttons(self):
        """
        Adds buttons for each of the answers.

        Actions:
            - Initialises self.buttons as a dictionary (index: button)
            - Iterates for each answer:
                - Creates a button with the answer text
                - Assigns a value to answer_index property
                - Binds the button to _answer_question
                - Adds the button to the layout and self.buttons
        """
        # TODO: Implement shuffling of answers
        # Dictionary makes it easier to shuffle if I need it
        self.buttons = {}

        for (curr_index, answer) in enumerate(self.curr_page["answers"]):
            button = Button(text=answer, height=50, size_hint_y=None)

            button.answer_index = curr_index

            button.bind(on_release=self._answer_question)

            self.buttons[curr_index] = button
            self.layout.add_widget(button)

    def _add_results_title(self):
        """Creates a label with the text 'Results'"""
        self._add_label(text="Results", font_size=60)

    def _add_score(self):
        """
        Adds a label displaying the user's score.

        The text looks like:
        "You got:
        4/5"
        """
        results_string = "You got:\n" + str(self.score) + "/" + \
            str(self.number_of_pages)

        self._add_label(text=results_string, font_size=40)

    def _add_percentage(self):
        """
        Adds a label displaying the user's percentage.

        Actions:
            - Assigns self.percentage the percentage to the nearest integer
            - Appends a percent sign to the end of the number
            - Creates a label with the percentage
        """
        self.percentage = round(100 * self.score / self.number_of_pages)
        percentage_string = str(self.percentage) + "%"

        self._add_label(text=percentage_string, font_size=40)

    def _add_comment(self):
        """
        Adds a label displaying a comment based on the user's score

        Actions:
            - Determines a message based on which range their score falls in
            - Creates a label with that message
        """
        if self.percentage > 75:
            comment = ("Well Done! "
                       "You clearly know a lot about how to be healthy!")
        elif self.percentage > 50:
            comment = "You did well, but there is room for improvement."
        elif self.percentage > 25:
            comment = "You should read over the information pages again."
        else:
            comment = "You did terribly ):"

        self._add_label(text=comment, font_size=30)

    def _add_restart_button(self):
        """Adds a button to allow the user to restart the quiz"""
        self._add_button(text="Restart Quiz", on_release_func=self._restart)

    def _add_results_button(self):
        """Adds a button to allow the user to view their results."""
        self._add_button(text="Show Results",
                         on_release_func=self._load_results_page)

    # ------------------
    # QUIZ LOGIC METHODS
    # ------------------

    def _answer_question(self, button):
        """
        Handles what happens when the user chooses an answer.

        Actions:
            - Makes sure they haven't already chosen an answer
            - Stores their chosen_button in self.chosen_button
            - Sets has_chosen_answer to True
            - Displays whether the user got the question right or wrong
            - If this is the last question:
                - Add a button to go to the results page
            - If this isn't the last question:
                - Add a button to go to the next question
            - Add a button to restart the quiz

        """
        if not self.has_chosen_answer:
            self.chosen_button = button

            self.has_chosen_answer = True

            self._display_right_or_wrong()

            if self.curr_page_index == self.max_page_index:
                self._add_results_button()
            else:
                self._add_next_page_button()

            self._add_restart_button()

    def _display_right_or_wrong(self):
        """
        Determines if the user was correct and calls the appropriate function

        Actions:
            - If they were correct:
                - Call _display_correct()
            - If they were incorrect:
                - Call _display_incorrect()
        """
        if self.chosen_button.answer_index == self.correct_index:
            self._display_correct()
        else:
            self._display_incorrect()

    def _display_correct(self):
        """
        Tells the user they were correct.

        Actions:
            - Adds a label telling them they were correct
            - Changes the colour of the button they chose to green
            - Increases their score
        """
        self._add_label(text="Correct! Well done (:")

        self.chosen_button.background_color = (0, 1, 0, 1)

        self.score += 1

    def _display_incorrect(self):
        """
        Tells the user they were incorrect.

        Actions:
            - Adds a label telling them they were incorrect
            - Changes the colour of the button they chose to red
            - Changes the colour of the correct answer to green
        """
        self._add_label(text="Incorrect ):")

        self.buttons[self.correct_index].background_color = (0, 1, 0, 1)

        self.chosen_button.background_color = (1, 0, 0, 1)

    def _restart(self, *args):
        """
        Restarts the quiz.

        Actions:
            - Resets the curr_page_index to 0
            - Resets the score to 0
            - Loads the first page
        """
        self.curr_page_index = 0
        self.score = 0
        self._load_page()
