import pygame
from code.entity import Entity


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Ajustando avatar
        self.surf = pygame.transform.scale(
            self.surf,
            (int(self.surf.get_width() * 3.5), int(self.surf.get_height() * 3.5)),
        )
        self.rect = self.surf.get_rect(left=position[0], top=position[1])

        self.speed = 8
        self.walk = self.surf
        # Configurando a imagem de ataque
        self.attack = pygame.image.load("./asset/attack.png").convert_alpha()
        self.attack = pygame.transform.scale(
            self.attack,
            (int(self.attack.get_width() * 3.5), int(self.attack.get_height() * 3.5)),
        )
        self.is_attacking = False

        # Ajustando sistema de colisão
        self.hitbox = pygame.Rect(position[0], position[1], 60, 100)
        largura_ataque = self.attack.get_width()
        altura_ataque = self.attack.get_height()
        self.attack_hitbox = pygame.Rect(0, 0, largura_ataque, altura_ataque)

        # Definindo contagem de vida
        self.max_hp = 100
        self.hp = 100
        self.is_dead = False
        self.invincible_timer = 0  # Tempo de invencibilidade após tomar dano

    # Método para receber dano
    def take_damage(self, amount: int):
        # Só toma dano se não estiver no tempo de invencibilidade e não estiver morto
        if self.invincible_timer == 0 and not self.is_dead:
            self.hp -= amount
            if self.hp <= 0:
                self.hp = 0
                self.is_dead = True
            # Dano TODA VEZ que a lança bater
            self.invincible_timer = 20

    def move(self):
        # Reduz o timer de invencibilidade
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        # Se estiver morto, não faz mais nada
        if self.is_dead:
            return

        # Checando teclas pressionadas
        keys = pygame.key.get_pressed()

        # Condição para aplicar a imagem de ataque e ligar o dano
        if keys[pygame.K_SPACE]:
            self.surf = self.attack
            self.is_attacking = True  # O Player atacando

            # Posiciona o hitbox do fogo na frente do personagem
            # Agora ele usa a largura da imagem de ataque para calcular a posição final
            self.attack_hitbox.left = self.rect.right
            self.attack_hitbox.centery = self.rect.centery
        else:
            self.surf = self.walk
            self.is_attacking = False  # O player está passivo

            # Move o hitbox do fogo para longe da tela para não atingir ninguém
            self.attack_hitbox.left = -500

        # Lógica de movimentação
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Andando para a esquerda (A ou ←)
            self.rect.x -= self.speed
        elif (
            keys[pygame.K_d] or keys[pygame.K_RIGHT]
        ):  # Andando para a direita (D ou →)
            self.rect.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # Andando para a cima (W ou ↑)
            self.rect.y -= self.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:  # Andando para a baixo (S ou ↓)
            self.rect.y += self.speed

        # Definindo os limites da window
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1920:
            self.rect.right = 1920
        if self.rect.top < 344:
            self.rect.top = 344
        if self.rect.bottom > 1080:
            self.rect.bottom = 1080

        # Acompanha a posição do personagem, mas mantém tamanho fixo
        self.hitbox.center = self.rect.center
