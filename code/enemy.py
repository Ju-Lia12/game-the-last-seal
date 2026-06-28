import pygame
from code.entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple, speed: int, hp: int):
        super().__init__(name, position)

        self.speed = speed
        self.hp = hp
        # Ajustando imagem enemy
        self.surf = pygame.transform.scale(
            self.surf, (self.surf.get_width() * 4, self.surf.get_height() * 4)
        )  # Dando zoom no corte para que o avatar fique proporcional a tela
        self.rect = self.surf.get_rect(left=position[0], top=position[1])

        self.timer_attack = 0

    def move(self, player_rect):
        # Definindo reconhecimento de distancia entre player para o ataque
        distancia = self.rect.left - player_rect.right
        if (
            distancia >= 30 and self.timer_attack == 0
        ):  # Continua andando se estiver longe
            self.rect.x -= self.speed
        else:  # Muda para imagem de ataque ao se aproximar do player
            self.timer_attack += 1

            if self.timer_attack < 5:
                self.rect.x -= 20
                if self.rect.left < player_rect.right - 10:
                    self.rect.left = player_rect.right - 10
            elif self.timer_attack < 18:
                self.rect.x += 2
            else:
                self.timer_attack = 0

        # print(f"player={player_rect.right} -- enemy: {self.rect.left}")

        # return super().move()
