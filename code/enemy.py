import pygame
from code.entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple, speed: int, hp: int):
        super().__init__(name, position)

        self.speed = speed
        self.hp = hp
        # Definiçoes de vida
        self.max_hp = hp
        self.is_dead = False
        self.invincible_timer = 0  # Tempo de invencibilidade após dano
        # Ajustando imagem enemy
        self.surf = pygame.transform.scale(
            self.surf, (self.surf.get_width() * 4, self.surf.get_height() * 4)
        )
        self.rect = self.surf.get_rect(left=position[0], top=position[1])

        self.timer_attack = 0

        # Hitbox do corpo do esqueleto
        self.hitbox = pygame.Rect(0, 0, 40, 90)
        # Hitbox da lança
        self.spear_hitbox = pygame.Rect(0, 0, 120, 20)

    def update_hitboxes(self):
        self.hitbox.center = self.rect.center
        self.spear_hitbox.width = 150
        # Posiciona a lança um pouco mais à frente
        self.spear_hitbox.right = self.rect.left + 40
        self.spear_hitbox.centery = self.rect.centery + 10

    # Método para receber dano
    def take_damage(self, amount: int):
        if self.invincible_timer == 0 and not self.is_dead:
            self.hp -= amount
            if self.hp <= 0:
                self.hp = 0
                self.is_dead = True
            # Tempo de invencibilidade
            self.invincible_timer = 20

    def move(self, is_colliding: bool):
        # Reduz o timer de invencibilidade
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        # Se o inimigo morreu, ele para de se mover e de atacar
        if self.is_dead:
            return

        # Se não está colidindo com o jogador E não está no meio de um ataque: anda para a esquerda
        if not is_colliding and self.timer_attack == 0:
            self.rect.x -= self.speed
        else:
            # Se colidiu (ou já começou a atacar), avança a animação
            self.timer_attack += 1

            # Bote
            if self.timer_attack < 5:
                self.rect.x -= 25
            # Recuo
            elif self.timer_attack < 15:
                self.rect.x += 12
            # Fim do ataque, zera o timer para poder andar ou atacar de novo
            else:
                self.timer_attack = 0

        # Atualiza as hitboxes após mover
        self.update_hitboxes()
