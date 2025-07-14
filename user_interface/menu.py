from .state_manager import GameStateManager
from .button import Button
from .music import Music
from .grid import Grid
from .shared_window import SharedWindow


class Menu:
    _shared_buttons = {}
    _main_menu_gsm = None

    allow_click = True
    time = 0
    _delay_time = 1

    @classmethod
    def return_gsm(cls):
        return cls._main_menu_gsm

    @classmethod
    def register_shared_button(cls, name, button_instance):
        """
        Registers a shared button instance with a given name.
        """
        cls._shared_buttons[name] = button_instance

    def __init__(self, is_main_menu=False):
        """
        If it is the main menu, automatically creates a GameStateManager.
        Secondary menus must use the game_state_manager from the main menu.
        """
        if is_main_menu:
            if Menu._main_menu_gsm is not None:
                raise RuntimeError("A main menu has already been created!")

            # Automatically create the GameStateManager for the main menu
            Menu._main_menu_gsm = GameStateManager(self)
            self.game_state_manager = Menu._main_menu_gsm

        else:
            if Menu._main_menu_gsm is None:
                raise ValueError("Secondary menus must be linked to a main menu first.")
            self.game_state_manager = Menu._main_menu_gsm

        self._buttons_list = []
        self.background = []
        self._grid = None
        self.music_manager = Music()

    def use_shared_button(self, name):
        """
        Adds a registered shared button to this menu's button list.
        """
        if name in Menu._shared_buttons:
            self._buttons_list.append(Menu._shared_buttons[name])
        else:
            raise KeyError(f"No shared button registered with name '{name}'")

    def add_buttons(self, *buttons: Button):
        """Adds one or more Button objects to the menu."""
        self._buttons_list.extend(buttons)

    def create_buttons(self,
                       coordinates_list: list[tuple[int, int]],
                       paths_list: list[tuple[str, str]],
                       functions_list: list[callable],
                       names_list: list[tuple],
                       size=60):

        # Security checks
        if not all([coordinates_list, paths_list, functions_list]):
            raise ValueError("None of the lists can be empty.")

        if len({len(coordinates_list), len(paths_list), len(functions_list)}) != 1:
            raise ValueError("All lists must have the same length.")

        if not all(callable(f) for f in functions_list):
            raise ValueError("All elements in the function list must be callable.")

        if not self._grid:
            raise ValueError("No grid layout defined.")

        # Getting the positions list
        positions_list = self._grid.get_points_position(*coordinates_list)

        # Creates the buttons and adds them to the buttons_list
        self._buttons_list.extend(
            Button(pos, paths, func, name,size)
            for pos, paths, func, name in zip(positions_list, paths_list, functions_list, names_list)
        )

    def draw_buttons(self):
        """Calls each button to draw itself on the screen."""
        for button_object in self._buttons_list:
            button_object()

    def verify_buttons(self):
        """Checks if any button is clicked and returns the clicked button."""
        if Menu.allow_click:
            for button_object in self._buttons_list:
                if button_object.is_clicked():
                    Menu.time = 0

                    if isinstance(button_object.function, Menu):
                        self.game_state_manager.set_timed_state(button_object.function)
                        Menu.allow_click = False
                    else:
                        button_object.function()
                        Menu.allow_click = False
                    return
        else:

            Menu.time += SharedWindow.instance.delta_time()
            if Menu.time >= Menu._delay_time:
                Menu.allow_click = True
                Menu.time = 0

    def add_background(self, *args: callable):
        self.background.extend(list(args))

    def set_grid(self, layout: tuple[int, int], x_offset: float, y_offset: float):
        self._grid = Grid(layout, x_offset, y_offset)

    def _draw_background(self):
        for background in self.background:
            background()

    def set_music(self, path):
        self.music_manager.set_custom_music(path)

    def __call__(self):
        self.music_manager.play()
        self._draw_background()
        self.draw_buttons()
        self.verify_buttons()
