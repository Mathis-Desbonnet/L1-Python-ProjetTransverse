import pygame
from pygame.sprite import AbstractGroup


class LongJump(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup, x, y, image):
        super().__init__(*groups)
        self.name = "long"
        self.image = image
        self.collision = self.image.get_rect()
        self.collision.x = x
        self.collision.y = y
        self.jumpSurfaceCollision = pygame.rect.Rect(230, 282, 14, 50)
        self.jumpSurfaceCollision.x = x + 230
        self.jumpSurfaceCollision.y = y + 282

        self.allCollision = [
            pygame.rect.Rect(x, 848, 96, 234),
            pygame.rect.Rect(x+544, 848, 96, 234),
        ]


    def getCordinates(self):
        return (self.collision.x, self.collision.y)
