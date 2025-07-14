from game_classes.barcopirata import BarcoPirata
from pplay.sprite import Sprite
from random import SystemRandom
secureRandom = SystemRandom()
class FastBoat(BarcoPirata):
    def __init__(self, simbolos, qtdsimbolos, janela, velocidade, qtdsequencias):
        super().__init__(simbolos, qtdsimbolos, janela, velocidade, qtdsequencias)
        self.barco = Sprite("assets/fastboat.png", frames=4)
        self.barco.set_position(janela.width,
                                secureRandom.randint(0, 20) * ((janela.height - self.barco.height - 30) // 20))
        self.barco.set_total_duration(500)
        self.velocidade = self.velocidade * 1.4
        self.sequencias.clear()
        self.listasequencias.clear()
        self.gera_sequencia(simbolos, max(1,qtdsimbolos//2))
        self.pontuacao = 10