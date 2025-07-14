import time

from utilities import Background, Ranking
from user_interface.menu import Menu
from user_interface.button import Button
from user_interface.music import Music
from game_classes.game import Game
from user_interface.shared_window import SharedWindow
from user_interface.settings import Settings
from pplay.sprite import Sprite


window = SharedWindow(1500, 800)
window.set_title("Keyraiders")
window.set_fullscreen()

# Initializing Game Menus
main_menu = Menu(is_main_menu=True)
play_menu = Menu()
options_menu = Menu()
difficulty_menu = Menu()
ranking_menu = Menu()
settings_menu = Menu()
game_over_menu = Menu()

x_offset = window.width / 28
y_offset = window.height / 20

ranking = Ranking()

# =================================================================================================

"""Adding Backgrounds"""

# Main Menu
title = Sprite("images/title.png")
title.set_position(window.width / 2 - title.width / 2, y_offset - 50)

background = Background()

main_menu.add_background(background, title.draw)

# Difficulty Menu
difficulty_menu.add_background(background)

# Play Menu
#game = Game(play_menu, ranking, game_over_menu, ranking_menu)
opt_sett = Settings(main_menu.game_state_manager, True, play_menu, game_over_menu)
# Options Menu
options_menu.add_background(opt_sett)

# Ranking Menu
ranking_menu.add_background(background, ranking)

# Settings Menu
settings_menu.add_background(background, Settings(main_menu.game_state_manager))

# Game Over Menu
game_over_menu.add_background(background)

# ==========================================================================================

""" Managing Sounds """

Button.set_sounds(
    hover="sounds/button_sounds/1b.mp3",
    click="sounds/button_sounds/1a.mp3"
)

Music.set_main_music("sounds/music/menu.ogg")

play_menu.set_music(None)
#options_menu.set_music("sounds/music/dead.ogg")
game_over_menu.set_music("sounds/music/dead.ogg")
# ==========================================================================================

""" Names """

#
Button.add_text_property(1, "CutePixel", 50, (151, 38),
                         (151, 49), (0, 0, 0))

# Main Menu
main_menu_buttons_name = [(1, "Play"), (1, "Ranking"), (1, "Settings"), (1, "Exit")]

# Difficulty Menu
difficulty_menu_buttons_name = [(1, "Easy"), (1, "Normal"), (1, "Hard")]

# Options Menu
options_menu_buttons_name = [(1, "Return to Menu")]

# ==========================================================================================

""" Coordinates """

# Main Menu
main_menu.set_grid((1, 6), x_offset, y_offset)
main_menu_buttons_coord = [(1, 3), (1, 4), (1, 5), (1, 6)]

# Difficulty Menu
difficulty_menu.set_grid((1, 3), x_offset, y_offset)
difficulty_menu_buttons_coord = [(1, 1), (1, 2), (1, 3)]

# Play Menu
play_menu_button_pos = (x_offset, y_offset)

# Options Menu
options_menu.set_grid((1, 3), x_offset, y_offset)
options_menu_buttons_coord = [(1, 3)]

# Others
back_button_pos = (x_offset, y_offset)

# ==========================================================================================

""" Paths """

# Main Menu
main_menu_buttons_paths = [
    ("images/buttons/main/1a.png", "Images/buttons/main/1b.png"),
    ("images/buttons/main/2a.png", "Images/buttons/main/2b.png"),
    ("images/buttons/main/3a.png", "Images/buttons/main/3b.png"),
    ("images/buttons/main/6a.png", "Images/buttons/main/6b.png"),
]

# Difficulty Menu
difficulty_menu_buttons_path = [
    ("images/buttons/difficulty/1a.png", "Images/buttons/difficulty/1b.png"),
    ("images/buttons/difficulty/2a.png", "Images/buttons/difficulty/2b.png"),
    ("images/buttons/difficulty/3a.png", "Images/buttons/difficulty/3b.png"),
]

# Play Menu
play_menu_button_path = ("images/buttons/play/1a.png", "images/buttons/play/1b.png")

# Options Menu
options_menu_button_path = [("images/buttons/main/3a.png", "Images/buttons/main/3b.png")]

# Others
back_button_path = ("images/buttons/back_button_a.png", "images/buttons/back_button_b.png")

# =================================================================================================

""" Functions """

# Main Menu
main_menu_functions_list = [
    difficulty_menu,
    ranking_menu,
    settings_menu,
    main_menu.game_state_manager.return_to_previous_state,
]

# Difficulty Menu
difficulty_menu_buttons_functions = [
    Game(play_menu, ranking, game_over_menu, ranking_menu).easy,
    Game(play_menu, ranking, game_over_menu, ranking_menu).normal,
    Game(play_menu, ranking, game_over_menu, ranking_menu).hard
]
def opt_func():
    main_menu.game_state_manager.return_to_initial_state()
    Menu.allow_click = False
    Menu.time = 0

# Options Menu
options_menu_button_function = [opt_func]

def function_back_button():
    Menu.return_gsm().return_to_previous_state()
    if Game.obj is not None:
        Game.obj.reseta_ultimo_inimigo(opt_sett.time_clicked)
        opt_sett.resetar()

# Others
back_button_function = function_back_button

# =================================================================================================

""" Creating Buttons """

# Main Menu
main_menu.create_buttons(
    main_menu_buttons_coord,
    main_menu_buttons_paths,
    main_menu_functions_list,
    main_menu_buttons_name
)

# Difficulty Menu
difficulty_menu.create_buttons(
    difficulty_menu_buttons_coord,
    difficulty_menu_buttons_path,
    difficulty_menu_buttons_functions,
    difficulty_menu_buttons_name
)

# Play Menu
play_menu_button = Button(play_menu_button_pos,
                          play_menu_button_path,
                          options_menu,
                          align_horizontal="left",
                          align_vertical="top")

# Options Menu
options_menu.create_buttons(
    options_menu_buttons_coord,
    options_menu_button_path,
    options_menu_button_function,
    options_menu_buttons_name,
    40
)

# Others
back_button = Button(back_button_pos,
                     back_button_path,
                     back_button_function,
                     align_horizontal="left",
                     align_vertical="top")

# =================================================================================================

""" Managing Buttons """

# Shared Buttons
Menu.register_shared_button("back_button", back_button)

# Difficulty Menu
difficulty_menu.use_shared_button("back_button")

# Play menu
play_menu.add_buttons(play_menu_button)

# Options Menu
options_menu.use_shared_button("back_button")

# Ranking menu
ranking_menu.use_shared_button("back_button")

# Settings Menu
settings_menu.use_shared_button("back_button")

# Game Over Menu
game_over_menu.use_shared_button("back_button")