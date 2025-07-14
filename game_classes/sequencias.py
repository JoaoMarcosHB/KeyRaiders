import random
from pplay.window import *
from pplay.sprite import *
secureRandom = random.SystemRandom()

class Sequencia:

    def __init__(self, sequencia, posx, posy, velocidade, linha):
        self.sequencia = []
        self.linha = linha
        self.seqescrita = sequencia
        self.seqcontrole = self.seqescrita.copy()
        for i in range(len(sequencia)):
            self.sequencia.append(Sprite(f"assets/{sequencia[i]}sprite.png", 2))
            self.sequencia[i].set_position(posx + self.sequencia[i].width*i, posy + self.sequencia[0].height*linha)
            self.sequencia[i].set_total_duration(1100)
        self.velocidade = velocidade

    def reposiciona_sequencia(self):
        for simb in self.sequencia:
            simb.y -= simb.height

    def desenha(self):
        for simb in self.sequencia:
            simb.draw()

    def move(self, posxbarco):
        qtd_movimento = self.sequencia[0].x - posxbarco
        for simb in self.sequencia:
            simb.x -= qtd_movimento

    def move_y(self, posypowerup, powerupheight):
        if len(self.sequencia) > 0:
            qtd_movimento = posypowerup+powerupheight - self.sequencia[0].y
            for simb in self.sequencia:
                simb.y += qtd_movimento

    def verifica_tecla(self, tecla):

        for i in range(len(self.seqcontrole)):
            if self.seqcontrole[i] == '':
                continue
            elif self.seqcontrole[i] == tecla:
                self.sequencia[i].set_curr_frame(1)
                self.seqcontrole[i] = ''
                if i == len(self.seqcontrole) - 1:
                    return -1 #Sequencia destruida
                break
            else:
                i = 0
                while(self.seqcontrole[i] == ''):
                    self.seqcontrole[i] = self.seqescrita[i]
                    self.sequencia[i].set_curr_frame(0)
                    i += 1
                return 0 #Sequencia não destruida