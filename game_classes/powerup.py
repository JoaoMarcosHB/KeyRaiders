import time
import random
from math import ceil

import pygame
from pplay.sprite import Sprite
from game_classes.sequencias import Sequencia
from game_classes.teclado import get_tecla
from user_interface.shared_window import SharedWindow

class Powerup:
    types = ["slow", "health"]
    def __init__(self, objectControl, symbols):
        self.type = random.choice(Powerup.types)
        self.objectcontrol = objectControl
        self.window = SharedWindow.instance
        self.sprite = Sprite(f"images/{self.type}.png", frames=1)
        self.sprite.set_position(random.randint(self.window.width//2,int(self.window.width - (self.objectcontrol.qtdsimbolos*30//2)-self.sprite.width//2)),0 - self.sprite.height - 40)
        self.symbols = symbols
        self.keyboard = SharedWindow.get_keyboard()
        self.timecatch = None
        self.valororiginal = 0
        self.sequencia = None
        self.velocidade = self.objectcontrol.velocidade*0.7
        self.gera_sequencia(self.objectcontrol.qtdsimbolos)
        self.lastTecla = None
        self.caminho_fonte = "./fonts/CutePixel.ttf"
        self.fontmenor = pygame.font.Font(self.caminho_fonte, 24)
        self.contaTempo = 0


    def gera_sequencia(self, qtdsimbolos):
        seq = []
        for j in range(qtdsimbolos):
            seq.append(random.choice(self.symbols))
        posx = self.sprite.x + self.sprite.width//2 - (qtdsimbolos*30//2)
        self.sequencia = Sequencia(seq, posx, self.sprite.y, self.velocidade, 0)

    def gera_efeito(self):
        self.timecatch = time.time()
        self.contaTempo = time.time()
        self.sequencia = None
        self.sprite = Sprite(f"images/{self.type}mini.png", frames=1)
        self.sprite.set_position(self.window.width - self.sprite.width - (len(self.objectcontrol.powerups)-1)*self.sprite.width, 5)
        if (self.type == "health"):
            self.valororiginal = self.objectcontrol.qtdsimbolos
            self.objectcontrol.qtdsimbolos =max(1, self.valororiginal//2)
        elif (self.type == "slow"):
            self.valororiginal = self.objectcontrol.velocidade
            self.objectcontrol.velocidade = self.valororiginal//2
        self.objectcontrol.ajustar_atributos(self.type, True)

    def draw(self):
        self.sprite.draw()
        if self.sequencia is not None:
            self.sequencia.desenha()
        if self.timecatch != None:
            self.printTime()

    def move(self):
        self.sprite.y += self.velocidade * self.window.delta_time()
        self.sequencia.move_y(self.sprite.y, self.sprite.height)
        tecla = get_tecla(self.keyboard)
        sequenciaDestruida = 0
        if self.lastTecla is None and tecla is not None:
            self.lastTecla = tecla
            sequenciaDestruida = self.sequencia.verifica_tecla(tecla)
        elif tecla is None:
            self.lastTecla = None
        if sequenciaDestruida == -1:
            self.gera_efeito()
        if self.sprite.y >= self.window.height:
            return -1
        return 0

    def printTime(self):
        texto = self.fontmenor.render(f"{int(30 - (ceil(self.contaTempo-self.timecatch)))}", True, (0,0,0))
        tela = self.window.get_screen()
        tela.blit(texto, (self.sprite.x + self.sprite.width//2 - texto.get_width()//2, self.sprite.y + self.sprite.height))

    def desfazEfeito(self):
        if (self.type == "health"):
            self.objectcontrol.qtdsimbolos = self.valororiginal
        elif (self.type == "slow"):
            self.objectcontrol.velocidade = self.valororiginal

        self.objectcontrol.ajustar_atributos(self.type, False)

    def contaEfeito(self):
        self.contaTempo += self.window.delta_time()
        if self.contaTempo - self.timecatch >= 30:
            self.desfazEfeito()
            return -1
        return 0

    def __call__(self):
        self.draw()
        if self.timecatch == None:
            return self.move()
        else:
            return self.contaEfeito()
