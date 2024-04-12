import pygame
from pygame.sprite import AbstractGroup


class Bumper(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup, x, y) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load("./assets/bumper_spr.png").convert_alpha()
        
        self.allImages = [self.image.subsurface((0, 0, 64, 128)), self.image.subsurface((64, 0, 64, 128)), self.image.subsurface((128, 0, 64, 128)), self.image.subsurface((192, 0, 64, 128)), self.image.subsurface((256, 0, 64, 128)), self.image.subsurface((320, 0, 64, 128))]
        self.collision = pygame.rect.Rect(x, y, 64, 128)
        self.collision.x = x
        self.collision.y = y

        self.collidedWithBumper = False

    def getCordinates(self):
        return (self.collision.x, self.collision.y)