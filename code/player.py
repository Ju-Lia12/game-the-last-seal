import pygame
from code.entity import Entity

class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        #Ajustando avatar
        self.surf = pygame.transform.scale(self.surf, (self.surf.get_width() * 4, self.surf.get_height() * 4)) #Dando zoom no corte para que o avatar fique proporcional a tela
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        
        self.speed = 8
        #Configurando a imagem de ataque
        self.walk = self.surf
        self.attack = pygame.image.load('./asset/attack.png').convert_alpha()
        self.attack = pygame.transform.scale(self.attack, (self.attack.get_width() * 4, self.attack.get_height() * 4))

    def move(self):
        #Definindo movimentos do avatar
        keys = pygame.key.get_pressed() #Checando teclas pressionadas
        #Condição para aplicar a imagem de ataque
        if keys[pygame.K_SPACE]:
            self.surf = self.attack
        else:
            self.surf = self.walk

        if keys[pygame.K_a] or keys[pygame.K_LEFT]: #Andando para a esquerda (A ou ←) 
            self.rect.x -= self.speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: #Andando para a direita (D ou →)
            self.rect.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]: #Andando para a cima (W ou ↑)
            self.rect.y -= self.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]: #Andando para a baixo (S ou ↓)
            self.rect.y += self.speed
        #Definindo os limites da window
        if self.rect.left < 0: 
            self.rect.left = 0
        if self.rect.right > 1920: 
            self.rect.right = 1920
        if self.rect.top < 344: 
            self.rect.top = 344
        if self.rect.bottom > 1080: 
            self.rect.bottom = 1080

        #print(self.rect)

        #return super().move()