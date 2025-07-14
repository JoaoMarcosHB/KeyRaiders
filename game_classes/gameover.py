from game_classes.controleinimigos import ObjectControl
from user_interface.button import Button
import time
from user_interface.shared_window import SharedWindow
from pplay.gameimage import GameImage
from pplay.sprite import Sprite
import pygame
from game_classes.teclado import get_tecla
dourado = (218, 165, 32)

class GameOver:
    def __init__(self, ranking, gsm, rankingmenu):
        self.ranking_menu = rankingmenu
        self.ranking = ranking
        self.gsm = gsm
        self.window = SharedWindow.instance
        self.pontuacao = ObjectControl.points
        self.caminho_fonte = "./fonts/CutePixel.ttf"
        self.font = pygame.font.Font(self.caminho_fonte, 96)
        self.fontmenor = pygame.font.Font(self.caminho_fonte, 36)
        self.fundo = GameImage("./images/game_background/fundofinal5.png")
        self.fundo.set_position(self.window.width/2 - self.fundo.width/2, self.window.height/2-self.fundo.height/2)
        self._paths = ("images/buttons/main/1a.png", "images/buttons/main/1b.png")
        self.sprite = Sprite("images/buttons/main/1a.png")
        self._posbotao = (self.fundo.x + self.fundo.width/2, self.fundo.y + self.fundo.height - self.sprite.height - 10)

        self.nome = ''
        self.botao = Button(self._posbotao, self._paths, self.registrar_pt(), (1, "Register"))
        self.tecla_antiga = None
        self.tecla = None
        self.controle = "|"
        self.ultimo = time.time()
        self.maxnome = 20
        self.teclado = self.window.get_keyboard()

    def registrar_pt(self):


        if self.nome.strip() != '':
            self.ranking.add_score(self.nome.upper(),self.pontuacao)
            self.gsm.return_to_initial_state()
            self.gsm.set_timed_state(self.ranking_menu)

    def recebe_nome(self):
        tecla = get_tecla(self.teclado)
        if tecla == None:
            self.tecla = None
            self.tecla_antiga = None
        elif tecla != self.tecla_antiga:
            self.tecla_antiga = tecla
            if tecla != "down" and tecla != "left" and tecla != "up" and tecla != "right":
                if tecla == "space":
                    if self.nome.strip() != '' and len(self.nome) < self.maxnome:
                        self.nome = self.nome + " "
                elif tecla == "backspace":
                    if self.nome != '':
                        nome = list(self.nome)
                        nome.pop()
                        junta = ''
                        for l in nome:
                            junta = junta + str(l)
                        self.nome = junta
                else:
                    if len(self.nome) < self.maxnome:
                        self.nome = self.nome + str(tecla)


    def draw_texto(self):
        gameover = self.font.render("Game Over", True, dourado)
        tela = SharedWindow.get_screen()
        posx = self.fundo.x + self.fundo.width/2 - gameover.get_width()/2
        posy = self.fundo.y + 40
        tela.blit(gameover, (posx,posy))
        texto = self.fontmenor.render(f"Your score was {self.pontuacao}.", True, dourado)
        texto2 = self.fontmenor.render("Enter your name to", True, dourado)
        posxtexto1 = self.fundo.x + self.fundo.width/2 - texto.get_width()/2
        posytexto1 =  posy + gameover.get_height()
        tela.blit(texto, (posxtexto1,posytexto1))
        posxtexto2 = self.fundo.x + self.fundo.width/2 - texto2.get_width()/2
        posytexto2 = posytexto1 + texto.get_height()
        tela.blit(texto2, (posxtexto2, posytexto2))
        texto2 = self.fontmenor.render("record your score.", True, dourado)
        posxtexto2 = self.fundo.x + self.fundo.width / 2 - texto2.get_width() / 2
        posytexto2 = posytexto2 + texto.get_height()/2 + 10
        tela.blit(texto2, (posxtexto2, posytexto2))
        texto = self.fontmenor.render(self.nome.upper() + self.controle, True, dourado)
        posxtexto1 = self.fundo.x + self.fundo.width / 2 - texto.get_width() / 2
        posytexto1 = posytexto2 + texto2.get_height()
        tela.blit(texto, (posxtexto1,posytexto1))
        if time.time() - self.ultimo >= 1:
            if self.controle == "|":
                self.controle = " "
            else:
                self.controle = '|'
            self.ultimo = time.time()

    def __call__(self):
        self.fundo.draw()
        self.draw_texto()
        self.recebe_nome()
        self.botao()
        if self.botao.is_clicked():
            self.registrar_pt()