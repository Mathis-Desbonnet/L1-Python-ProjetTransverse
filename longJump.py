import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("./assets/regular_jump.png")
        self.collision = self.image.get_rect()
