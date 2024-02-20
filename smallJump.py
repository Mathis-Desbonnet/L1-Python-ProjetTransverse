import pygame
from pygame.sprite import AbstractGroup


class smallJump(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup, x, y):
        super().__init__(*groups)
        self.image = pygame.image.load("./assets/regular_jump.png")
        self.collision = self.image.get_rect()
        self.collision.x = x
        self.collision.y = y

    def getCordinates(self):
        return (self.collision.x, self.collision.y)
