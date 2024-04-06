import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.rect = pygame.rect.Rect(x, y, 50, 50)
        
        self.collisionBox = pygame.rect.Rect(x, y, 50, 50)
        
    def setYPos(self, y):
        self.rect.y = y