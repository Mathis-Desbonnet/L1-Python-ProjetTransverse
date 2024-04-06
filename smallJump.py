import pygame
from pygame.sprite import AbstractGroup


class SmallJump(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup, x, y, image):
        super().__init__(*groups)
        self.name = "small"
        self.image = image
        self.collision = self.image.get_rect()
        self.collision.x = x
        self.collision.y = y
        
        self.allCollision = [
            pygame.rect.Rect(x, 848, 247, 234),
            pygame.rect.Rect(x+400, 848, 247, 234),
        ]

    def getCordinates(self):
        return (self.collision.x, self.collision.y)
