import pygame
from code.menu import Menu
from code.level import Level


class Game:
    def __init__(self):
        # Inicializando o pygame
        pygame.init()
        # Criando a tela do game
        self.window = pygame.display.set_mode(
            size=(1920, 1080)
        )  # Não redimencionei a window para ficar do tamanho da minha imagem de background, escolhi deixar minhas imagens do tamanho da window

    def run(self):
        while True:
            menu = Menu(self.window)  # Recebendo o Menu
            opcao_escolhida = menu.run()  # Executando o Menu
            # Iniciando level
            if opcao_escolhida == "New_Game":
                playing_level = True
                while playing_level:  # Controle do level
                    level = Level(self.window, "Level 1", "Single_Player")
                    level_return = level.run()  # Executando o Level
                    if (
                        level_return == "Restart"
                    ):  # Volta para o topo do loop reiniciando o level do zero
                        pass
                    if level_return == "Quit":  # Volta para o menu principal
                        playing_level = False
