import pygame

from code.menu import Menu

class Game: 
    def __init__(self):
        #Inicializando o pygame
        pygame.init()
        #Criando a tela do game
        self.window = pygame.display.set_mode(size = (1000, 900)) #Não redimencionei a window para ficar do tamanho da minha imagem de background, escolhi deixar minhas imagens do tamanho da window 

    def run(self):
        while True:
            menu = Menu(self.window) #Recebendo o Menu
            menu.run() #Executando o Menu
            pass




