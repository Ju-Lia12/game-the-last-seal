import pygame
from code.entity import Entity


class Relic(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Redimensiona o icone
        self.surf = pygame.transform.scale(
            self.surf, (self.surf.get_width() * 2, self.surf.get_height() * 2)
        )
        self.rect = self.surf.get_rect(left=position[0], top=position[1])

    # A relíquia não se move, então não precisa de lógica de movimento
    def move(self):
        pass
