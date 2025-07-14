import random
from pplay.window import *
from pplay.sprite import *
from pplay.sound import Sound

from game_classes.game_background import GameBackground
from game_classes.sequencias import Sequencia
from user_interface.shared_window import SharedWindow
from user_interface.music import Music
secureRandom = random.SystemRandom()


class BarcoPirata:
    gameover = False
    velocidade = 1

    janela = ''
    def __init__(self, simbolos, qtdsimbolos, janela, velocidade, qtdsequencias):
        self.barco = Sprite("assets/barquinhopirata.png", 4)
        self.qtdsequencias = qtdsequencias
        self.listasequencias = []
        self.sequencias = []

        self.velocidade = velocidade
        self.barco.set_total_duration(1100)
        self.barco.set_position(janela.width, secureRandom.randint(0,20)*((janela.height - self.barco.height -30)// 20))
        self.janela = janela
        self.vivo = True
        self.pontuacao = 20
        self.explosion = Sprite("./images/effects/explosion2.png", frames=8)
        self.explosion.set_total_duration(300)
        self.explosionsound = Sound("./sounds/game_sounds/explosioncut.mp3")
        self.explosionsound.set_volume(Music.volume)
        self.gera_sequencia(simbolos, qtdsimbolos)

    @classmethod
    def set_gameover(cls, gameover:bool):
        cls.gameover = gameover

    def gera_sequencia(self, simbolos, qtdsimbolos):
        for i in range(self.qtdsequencias):
            seq = []
            for j in range(qtdsimbolos):
                seq.append(secureRandom.choice(simbolos))
            self.listasequencias.append(seq)
            self.sequencias.append(Sequencia(seq, self.barco.x, self.barco.y+self.barco.height, self.velocidade, i))

    def move_sequencias(self):
        for seq in self.sequencias:
            seq.move(self.barco.x)
    def desenha_sequencias(self):
        for seq in self.sequencias:
            seq.desenha()

    def move(self, tecla):
        if self.vivo:
            seq = 0
            if tecla is not None:
                seq = self.sequencias[0].verifica_tecla(tecla)
            if seq == 0:
                self.barco.x -= self.velocidade*self.janela.delta_time()
                if self.barco.x <= GameBackground.islandborder:
                    BarcoPirata.set_gameover(True)
                self.move_sequencias()

            elif seq == -1:
                self.sequencias.pop(0)
                self.listasequencias.pop(0)
                GameBackground.shoot_Cannon(self.barco.x + self.barco.width // 2, self.barco.y + self.barco.height // 2)
                self.explosionsound.play()

                if len(self.sequencias) > 0:
                    for seq in self.sequencias:
                        seq.reposiciona_sequencia()
                else:


                    self.vivo = False
                    self.explosion.set_position(self.barco.x, self.barco.y)
        else:
            if self.explosion.get_curr_frame() == self.explosion.get_final_frame()-1:
                return -1
        self.desenha_sequencias()
        self.desenha()
        return 0

    def desenha(self):
        self.barco.draw()
        self.desenha_sequencias()
        self.barco.update()
        if not self.vivo:
            self.explosion.draw()
            self.explosion.update()