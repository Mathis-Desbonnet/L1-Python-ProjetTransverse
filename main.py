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
        
        self.imageTextPause = pygame.image.load("./assets/text_pause.png").convert_alpha()#PAUSE CODE
        self.imageTextResume = pygame.image.load("./assets/text_resume.png").convert_alpha()#PAUSE CODE
        self.imageKeyEscape = pygame.image.load("./assets/key_escape.png").convert_alpha()#PAUSE CODE
        self.imagePauseBack = pygame.image.load("./assets/pause_back.png").convert_alpha()#PAUSE CODE
        self.imageQuit = pygame.image.load("./assets/button_quit_0.png").convert_alpha()#PAUSE CODE

        self.platformGroup = pygame.sprite.Group()
        self.platformGroup.add(Platform(x=0, y=0, image=self.imagePlatform))
        self.platformGroup.add(Platform(x=640, y=0, image=self.imagePlatform))
        self.platformGroup.add(Platform(x=1280, y=0, image=self.imagePlatform))
        self.platformGroup.add(Platform(x=1920, y=0, image=self.imagePlatform))

        self.bumperGroup = pygame.sprite.Group()

        self.player = Player(200, 710)

        self.tick = 0

        self.speed = 10
        self.maxSpeed = 40
        self.fargroundSpeed = 2
        self.frontgroundSpeed = 10
        self.fargroundX = 0
        self.frontgroundX = 0
        self.anim = 0

        self.g = 9.8
        self.currentSpeed = 0
        self.nextPlatformHeight = 768

        self.isJumping = False
        self.needToFall = True
        
        self.ending = False
        self.onPause = False #PAUSE CODE
        self.isPausing = False #PAUSE CODE

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
            #LongJump(x=1920, y=0, image=self.imageBig),
        ]
        self.platformGroup.add(random.choice(self.platfomType))
        if self.platformGroup.sprites()[-1].name == "long":
            self.bumperGroup.add(Bumper(x=1920, y=768, image=self.imageBumper))

    def updateNewPlatform(self):
        if self.speed != 0:#PAUSE CODE
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
                self.player.setYPos(710)
                self.player.collisionBox.y = 710
                self.currentSpeed = 0
                self.isJumping = False

        if keys[pygame.K_SPACE] and not self.isJumping:
            if self.onPause:#PAUSE CODE
                from menu import mainMenu #PAUSE CODE
                self.running = False #PAUSE CODE
            else:
                self.isJumping = True
                self.currentSpeed = -50
                self.fallingPosition()

        if keys[pygame.K_ESCAPE]: #PAUSE CODE
            if not self.isPausing:#PAUSE CODE
                self.isPausing = True#PAUSE CODE
                self.onPause = not(self.onPause) #PAUSE CODE
                self.speed = 20*(not(self.onPause))#PAUSE CODE
                self.fargroundSpeed = 2*(not(self.onPause))#PAUSE CODE
                self.frontgroundSpeed = 10*(not(self.onPause))#PAUSE CODE
        else : self.isPausing = False#PAUSE CODE

    def draw(self):
        self.screen.blit(self.imageBack, (0, 0))
        self.screen.blit(self.imagefarground1, (self.fargroundX, 0))
        self.screen.blit(self.imagefarground2, (self.fargroundX+3072, 0))
        self.screen.blit(self.imagefrontground1, (self.frontgroundX, 0))
        self.screen.blit(self.imagefrontground2, (self.frontgroundX+3072, 0))

        self.fargroundX = (self.fargroundX-self.fargroundSpeed)%-3072
        self.frontgroundX = (self.frontgroundX-self.frontgroundSpeed)%-3072

        #pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect)
        
        self.screen.blit(self.player.images[self.anim%4], self.player.getCoordinates())
        if self.tick % (10-(self.speed//5)) == 0:
            self.anim += 1

        for platform in self.platformGroup.sprites():
            self.screen.blit(platform.image, platform.getCordinates())

        for bumper in self.bumperGroup.sprites():
            self.screen.blit(bumper.image, bumper.getCordinates())
            
        if self.onPause :#PAUSE CODE
            self.screen.blit(self.imagePauseBack, (0, 0))#PAUSE CODE
            self.screen.blit(self.imageKeyEscape, (210, 80))#PAUSE CODE
            self.screen.blit(self.imageQuit, (600, 456))#PAUSE CODE
            self.screen.blit(self.imageTextResume, (350, 92))#PAUSE CODE
        else :
            self.screen.blit(self.imageKeyEscape, (210, 80))#PAUSE CODE
            self.screen.blit(self.imageTextPause, (350, 92))#PAUSE CODE

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
