import pygame
import random
from pygame.font import Font
from pygame import Rect, Surface

from code.entity_factory import EntityFactory


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list = []
        # Imagem backgroubnd
        self.surf = pygame.image.load("./asset/battlebackground1.png")
        self.rect = self.surf.get_rect()
        # Carregando imagens de pausa/mini menu
        self.settings1 = pygame.image.load("./asset/settings1.png")
        self.settings1 = pygame.transform.scale(self.settings1, (100, 100))
        self.settings1_rect = self.settings1.get_rect(center=(1850, 50))
        self.mini_menu = pygame.image.load("./asset/mini_menu.png")
        self.mini_menu = pygame.transform.scale(self.mini_menu, (800, 850))
        self.mini_menu_rect = self.mini_menu.get_rect(center=(960, 540))
        # Barras de vida
        self.ui_bar = pygame.image.load("./asset/hp2.png").convert_alpha()
        self.ui_bar = pygame.transform.scale(
            self.ui_bar, (self.ui_bar.get_width() * 2, self.ui_bar.get_height() * 2)
        )
        # Registrando tamnho barra vermelha para calcular a porcentagem quando tomar dano
        self.bar_max_width = self.ui_bar.get_width()
        self.bar_height = self.ui_bar.get_height()
        # Cursor da vida
        self.ui_knob = pygame.image.load("./asset/hp3.png").convert_alpha()
        self.ui_knob = pygame.transform.scale(
            self.ui_knob, (self.ui_knob.get_width() * 2, self.ui_knob.get_height() * 2)
        )

        factory = EntityFactory()
        self.player = factory.get_entity("Player", (20, 600))
        # Lista para gerenciar múltiplos inimigos
        self.enemy_list = []
        self.spawn_timer = 0  # Temporizador para nascer inimigos
        # Definindo nascimentoo primeiro inimigo imediatamente
        primeiro_inimigo = factory.get_entity("Enemy", (1920, 600))
        self.enemy_list.append(primeiro_inimigo)
        # A relíquia fica no final da fase
        self.relic = factory.get_entity("Relic", (1800, 600))
        # Contador de selos coletados para a condição de vitória
        self.seals_collected = 0
        self.entity_list.append(self.player)

    def run(
        self,
    ):
        pygame.mixer_music.load("./asset/battle1.mp3")
        pygame.mixer_music.play(-1)
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.window.blit(source=self.settings1, dest=self.settings1_rect)

            # Configurando nascimento dos inimigos
            self.spawn_timer += 1
            if self.spawn_timer >= 60:  # Nasce 1 a cada 1 segundo)
                self.spawn_timer = 0
                y_aleatorio = random.randint(350, 900)
                novo_inimigo = EntityFactory.get_entity("Enemy", (1920, y_aleatorio))
                self.enemy_list.append(novo_inimigo)

            # Coleta da reliquia/selo
            self.window.blit(source=self.relic.surf, dest=self.relic.rect)
            if self.player.hitbox.colliderect(self.relic.rect):
                self.seals_collected += 1
                if self.seals_collected >= 4:
                    # print("VITÓRIA! Todos os selos coletados!")
                    # Loop da tela de vitória
                    win_screen = True
                    while win_screen:
                        self.level_title_text(
                            60,
                            "PARABÉNS, TODOS OS SELOS MÁGICOS COLETADOS!",
                            (0, 0, 0),
                            (960, 540),
                        )
                        pygame.display.flip()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                return "Quit"
                else:
                    # Move a relíquia para uma nova posição aleatória
                    self.relic.rect.x = random.randint(100, 1700)
                    self.relic.rect.y = random.randint(450, 900)

            # Configurando e checando colisões
            for enemy in self.enemy_list:
                # Atualiza hitboxes antes de checar colisões (evita erro de posição atrasada)
                enemy.update_hitboxes()
                # Verifica se a lança atingiu o player
                is_spear_hitting = (
                    enemy.timer_attack > 0
                    and self.player.hitbox.colliderect(enemy.spear_hitbox)
                )
                is_same_y = abs(self.player.hitbox.bottom - enemy.hitbox.bottom) < 150
                # O inimigo para de andar se o corpo dele bater no player (para dano de colisão)

                # Inimigo ataca se estiver perto e na mesma altura
                distancia = enemy.hitbox.left - self.player.hitbox.right
                can_attack = 0 < distancia < 100 and is_same_y

                # Sofrendo danos
                if self.player.is_attacking:
                    # Player ataca: usa a hitbox do fogo
                    if self.player.attack_hitbox.colliderect(enemy.hitbox):
                        enemy.take_damage(25)
                        print(f"Acertou fogo! HP Inimigo: {enemy.hp}")
                if is_spear_hitting:
                    # Inimigo ataca: a lança causa dano no corpo do player
                    self.player.take_damage(20)
                    print(f"Tomou lanca! HP Player: {self.player.hp}")

                # Dano visual
                if not enemy.is_dead:
                    enemy.move(can_attack)
                    # Efeito de piscar ao tomar dano inimigo
                    if enemy.invincible_timer == 0 or (enemy.invincible_timer % 6 < 3):
                        self.window.blit(source=enemy.surf, dest=enemy.rect)

            # # Efeito de piscar ao tomar dano player
            if not self.player.is_dead:
                self.player.move()
                if self.player.invincible_timer == 0 or (
                    self.player.invincible_timer % 6 < 3
                ):
                    self.window.blit(source=self.player.surf, dest=self.player.rect)

            # Sistema de vida e contador de reliquias/selos coletados

            # Calculando o tamanho atual da barra vermelha baseado na porcentagem de vida
            if self.player.hp > 0:
                porcentagem_hp = self.player.hp / self.player.max_hp
                largura_atual = int(self.bar_max_width * porcentagem_hp)
                # Cortando/Redimensionando a imagem vermelha para o tamanho atual de vida
                current_bar_surf = pygame.transform.scale(
                    self.ui_bar, (largura_atual, self.bar_height)
                )
                # Desenhando a barra vermelha na tela
                bar_x = 20
                bar_y = 40
                self.window.blit(current_bar_surf, (bar_x, bar_y))
                # Desenhando o marcador em cima da barra vermelha
                knob_x = bar_x + largura_atual - (self.ui_knob.get_width() // 2)
                knob_y = (
                    bar_y + (self.bar_height // 2) - (self.ui_knob.get_height() // 2)
                )
                self.window.blit(self.ui_knob, (knob_x, knob_y))

            # Desenhando o contador de selos na tela
            self.level_title_text(
                40, f"Selos: {self.seals_collected} / 4", (185, 0, 0), (1650, 50)
            )

            pygame.display.flip()

            # Configurações de final de jogo
            if self.player.is_dead:
                # print("GAME OVER!")
                # Loop da tela de Game Over
                game_over = True
                while game_over:
                    self.level_title_text(100, "GAME OVER", (160, 0, 0), (960, 540))
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            return "Restart"

            for event in pygame.event.get():
                if (
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                ):  # Detectando click do mouse
                    mouse_pos = pygame.mouse.get_pos()
                    if self.settings1_rect.collidepoint(
                        mouse_pos
                    ):  # Se o settings for selecionado congela o jogo e abre o mini menu de pausa
                        pausado = True
                        while pausado:
                            mouse_pos_settings = pygame.mouse.get_pos()
                            self.window.blit(
                                source=self.mini_menu, dest=self.mini_menu_rect
                            )  # Desenhando o mini menu
                            # Definindo o texto do mini menu
                            self.level_text(80, "MENU", (255, 235, 215), (960, 300))
                            rect_continue = self.level_text(
                                50, "Continue", (65, 85, 115), (960, 400)
                            )
                            rect_restart = self.level_text(
                                50, "Restart", (65, 85, 115), (960, 450)
                            )
                            rect_quit = self.level_text(
                                50, "Quit", (65, 85, 115), (960, 500)
                            )

                            botoes_menu = [
                                rect_continue,
                                rect_restart,
                                rect_quit,
                            ]  # Lista de botões do mini menu
                            pygame.display.flip()  # Exibindo na tela

                            # Checando clicks do mini menu
                            for event_mini_menu in pygame.event.get():
                                if (
                                    event_mini_menu.type == pygame.MOUSEBUTTONDOWN
                                    and event_mini_menu.button == 1
                                ):
                                    for indice, botoes_menu in enumerate(botoes_menu):
                                        if botoes_menu.collidepoint(mouse_pos_settings):
                                            if indice == 0:
                                                pausado = False  # Fecha o mini menu e continua o jogo
                                            elif indice == 1:
                                                return "Restart"
                                            elif indice == 2:
                                                return "Quit"

                # if event.type == pygame.QUIT:
                #     pygame.quit()
                #     quit()

    def level_text(
        self, text_size: int, text: str, text_color: tuple, text_position: tuple
    ):
        text_font: Font = pygame.font.SysFont(
            name="FantasyRPGtextRegular", size=text_size
        )
        text_surf: Surface = text_font.render(text, False, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_position)
        self.window.blit(source=text_surf, dest=text_rect)
        return text_rect  # Retornando o retangulo criado para saber a posição do mouse

    # Novo método para usar a fonte de título do Menu
    def level_title_text(
        self, text_size: int, text: str, text_color: tuple, text_position: tuple
    ):
        text_font: Font = pygame.font.SysFont(
            name="FantasyRPGtitleRegular", size=text_size
        )
        text_surf: Surface = text_font.render(text, False, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_position)
        self.window.blit(source=text_surf, dest=text_rect)
        return text_rect
