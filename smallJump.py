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

    def getCordinates(self):
        return (self.collision.x, self.collision.y)
