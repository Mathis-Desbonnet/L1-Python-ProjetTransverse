import pygame
import random
from plateform import Platform
from player import Player
from smallJump import SmallJump
from longJump import LongJump
from bumper import Bumper
from fonctionTrajectoireY import ySerieBasicJump, defineSpeedWithAngle


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

        self.g = 9.81
        self.currentSpeed = 0
        self.nextPlatformHeight = 768

        self.isJumping = False
        self.needToFall = True
        
        self.ending = False
        self.onPause = False #PAUSE CODE
        self.isPausing = False #PAUSE CODE
        
        self.longJumpState = False
        
        self.saveSpeed = 0

        self.bumperAnim = 0

        self.arrowImage = pygame.image.load("./assets/arrow.png").convert_alpha()
        self.allArrowImages = [self.arrowImage.subsurface((0, 0, 384, 384)), self.arrowImage.subsurface(384, 0, 384, 384), self.arrowImage.subsurface(768, 0, 384, 384), self.arrowImage.subsurface(1152, 0, 384, 384), self.arrowImage.subsurface(1536, 0, 384, 384),
                               self.arrowImage.subsurface(0, 384, 384, 384), self.arrowImage.subsurface(384, 384, 384, 384), self.arrowImage.subsurface(768, 384, 384, 384), self.arrowImage.subsurface(1152, 384, 384, 384), self.arrowImage.subsurface(1536, 384, 384, 384),
                               self.arrowImage.subsurface(0, 768, 384, 384), self.arrowImage.subsurface(384, 768, 384, 384), self.arrowImage.subsurface(768, 768, 384, 384), self.arrowImage.subsurface(1152, 768, 384, 384), self.arrowImage.subsurface(1536, 768, 384, 384)]
        self.arrowAnim = 0
        self.arrowGoUp = True
        self.angle = 20

    def fall(self):
            self.player.collisionBox.y += 5
            self.needToFall = True
            for platform in self.platformGroup.sprites():
                for collision in platform.allCollision:
                    if self.player.collisionBox.colliderect(collision):
                        self.needToFall = False
            if self.needToFall and self.isJumping == False and self.longJumpState == False:
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

    def bumperCollision(self):
        if not self.longJumpState and not self.ending:
            for bumper in self.bumperGroup.sprites():
                if self.player.collisionBox.colliderect(bumper.collision):

                    self.saveSpeed = self.speed
                    self.speed = 0
                    self.frontgroundSpeed = 0
                    self.fargroundSpeed = 0

                    self.bumperAnim = 1

                    self.longJumpState = True
                    bumper.collidedWithBumper = True

                    self.player.rect.y -= 100
                    self.player.collisionBox.y -= 100

    def chooseAngle(self):
        if self.speed == 0 and self.longJumpState and not self.onPause:
            self.screen.blit(self.allArrowImages[self.arrowAnim], (400, 400))

            if self.tick%10 == 0 and self.arrowGoUp:
                self.arrowAnim += 1
                self.angle += 5
            elif self.tick%10 == 0 and not self.arrowGoUp:
                self.arrowAnim -= 1
                self.angle -= 5

            if self.arrowAnim == 14:
                self.arrowGoUp = False
            elif self.arrowAnim == 0:
                self.arrowGoUp = True

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.arrowAnim = 0
                self.speed = self.saveSpeed
                self.frontgroundSpeed = self.speed
                self.fargroundSpeed = self.speed//5

                self.currentSpeed = defineSpeedWithAngle(-self.angle, self.speed)[1]
                self.speed = defineSpeedWithAngle(-self.angle, self.speed)[0]
                self.frontgroundSpeed = self.speed
                self.fargroundSpeed = self.speed//5
                    
                print(self.speed, self.currentSpeed)
                    
                self.player.setYPos(ySerieBasicJump(5, self.player.rect.y, self.currentSpeed, self.speed/20)[0])
                self.player.collisionBox.y = ySerieBasicJump(5, self.player.rect.y, self.currentSpeed, self.speed/20)[0]

                self.angle = 20

    def longJump(self):
        if self.longJumpState and self.needToFall and not self.onPause and self.speed != 0:
            self.player.setYPos(ySerieBasicJump(5, self.player.rect.y, self.currentSpeed, self.speed/20)[0])
            self.player.collisionBox.y = ySerieBasicJump(5, self.player.rect.y, self.currentSpeed, self.speed/20)[0]
            self.currentSpeed = ySerieBasicJump(5, self.player.rect.y, self.currentSpeed, self.speed/20)[1]
            if self.bumperAnim < 6:
                self.bumperAnim += 1
        elif self.longJumpState and not self.onPause and self.speed != 0:
                self.player.setYPos(710)
                self.player.collisionBox.y = 710
                self.currentSpeed = 0
                self.speed = 10
                self.longJumpState = False

    def createNewPlatform(self, delta):
        self.platfomType = [
            Platform(x=1920-delta, y=0, image=self.imagePlatform),
            SmallJump(x=1920-delta, y=0, image=self.imageSmall),
            LongJump(x=1920-delta, y=0, image=self.imageBig),
        ]
        randomNumber = random.randint(0, 10)
        if randomNumber < 10:
            self.platformGroup.add(self.platfomType[randomNumber%2])
        else:
            self.platformGroup.add(self.platfomType[2])
        if self.platformGroup.sprites()[-1].name == "long":
            self.bumperGroup.add(Bumper(x=1920, y=720))

    def updateNewPlatform(self):
        if self.speed != 0:#PAUSE CODE
            if self.platformGroup.sprites()[0].collision.x <= -640:
                
                delta = -640 - self.platformGroup.sprites()[0].collision.x

                self.deleteBumper(self.platformGroup.sprites()[0].name)
                self.platformGroup.remove(self.platformGroup.sprites()[0])
                self.tick = 0

                self.createNewPlatform(delta)
            
    def fallingPosition(self):
        self.player.setYPos(ySerieBasicJump(self.g, self.player.rect.y, self.currentSpeed, self.speed/20)[0])
        self.player.collisionBox.y = ySerieBasicJump(self.g, self.player.rect.y, self.currentSpeed, self.speed/20)[0]

    def isKeySpacePressed(self):
        keys = pygame.key.get_pressed()

        if self.isJumping and not self.onPause:
            if self.needToFall:
                self.fallingPosition()
                self.currentSpeed = ySerieBasicJump(self.g, self.player.rect.y, self.currentSpeed, self.speed/20)[1]
            else:
                self.player.setYPos(710)
                self.player.collisionBox.y = 710
                self.currentSpeed = 0
                self.isJumping = False

        if keys[pygame.K_SPACE] and not self.isJumping and not self.longJumpState:
            if self.onPause:#PAUSE CODE
                self.saveSpeed = self.speed
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
                if self.onPause:
                    self.saveSpeed = self.speed
                    self.speed = 0#PAUSE CODE
                    self.fargroundSpeed = 0#PAUSE CODE
                    self.frontgroundSpeed = 0#PAUSE CODE
                else:
                    self.speed = self.saveSpeed#PAUSE CODE
                    self.fargroundSpeed = self.saveSpeed//5#PAUSE CODE
                    self.frontgroundSpeed = self.saveSpeed#PAUSE CODE
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
        
        if self.isJumping:
            self.screen.blit(self.player.images[0], self.player.getCoordinates())
        else:
            self.screen.blit(self.player.images[self.anim%4], self.player.getCoordinates())
        if self.tick % (10-(self.speed//5)) == 0 and self.speed != 0 and not self.onPause:
            self.anim += 1

        for platform in self.platformGroup.sprites():
            self.screen.blit(platform.image, platform.getCordinates())

        for bumper in self.bumperGroup.sprites():
            if bumper.collidedWithBumper:
                self.screen.blit(bumper.allImages[self.bumperAnim%6], bumper.getCordinates())
            else:
                self.screen.blit(bumper.allImages[0], bumper.getCordinates())
            
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
        self.chooseAngle()
        pygame.display.flip()
        
    def increaseSpeed(self):
        self.speed += 1
        self.fargroundSpeed += 0.2
        self.frontgroundSpeed += 1

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.tick = (self.tick+1)%60
            
            if pygame.time.get_ticks() % 10000 == 0 and not self.longJumpState:
                self.increaseSpeed()
                print(self.speed)
                
            self.longJump()

            if not self.ending:
                self.refreshScreen()
                self.updateNewPlatform()
                self.platformMovement()
                self.bumperMovement()
                self.isKeySpacePressed()
                self.bumperCollision()
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
