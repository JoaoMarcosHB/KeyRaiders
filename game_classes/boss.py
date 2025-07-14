from game_classes.barcopirata import BarcoPirata
from user_interface.shared_window import SharedWindow


class Boss(BarcoPirata):
    def __init__(self, simbolos, qtdsimbolos, janela, velocidade, qtdsequencias):
        super().__init__(simbolos, qtdsimbolos, janela, velocidade, qtdsequencias)
        self.barco.y = SharedWindow.instance.height//2
        self.sequencias.clear()
        self.listasequencias.clear()
        self.velocidade = self.velocidade/5
        self.gera_sequencia(simbolos, qtdsimbolos)
