from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from utils.helpers import parse_json


class CustomScreen(Screen):
    """
    A generic screen subclass that handles layout and loading data.

    Attributes:
        pages (list):
            A list of "pages" (dictionaries) loaded from a JSON file.
            Each page contains content to display at once. For example:
            - A page of information
            - A page representing a quiz question
            The name "pages" is generic to support any type of content
        title_key (str):
            The key in each page in the json file specifying the title
        number_of_pages (int):
            Total number of pages
        max_page_index (int):
            Index of the last page
        curr_page_index (int):
            Index of currently displayed page
        curr_page (dict):
            The content in the current page
        layout (BoxLayout):
            The layout displayed on screen
        scroll_view (ScrollView):
            The scroll view wrapping the main layout
        title (str):
            The current page's title (Set if a title label is added)
   """

    def __init__(self, page_type, title_key="title", **kwargs):
        """
        Loads the pages and initializes the first page.

        Args:
            page_type (str):
                The key in the json file specifying which pages to load.
            title_key (str):
                The key in each page in the json file specifying the title
            **kwargs:
                Additional arguments passed to the parent Screen class.

        Actions:
            - Assigns a value to the title_key attribute
            - Loads pages from the JSON file
            - Calculates number_of_pages and max_page_index
            - Initialises curr_page_index to 0
            - Loads the first page
        """

        super().__init__(**kwargs)

        self.title_key = title_key

        self.pages = parse_json("data.json")[page_type]

        self.number_of_pages = len(self.pages)

        self.max_page_index = self.number_of_pages - 1

        self.curr_page_index = 0

        self._load_page()

    # -------------------------
    # LOADING METHODS (_load_*)
    # -------------------------

    def _load_page(self):
        """
        Sets up scrollable layout for the current page.

        Actions:
            - Stores the current page data in curr_page
            - Clears all widgets from the screen
            - Creates a vertical BoxLayout whose size adjusts to its children
            - Wraps the BoxLayout in a ScrollView and adds it to the screen
        """

        self.curr_page = self.pages[self.curr_page_index]

        self.clear_widgets()

        self.layout = BoxLayout(orientation="vertical",
                                            size_hint_y=None,
                                            spacing=30,
                                            padding=[20, 20, 20, 20])

        # Automatically set the layout's height to fit its children
        self.layout.bind(
            minimum_height=self.layout.setter("height"))

        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.layout)
        self.add_widget(self.scroll_view)

    # ---------------------------
    # UI-BUILDER METHODS (_add_*)
    # ---------------------------

    def _add_button(self, text, on_release_func, size_hint_x=1, height=50):
        """
        Adds a button to the layout

        Args:
            text (str): The text to be displayed on the button
            on_release_func (callable): Function to call when button is pressed
            size_hint_x (float, optional): Size hint for x axis (Default 1)
            height (int, optional): Height of the button (Default 50)

        Actions:
            - Creates a button
            - Binds the button to the on_release_func
            - Adds the button to the layout
        """
        button = Button(text=text, size_hint_y=None,
                        size_hint_x=size_hint_x, height=height)
        button.bind(on_release=on_release_func)
        self.layout.add_widget(button)

    def _add_label(self, text, font_size=40):
        """
        Adds a label to the layout

        Args:
            text (str): The text to be displayed on the label
            font_size (int): The label's font size

        Actions:
            - Creates an AutoResizingLabel
            - Adds the AutoResizingLabel to the layout
        """
        label = AutoResizingLabel(text=text, font_size=font_size)
        self.layout.add_widget(label)

    def _add_next_page_button(self):
        """Adds a button to go to the next page"""
        self._add_button(text="Next", on_release_func=self._go_to_next_page)

    def _add_previous_page_button(self):
        """Adds a button to go to the next page"""
        self._add_button(
            text="Back", on_release_func=self._go_to_previous_page)

    def _add_home_button(self):
        """Adds a button to return to the home screen."""
        self._add_button(text="Home", size_hint_x=0.2,
                         height=100, on_release_func=self._go_home)

    def _add_title_label(self):
        """
        Adds a label for the page title.

        Actions:
            - Assigns the page's title to self.title
            - Adds the label to the layout
        """
        self.title = self.curr_page[self.title_key]
        title_label = AutoResizingLabel(text=self.title, font_size=90)
        self.layout.add_widget(title_label)

    # ----------------------
    # APP NAVIGATION METHODS
    # ----------------------
    def _go_to_next_page(self, *args):
        """
        Loads the next page.

        Actions:
            - Increases curr_page_index
            - Loads the new page
        """
        self.curr_page_index += 1
        self._load_page()

    def _go_to_previous_page(self, *args):
        """
        Loads the previous page.

        Actions:
            - Decreases curr_page_index
            - Loads the page
        """
        self.curr_page_index -= 1
        self._load_page()

    def _go_home(self, *args):
        """Moves to the homepage."""
        self.manager.current = "HomeScreen"


class AutoResizingImage(Image):
    """An image whose size will auto-adjust if the screen changes size."""

    def __init__(self, portion_of_screen_width, **kwargs):
        """
        Sets up the automatic size adjustment.

        Args:
            portion_of_screen_width (float):
                The amount of the screen's width the image takes up
            **kwargs:
                Arguments passed to the parent Image class

        Actions:
            - Sets the height to be controlled manually
            - Sets the image to a specified portion of the screen's width
            - Centers the image
            - Binds the image's height to its width
        """
        super().__init__(**kwargs)

        self.size_hint_y = None

        self.size_hint_x = portion_of_screen_width

        self.pos_hint = {"center_x": 0.5}

        self.bind(width=self._update_size)

    def _update_size(self, *args):
        """Adjusts the image's height to maintain aspect ratio."""
        self.height = self.width / self.image_ratio


class AutoResizingLabel(Label):
    """A label that wraps text and adjusts height to fit content."""

    def __init__(self, **kwargs):
        """
        Sets up wrapping and height adjustment.

        Args:
            **kwargs:
                Arguments passed to the parent Label class

        Actions:
            - Sets the height to be controlled manually
            - Binds the text width to the widget's width for wrapping
            - Binds the widget's height to the text height
        """
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.bind(width=self._update_text_width)
        self.bind(texture_size=self._update_height)

    def _update_text_width(self, *args):
        """Sets the text width to the widget's width so it wraps properly."""
        self.text_size = (self.width, None)

    def _update_height(self, *args):
        """Sets the widget's height to the height of the text."""
        self.height = self.texture_size[1]
