import pygame
import random
from plateform import Platform
from smallJump import SmallJump
from longJump import LongJump
from bumper import Bumper


class Main:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True
        self.imageBack = pygame.image.load("./assets/sky_background.png").convert()

        self.clock = pygame.time.Clock()

        self.imageSmall = pygame.image.load("./assets/regular_jump.png").convert_alpha()
        self.imagePlatform = pygame.image.load("./assets/roof_floor.png").convert_alpha()
        self.imageBig = pygame.image.load("./assets/long_jump.png").convert_alpha()
        self.imageBumper = pygame.image.load("./assets/bumper.png").convert_alpha()

        self.platformGroup = pygame.sprite.Group()
        self.platformGroup.add(Platform(x=0, y=0, image=self.imagePlatform))
        self.platformGroup.add(Platform(x=640, y=0, image=self.imagePlatform))
        self.platformGroup.add(Platform(x=1280, y=0, image=self.imagePlatform))
        self.platformGroup.add(Platform(x=1920, y=0, image=self.imagePlatform))

        self.bumperGroup = pygame.sprite.Group()

        self.tick = 0

        self.speed = 10

    def draw(self):
        self.screen.blit(self.imageBack, (0, 0))

        for platform in self.platformGroup.sprites():
            self.screen.blit(platform.image, platform.getCordinates())

        for bumper in self.bumperGroup.sprites():
            self.screen.blit(bumper.image, bumper.getCordinates())

    def platformMovement(self):
        for platform in self.platformGroup.sprites():
            platform.collision.x -= self.speed 

    def bumperMovement(self):
        for bumper in self.bumperGroup.sprites():
            bumper.collision.x -= self.speed

    def deleteBumper(self, platformName):
        if platformName == "long":
            self.bumperGroup.remove(self.bumperGroup.sprites()[0])

    def createNewPlatform(self):
        self.platfomType = [
            Platform(x=1920, y=0, image=self.imagePlatform),
            SmallJump(x=1920, y=0, image=self.imageSmall),
            LongJump(x=1920, y=0, image=self.imageBig),
        ]
        self.platformGroup.add(random.choice(self.platfomType))
        if self.platformGroup.sprites()[-1].name == "long":
            self.bumperGroup.add(Bumper(x=1920, y=768, image=self.imageBumper))

    def updateNewPlatform(self):
        if self.tick % (640//self.speed) == 0:

            self.deleteBumper(self.platformGroup.sprites()[0].name)
            self.platformGroup.remove(self.platformGroup.sprites()[0])
            self.tick = 0

            self.createNewPlatform()

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
            self.updateNewPlatform()
            self.platformMovement()
            self.bumperMovement()

            print(self.clock.get_fps())

            self.clock.tick(60)


Main().run()
