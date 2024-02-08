import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        platform1 = pygame.image.load("/assets/p1.png").convert_alpha()
        platform = platform1.get_rect()
