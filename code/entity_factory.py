from code.player import Player
from code.enemy import Enemy
from code.relic import Relic

# Classe responsável por construir as entidades do jogo (Padrão Factory do UML)
class EntityFactory:
    @staticmethod
    def get_entity(entity_type: str, position: tuple):
        # A fábrica recebe um "pedido" (string) e entrega o objeto pronto
        if entity_type == "Player":
            return Player("walk", position)
        elif entity_type == "Enemy":
            # Aumentei a velocidade de 4 para 6 para o desafio ficar maior
            return Enemy("enemy_walk", position, speed=6, hp=50)
        elif entity_type == "Relic":
            return Relic("relic", position)
        else:
            return None
