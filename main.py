import pygame
import random
from plateform import Platform
from player import Player
from smallJump import SmallJump
from longJump import LongJump
from bumper import Bumper
from fonctionTrajectoireY import ySerieBasicJump


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

        self.player = Player(200, 800)

        self.tick = 0

        self.speed = 10
        self.maxSpeed = 40
        self.fargroundSpeed = 2
        self.frontgroundSpeed = 10
        self.fargroundX = 0
        self.frontgroundX = 0

        self.g = 9.8
        self.currentSpeed = 0
        self.nextPlatformHeight = 768

        self.isJumping = False
        self.needToFall = True
        
        self.ending = False

    def fall(self):
            self.player.collisionBox.y += 5
            self.needToFall = True
            for platform in self.platformGroup.sprites():
                for collision in platform.allCollision:
                    if self.player.collisionBox.colliderect(collision):
                        self.needToFall = False
            if self.needToFall and self.isJumping == False:
                self.currentSpeed = 50
                self.ending = True
            self.player.collisionBox.y = self.player.rect.y

    def platformMovement(self):
        for platform in self.platformGroup.sprites():
            platform.collision.x -= self.speed 
            for collision in platform.allCollision:
                collision.x -= self.speed

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
            
            if self.speed < self.maxSpeed:
                self.speed += 1
                self.fargroundSpeed += 1
                self.frontgroundSpeed += 1

            self.createNewPlatform()
            
    def fallingPosition(self):
        self.player.setYPos(ySerieBasicJump(self.g, self.player.rect.y, self.currentSpeed, self.speed/20)[0])
        self.player.collisionBox.y = ySerieBasicJump(self.g, self.player.rect.y, self.currentSpeed, self.speed/20)[0]

    def isKeySpacePressed(self):
        keys = pygame.key.get_pressed()

        if self.isJumping:
            if self.needToFall:
                self.fallingPosition()
                self.currentSpeed = ySerieBasicJump(self.g, self.player.rect.y, self.currentSpeed, self.speed/20)[1]
            else:
                self.player.setYPos(800)
                self.player.collisionBox.y = 800
                self.currentSpeed = 0
                self.isJumping = False

        if keys[pygame.K_SPACE] and not self.isJumping:
            self.isJumping = True
            self.currentSpeed = -50
            self.fallingPosition()

    def draw(self):
        self.screen.blit(self.imageBack, (0, 0))
        self.screen.blit(self.imagefarground1, (self.fargroundX, 0))
        self.screen.blit(self.imagefarground2, (self.fargroundX+3072, 0))
        self.screen.blit(self.imagefrontground1, (self.frontgroundX, 0))
        self.screen.blit(self.imagefrontground2, (self.frontgroundX+3072, 0))

        self.fargroundX = (self.fargroundX-self.fargroundSpeed)%-3072
        self.frontgroundX = (self.frontgroundX-self.frontgroundSpeed)%-3072

        pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect)

        for platform in self.platformGroup.sprites():
            self.screen.blit(platform.image, platform.getCordinates())

        for bumper in self.bumperGroup.sprites():
            self.screen.blit(bumper.image, bumper.getCordinates())

    def refreshScreen(self):
        self.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.tick = (self.tick+1)%60

            if not self.ending:
                self.refreshScreen()
                self.updateNewPlatform()
                self.platformMovement()
                self.bumperMovement()
                self.isKeySpacePressed()
                self.fall()
            else:
                self.refreshScreen()
                self.updateNewPlatform()
                self.platformMovement()
                self.bumperMovement()
                self.fallingPosition()
                self.currentSpeed = ySerieBasicJump(self.g, self.player.rect.y, self.currentSpeed, self.speed/20)[1]


            self.clock.tick(60)

Main().run()
