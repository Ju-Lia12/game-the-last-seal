import pygame.image 
from pygame.font import Font
from pygame import Surface, Rect

class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/img_menu.png') #Carregando a imagem background do Menu
        self.rect = self.surf.get_rect() #Cordenadas da imagem background

    def run(self, ):
        #Carregando música do Menu
        pygame.mixer_music.load('./asset/menu.mp3')
        pygame.mixer_music.play(-1) #Tocando a musica do Menu
        while True:
            self.window.blit(source = self.surf, dest = self.rect) #Desenhando a imagem background Menu na tela
            mouse_pos = pygame.mouse.get_pos() #Detectando a posição do mouse para fazer a seleção no Menu
            #Criando e confugurando o Menu
            self.menu_text(90,'The Last Seal', (255,202,202), (500,260))
            rect_new_game = self.menu_text(45,'New Game', (255,202,202), (500,500))
            rect_coop = self.menu_text(45,'New Game - Cooperative', (255,202,202), (500,550))
            rect_score = self.menu_text(45,'Score', (255,202,202), (500,600))
            rect_exit = self.menu_text(45,'Exit', (255,202,202), (500,650))
            #Mudando a cor do texto quando o mouse passa por ele
            if rect_new_game.collidepoint(mouse_pos):
                self.menu_text(45,'New Game', (255,155,155), (500,500))
            if rect_coop.collidepoint(mouse_pos):
                self.menu_text(45,'New Game - Cooperative', (255,155,155), (500,550))
            if rect_score.collidepoint(mouse_pos):
                self.menu_text(45,'Score', (255,155,155), (500,600))
            if rect_exit.collidepoint(mouse_pos):
                self.menu_text(45,'Exit', (255,155,155), (500,650))
            #Criando lista para usar como botões
            botoes = [rect_new_game, rect_coop, rect_score, rect_exit]

            pygame.display.flip() #Mostrando a imagem e texto do Menu
            
            #Checando eventos 
            for event in pygame.event.get():
                #Detectando se, e onde, o mouse foi pressionado
                if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                    for indice, botoes in enumerate(botoes):
                        if botoes.collidepoint(mouse_pos):
                            if indice == 0:
                                pass
                            if indice == 1:
                                pass
                            if indice == 2:
                                pass
                            if indice == 3:
                                pygame.quit()
                                quit()


                # if event.type == pygame.QUIT: 
                #     pygame.quit() #Fechar a tela
                #     quit() #Encerrar pygame



    def menu_text(self, text_size: int, text: str, text_color: tuple, text_position: tuple):
        text_font: Font = pygame.font.SysFont (name = "Jacquard12-Regular", size = text_size)
        text_surf: Surface = text_font.render (text, False, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center = text_position)
        self.window.blit(source = text_surf, dest = text_rect)
        return text_rect #Retornando o retangulo criado para saber a posição do mouse