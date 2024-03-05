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
        self.imageBack = pygame.image.load("./assets/sky_background.png").convert_alpha()
        self.imagefarground1 = pygame.image.load("./assets/farground_spr1.png").convert_alpha()
        self.imagefarground2 = pygame.image.load("./assets/farground_spr1.png").convert_alpha()
        self.imagefrontground1 = pygame.image.load("./assets/frontground_spr2.png").convert_alpha()
        self.imagefrontground2 = pygame.image.load("./assets/frontground_spr2.png").convert_alpha()

        self.clock = pygame.time.Clock()

        self.platformGroup = pygame.sprite.Group()
        self.platformGroup.add(Platform(x=0, y=0))
        self.platformGroup.add(Platform(x=640, y=0))
        self.platformGroup.add(Platform(x=1280, y=0))
        self.platformGroup.add(Platform(x=1920, y=0))

        self.bumperGroup = pygame.sprite.Group()

        self.tick = 0

        self.speed = 20
        self.fargroundSpeed = 2
        self.frontgroundSpeed = 10
        self.fargroundX = 0
        self.frontgroundX = 0

    def draw(self):
        self.screen.blit(self.imageBack, (0, 0))
        self.screen.blit(self.imagefarground1, (self.fargroundX, 0))
        self.screen.blit(self.imagefarground2, (self.fargroundX+3072, 0))
        self.screen.blit(self.imagefrontground1, (self.frontgroundX, 0))
        self.screen.blit(self.imagefrontground2, (self.frontgroundX+3072, 0))

        self.fargroundX = (self.fargroundX-self.fargroundSpeed)%-3072
        self.frontgroundX = (self.frontgroundX-self.frontgroundSpeed)%-3072

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
            Platform(x=1920, y=0),
            SmallJump(x=1920, y=0),
            LongJump(x=1920, y=0),
        ]
        self.platformGroup.add(random.choice(self.platfomType))
        if self.platformGroup.sprites()[-1].name == "long":
            self.bumperGroup.add(Bumper(x=1920, y=768))

    def updateNewPlatform(self):
        if self.tick % (640//self.speed) == 0:

            self.deleteBumper(self.platformGroup.sprites()[0].name)
            self.platformGroup.remove(self.platformGroup.sprites()[0])

            self.createNewPlatform()

    def refreshScreen(self):
        self.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.tick = (self.tick+1)%60

            self.refreshScreen()
            self.updateNewPlatform()
            self.platformMovement()
            self.bumperMovement()

            self.clock.tick(60)


Main().run()
