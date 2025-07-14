from game_classes.controleinimigos import ObjectControl
from game_classes.game import Game
from user_interface.button import Button
import time
from user_interface.music import Music
from user_interface.shared_window import SharedWindow
from pplay.gameimage import GameImage
from pplay.sprite import Sprite
import pygame
from game_classes.game_background import GameBackground
from game_classes.teclado import get_tecla
dourado = (218, 165, 32)

class Settings:
    def __init__(self, gsm, play=False, play_menu= None, gameover_menu=None):
        self.playing = play
        self.gsm = gsm
        self.playmenu = play_menu
        self.gameover = gameover_menu
        self.volume = Music.volume
        self.window = SharedWindow.instance
        self.caminho_fonte = "./fonts/CutePixel.ttf"
        self.font = pygame.font.Font(self.caminho_fonte, 64)
        self.fontmenor = pygame.font.Font(self.caminho_fonte, 36)
        self.fundo = GameImage("./images/game_background/fundofinal5.png")
        self.fundo.set_position(self.window.width / 2 - self.fundo.width / 2,
                                self.window.height / 2 - self.fundo.height / 2)
        self._paths = ("images/buttons/main/1a.png", "Images/buttons/main/1b.png")
        self.sprite = Sprite("images/buttons/main/1a.png")
        self.incbutton = None
        self.decbutton = None
        self.showFpsButton = None
        self.hideFpsButton = None
        self.gera_botoes()
        self.bg = None
        self.obj = None
        self.time_clicked = time.time()

    def resetar(self):
        self.bg = None
        self.obj = None

    def increase_volume(self):
        if self.volume < 100:
            self.volume += 5
            #Music.set_main_music("sounds/music/menu.ogg")
        else:
            self.volume = 100

            #Music.set_main_music("sounds/music/menu.ogg")
        amount = self.volume - Music.volume
        if self.playing:
            if self.playmenu.music_manager.custom_music is not None:
                self.playmenu.music_manager.custom_music.increase_volume(amount)
            if self.gameover.music_manager.custom_music is not None:
                self.gameover.music_manager.custom_music.increase_volume(amount)
        Music.set_volume(self.volume)

    def decrease_volume(self):
        if self.volume > 0:
            self.volume -= 5
            #Music.set_main_music("sounds/music/menu.ogg")

        else:
            self.volume = 0
            #Music.set_main_music("sounds/music/menu.ogg")
        amount = self.volume - Music.volume
        if self.playing:
            if self.playmenu.music_manager.custom_music is not None:
                self.playmenu.music_manager.custom_music.increase_volume(amount)
            if self.gameover.music_manager.custom_music is not None:
                self.gameover.music_manager.custom_music.increase_volume(amount)
        Music.set_volume(self.volume)

    def change_show_fps(self):
        GameBackground.showFps = not GameBackground.showFps


    def gera_botoes(self):
        pathsincrease = ("images/buttons/settings/increasevolume1.png", "images/buttons/settings/increasevolume2.png")
        pathsdecrease = ("images/buttons/settings/decreasevolume1.png", "images/buttons/settings/decreasevolume2.png")
        sprite = Sprite(pathsincrease[0])
        config = self.font.render("Settings", True, dourado)
        posx = self.fundo.x + self.fundo.width / 2 - config.get_width() / 2
        posy = self.fundo.y + 40
        volume = self.fontmenor.render(f"Volume: {self.volume}", True, dourado)
        posx = self.fundo.x + self.fundo.width / 2 - volume.get_width() / 2
        posy = posy + config.get_height() + volume.get_height()
        self.incbutton = Button((posx + volume.get_width() + sprite.width, posy + volume.get_height()/2), pathsincrease, self.increase_volume(), (0, ""))
        self.decbutton = Button((posx -sprite.width, posy + volume.get_height()/2), pathsdecrease, self.decrease_volume(),
                                (0, ""))
        pathsshowFps = ("images/buttons/settings/fps1a.png", "images/buttons/settings/fps1b.png")
        pathshideFps = ("images/buttons/settings/fps2a.png", "images/buttons/settings/fps2b.png")

        sprite = Sprite(pathsshowFps[0])
        posx = self.window.width//2
        posy += sprite.height*2

        self.showFpsButton = Button((posx, posy), pathsshowFps, self.change_show_fps,(1, "Show FPS"),
                                    size=30)
        self.hideFpsButton = Button((posx, posy), pathshideFps, self.change_show_fps, (1, "Hide FPS"),
                                    size=30)



    def _draw_text(self):
        tela = self.window.get_screen()
        text = "Settings"
        if self.playing:
            text = "Paused"
        config = self.font.render(text, True, dourado)
        posx = self.fundo.x + self.fundo.width / 2 - config.get_width() / 2
        posy = self.fundo.y + 40
        tela.blit(config, (posx, posy))
        volume = self.fontmenor.render(f"Volume: {self.volume}", True, dourado)
        posx = self.fundo.x + self.fundo.width / 2 - volume.get_width() / 2
        posy = posy + config.get_height() + volume.get_height()
        tela.blit(volume, (posx,posy))


    def draw_buttons(self):
        #if self.incbutton is not None and self.decbutton is not None:
        self.incbutton()
        if self.incbutton.is_clicked():
            self.increase_volume()

        self.decbutton()
        if self.decbutton.is_clicked():
            self.decrease_volume()

        if not GameBackground.showFps:
            self.showFpsButton()
            if self.showFpsButton.is_clicked():
                self.change_show_fps()
        else:
            self.hideFpsButton()
            if self.hideFpsButton.is_clicked():
                self.change_show_fps()

    def set_background(self):
        if self.playing:
            if self.bg != Game.background:
                self.time_clicked = time.time()
                self.bg = Game.background
            if self.obj != Game.obj:
                self.obj = Game.obj
            if self.bg is not None:
                self.bg(ObjectControl.points)
            if self.obj is not None:
                self.obj.desenha()


    def __call__(self):
        self.set_background()
        self.fundo.draw()
        self._draw_text()
        self.draw_buttons()
        self.volume = Music.volume