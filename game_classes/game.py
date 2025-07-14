from user_interface.menu import Menu
from user_interface.shared_window import SharedWindow
from game_classes.game_background import GameBackground
from game_classes.controleinimigos import ObjectControl
from game_classes.gameover import GameOver
from utilities import Ranking

class Game:
    background = None
    obj = None
    symbols = None
    def __init__(self, game_menu: Menu, ranking: Ranking, game_over_menu:Menu, rankingmenu: Menu):
        self.ranking_menu = rankingmenu
        self.window = SharedWindow.instance
        self.game_over_menu = game_over_menu
        if not self.window:
            raise ValueError("The shared_window instance must be set before creating the game.")
        self.background = None
        self.difficulty = None
        self.game_menu = game_menu
        self.gsm = game_menu.game_state_manager
        self.ranking = ranking
        self.symbols = None
        self.gamecontrol = None

    @classmethod
    def set_bg(cls, bg):
        cls.background = bg


    @classmethod
    def set_obj(cls,obj):
        cls.obj = obj

    @classmethod
    def set_symbols(cls, symb):
        cls.symbols = symb

    def _start_game(self):
        self.gsm.set_timed_state(self.game_menu)
        self.game_menu.background.clear()
        self.game_menu.add_background(self)
        self.background = GameBackground()
        self.gamecontrol = ObjectControl(self.symbols, 100 + 0.1*100*self.difficulty, 3+ self.difficulty, self.game_menu, self.difficulty)
        Game.set_bg(self.background)
        Game.set_obj(self.gamecontrol)
        Game.set_symbols(self.symbols)

    def easy(self):
        self.symbols = ['left', 'right']
        self.difficulty = 1
        self._start_game()

    def normal(self):
        self.difficulty = 2
        self.symbols = ['up', 'down', 'left', 'right']
        self._start_game()

    def hard(self):
        self.difficulty = 3
        self.symbols = ['up', 'down', 'left', 'right', 'a', 's','d']
        self._start_game()

    def check_gameover(self):
        if ObjectControl.gameover:
            self.gsm.return_to_initial_state()
            if len(self.game_over_menu.background) > 1:
                self.game_over_menu.background.pop()
            self.game_over_menu.add_background(GameOver(self.ranking, self.gsm, self.ranking_menu))
            self.gsm.set_timed_state(self.game_over_menu)
            self.background.reset()
            self.gamecontrol.reset()
            self.game_menu.background.clear()
            self.gamecontrol = None
            self.symbols = None
            self.difficulty = None
            self.background = None
            ObjectControl.set_gameover()
            ObjectControl.set_points(0)



    def __call__(self):
        #self.window.set_background_color((0, 0, 255))
        self.check_gameover()
        if self.background != None:
            self.background(ObjectControl.points)
        if self.gamecontrol != None:
            self.gamecontrol()

