import random
import time
from user_interface.menu import Menu
from user_interface.shared_window import  SharedWindow
from game_classes.barcopirata import BarcoPirata
from game_classes.teclado import get_tecla
from game_classes.boss import Boss
from game_classes.fastboat import FastBoat
from user_interface.music import Music
from game_classes.powerup import Powerup
from game_classes.game_background import GameBackground
secureRandom = random.SystemRandom()

class ObjectControl:
    gameover = False
    points = 0
    powerups = []
    def __init__(self, simbolos, velocidade, qtdsimbolos, play_menu:Menu, dificuldade):
        ObjectControl.set_points(0)
        self.dificuldade = dificuldade
        self.simbolos = simbolos
        self.play_menu = play_menu
        self.play_menu.set_music("./sounds/music/play.ogg")
        self.janela = SharedWindow.instance
        self.velocidade = velocidade
        self.velocidademaxima = self.velocidade + self.velocidade*self.dificuldade*0.5
        self.qtdsimbolos = qtdsimbolos
        self.qtdmaxsimbolos = self.qtdsimbolos + self.dificuldade*2
        self.objetos = []
        self.teclado = SharedWindow.get_keyboard()
        self.tecla = ''
        self.teclanova = ''
        self.teclaantiga = None
        self.qtdinimigosmortos = 0
        self.last_enemy = time.time()
        self._next_enemy = 5
        self.bossfight = False
        self.qtdboss = 0
        self.powerups = []


    @classmethod
    def check_gameover(cls):
        if BarcoPirata.gameover:
            cls.gameover = True

    @classmethod
    def set_gameover(cls):
        cls.gameover = False
        BarcoPirata.set_gameover(False)

    @classmethod
    def set_points(cls, points):
        cls.points = points

    def reseta_ultimo_inimigo(self, tempo):
        self.last_enemy = time.time() - (tempo - self.last_enemy)

    def callPowerups(self):
        for powerup in self.powerups:
            p = powerup()
            if p == -1:
                self.powerups.remove(powerup)
                break

    def gera_inimigo(self, boss = False):
        velocidade = self.velocidade + int(ObjectControl.points/20)
        if velocidade > self.velocidademaxima:
            velocidade = self.velocidademaxima
        qtdsimbolos = self.qtdsimbolos + int(ObjectControl.points/1000)
        if qtdsimbolos > self.qtdmaxsimbolos:
            qtdsimbolos = self.qtdmaxsimbolos

        if not boss:
            self.objetos.append(secureRandom.choice([
                BarcoPirata(self.simbolos, qtdsimbolos, self.janela, velocidade,1),
                BarcoPirata(self.simbolos, qtdsimbolos, self.janela, velocidade, 1),
                FastBoat(self.simbolos, qtdsimbolos, self.janela, velocidade,1)
            ]))
        else:
            self.objetos.append(
                Boss(self.simbolos, qtdsimbolos, self.janela, velocidade, 2 + self.dificuldade + self.qtdboss))

        self.objetos[-1].desenha()


    def move(self):
        for obj in self.objetos:
            destruir = obj.move(self.tecla)
            if destruir == -1:
                self.destroi_inimigo(obj)

                if self.bossfight and len(self.objetos) == 0:
                    self.bossfight = False
                    self.last_enemy = time.time()
                    if Music.volume > 0:
                        self.play_menu.music_manager.custom_music.decrease_volume(30)
                    self.play_menu.set_music("./sounds/music/play.ogg")


    def desenha(self):
        for obj in self.objetos:
            obj.desenha()
        for powerup in self.powerups:
            powerup.draw()

    def recebe_teclado(self):
        self.tecla = None
        self.teclanova = get_tecla(self.teclado)
        if(self.teclanova == None):
            self.teclaantiga = None
        elif(self.teclaantiga == None and self.teclanova!= None):
            self.tecla = self.teclanova
            self.teclaantiga = self.tecla

    def reset(self):
        self.objetos.clear()
        self.powerups.clear()

    def destroi_inimigo(self, inimigo: BarcoPirata):
        ObjectControl.set_points(ObjectControl.points + inimigo.pontuacao)

        self.objetos.remove(inimigo)
        self.qtdinimigosmortos += 1
        if self.qtdinimigosmortos % 20 == 0:
            self.powerups.append(Powerup(self, self.simbolos))

    def geracao_inimigos(self):
        if not self.bossfight:
            if time.time() - self.last_enemy >= self._next_enemy:
                self.gera_inimigo()
                self.last_enemy = time.time()
                self._next_enemy = secureRandom.randint(-2, 1) + 4

            if ObjectControl.points//500 > self.qtdboss:
                self.bossfight = True
                self.qtdboss +=1
                self.gera_inimigo(boss=True)
                self.play_menu.set_music("./sounds/music/boss.ogg")
                if Music.volume > 0:
                    self.play_menu.music_manager.custom_music.increase_volume(30)

    def ajustar_atributos(self,type, apply):
        if type == "slow":
            for object in self.objetos:
                if apply:
                    object.velocidade = object.velocidade/2
                else:
                    object.velocidade = object.velocidade*2


    def __call__(self):
        ObjectControl.check_gameover()
        self.geracao_inimigos()
        self.recebe_teclado()
        self.move()
        self.callPowerups()