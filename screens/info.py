from utils.widgets import AutoResizingImage
from utils.widgets import CustomScreen


class InfoScreen(CustomScreen):
    """
    A subclass of CustomScreen to hold pages of information.

    The JSON file should have the following structure:
    {
        "title": "The title of the page",
        "img": "The filename of an image in the images/ directory",
        "sections": [
            {
                "heading-title": "The section title",
                "text": "The section's body text"
            }
        ]
    }
    """

    def __init__(self, **kwargs):
        """
        Initialises the CustomScreen with the correct page type.

        Args:
            **kwargs:
                Arguments passed to the parent CustomScreen class
        """
        super().__init__(page_type="information-pages",
                         title_key="title", **kwargs)

    # -------------------------
    # LOADING METHODS (_load_*)
    # -------------------------

    def _load_page(self):
        """
        Loads the current page.

        Actions:
            - Adds a home button
            - Adds a page title and an image
            - Adds the page sections
            - Adds navigation buttons
        """
        super()._load_page()

        self._add_home_button()

        self._add_title_label()
        self._add_img()

        self._add_sections()

        self._add_navigation_buttons()

    # ---------------------------
    # UI-BUILDER METHODS (_add_*)
    # ---------------------------

    def _add_img(self):
        """
        Adds an image to the page.

        Actions:
            - Creates an Image widget with the current page's image path
            - Adds the image to the layout
        """
        img_path = "images/" + self.curr_page["img"]
        img_widget = AutoResizingImage(
            portion_of_screen_width=0.4, source=img_path)
        self.layout.add_widget(img_widget)

    def _add_sections(self):
        """
        Adds the sections to the page.

        Actions:
            - Iterates through each section in the current page:
                - Adds a label with the section title
                - Adds a label with the section text
        """
        for section in self.curr_page["sections"]:
            section_title = section["heading-title"]
            self._add_label(text=section_title, font_size=60)

            section_text = section["text"]
            self._add_label(text=section_text)

    def _add_navigation_buttons(self):
        """
        Adds buttons to navigate to the next and previous pages.

        Actions:
            - If the current page is not the last page:
                - Creates a button bound to _go_to_next_page
                - Adds the button to the layout

            - If the current page is not the first page:
                - Creates a button bound to _go_to_previous_page
                - Adds the button to the layout
        """
        if self.curr_page_index != self.max_page_index:
            self._add_next_page_button()

        if self.curr_page_index != 0:
            self._add_previous_page_button()
