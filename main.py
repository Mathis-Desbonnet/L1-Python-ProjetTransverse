import pygame
import random
from plateform import Platform
from smallJump import smallJump


class Main:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True
        self.imageBack = pygame.image.load("./assets/sky_background.png")

        self.clock = pygame.time.Clock()

        self.platformGroup = pygame.sprite.Group()
        self.platformGroup.add(Platform(x=0, y=0))
        self.platformGroup.add(Platform(x=640, y=0))
        self.platformGroup.add(Platform(x=1280, y=0))
        self.platformGroup.add(Platform(x=1920, y=0))

        self.tick = 0

    def draw(self):
        self.screen.blit(self.imageBack, (0, 0))

        for platform in self.platformGroup.sprites():
            self.screen.blit(platform.image, platform.getCordinates())

    def platformMovement(self):
        for platform in self.platformGroup.sprites():
            platform.collision.x -= 10

    def createNewPlatform(self):
        print(self.tick)
        if self.tick % 64 == 0:
            print(self.platformGroup.__len__())
            self.platfomType = [Platform(x=1920, y=0), smallJump(x=1920, y=0)]
            self.platformGroup.remove(self.platformGroup.sprites()[0])
            self.platformGroup.add(random.choice(self.platfomType))

    def refreshScreen(self):
        self.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.tick += 1

            self.refreshScreen()
            self.createNewPlatform()
            self.platformMovement()
            self.clock.tick(60)


Main().run()
