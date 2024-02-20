import pygame
from pygame.sprite import AbstractGroup


class Platform(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup, x, y):
        super().__init__(*groups)
        self.name = "platform"
        self.image = pygame.image.load("./assets/roof_floor.png")
        self.collision = self.image.get_rect()
        self.collision.x = x
        self.collision.y = y

    def getCordinates(self):
        return (self.collision.x, self.collision.y)
