import pygame
from pygame.font import Font
from pygame import Rect, Surface

#TODO: remover linhas de teste player
from code.player import Player


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        #self.entity_list: list[Entity] = []
        
        #Configurando visuais do Level
        self.surf = pygame.image.load('./asset/battlebackground1.png') #Carregando a imagem background
        self.rect = self.surf.get_rect() #Cordenadas da imagem background
        self.settings1 = pygame.image.load('./asset/settings1.png') #Carreagndo icon de settings
        self.settings1 = pygame.transform.scale(self.settings1, (100, 100)) #Redimensionando tamanho do icon
        self.settings1_rect = self.settings1.get_rect(center = (1850, 50)) #Definindo posição do icon
        #Definindo imagem do mini menu
        self.mini_menu = pygame.image.load('./asset/mini_menu.png')
        self.mini_menu = pygame.transform.scale(self.mini_menu, (800, 850))
        self.mini_menu_rect = self.mini_menu.get_rect(center = (960, 540))

        #TODO: remover linhas de teste player
        self.player = Player('walk', (400,600)) 

    def run(self, ):
        #Carregando música do level
        pygame.mixer_music.load('./asset/battle1.mp3')
        pygame.mixer_music.play(-1) #Tocando a musica do level
        while True:
            self.window.blit(source = self.surf, dest = self.rect) #Desenhando a imagem background do level
            self.window.blit(source = self.settings1, dest = self.settings1_rect) #Desenhando o icon 
            # TODO: remover linhas de teste player
            self.player.move()
            self.window.blit(source = self.player.surf, dest = self.player.rect)

            pygame.display.flip() #Exibindo configurações na tela 

            #Configurando o mini menu
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Detectando click do mouse
                    mouse_pos = pygame.mouse.get_pos()
                    if self.settings1_rect.collidepoint(mouse_pos): #Se o settings for selecionado congela o jogo e abre o mini menu de pausa
                        pausado = True
                        while pausado:
                            mouse_pos_settings = pygame.mouse.get_pos()
                            self.window.blit(source = self.mini_menu, dest = self.mini_menu_rect) #Desenhando o mini menu
                            #Definindo o texto do mini menu
                            self.level_text(80, 'MENU', (255, 235, 215), (960, 300))
                            rect_continue = self.level_text(50, 'Continue', (65, 85, 115), (960, 400))
                            rect_restart = self.level_text(50, 'Restart', (65, 85, 115), (960, 450))
                            rect_quit = self.level_text(50, 'Quit', (65, 85, 115), (960, 500))

                            botoes_menu = [rect_continue, rect_restart, rect_quit] #Lista de botões do mini menu
                            pygame.display.flip() #Exibindo na tela

                            #Checando clicks do mini menu
                            for event_mini_menu in pygame.event.get():
                                if event_mini_menu.type == pygame.MOUSEBUTTONDOWN and event_mini_menu.button == 1:
                                    for indice, botoes_menu in enumerate(botoes_menu):
                                        if botoes_menu.collidepoint(mouse_pos_settings):
                                            if indice == 0:
                                                pausado = False #Fecha o mini menu e continua o jogo
                                            elif indice == 1:
                                                return 'Restart'
                                            elif indice == 2:
                                                return 'Quit'



                # if event.type == pygame.QUIT:
                #     pygame.quit()
                #     quit()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_position: tuple):
        text_font: Font = pygame.font.SysFont (name = "FantasyRPGtextRegular", size = text_size)
        text_surf: Surface = text_font.render (text, False, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center = text_position)
        self.window.blit(source = text_surf, dest = text_rect)
        return text_rect #Retornando o retangulo criado para saber a posição do mouse