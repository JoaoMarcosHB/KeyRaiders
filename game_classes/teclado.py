from pplay.window import *
from pplay.sprite import *
from user_interface.shared_window import SharedWindow
import pygame
def get_tecla(teclado):

    for evento in pygame.event.get():
        # Se o usuário fechar a janela
        if evento.type == pygame.QUIT:
            rodando = False

        # Verifica se uma tecla foi pressionada
        if evento.type == pygame.KEYDOWN:
            # Verifica se a tecla pressionada é o Backspace
            if evento.key == pygame.K_BACKSPACE:
                return "backspace"

    if(teclado.key_pressed("UP")):
        return 'up'
    if(teclado.key_pressed("DOWN")):
        return'down'
    if(teclado.key_pressed('LEFT')):
        return 'left'
    if(teclado.key_pressed("RIGHT")):
        return 'right'
    if teclado.key_pressed("space"):
        return 'space'
    # if teclado.key_pressed("backspace"):
    #     return "backspace"
    # Letras minúsculas (a-z)
    for codigo_ascii in range(ord('a'), ord('z') + 1):
        letra = chr(codigo_ascii)
        if teclado.key_pressed(letra):
            return letra

    # Números (0-9)
    for numero in range(10):
        numero_str = str(numero)
        if teclado.key_pressed(numero_str):
            return numero_str

    # Se nenhuma das teclas acima estiver pressionada
    return None