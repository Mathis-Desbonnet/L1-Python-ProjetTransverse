import pygame
import random
from plateform import Platform
from player import Player
from smallJump import SmallJump
from longJump import LongJump
from bumper import Bumper
from fonctionTrajectoireY import ySerieBasicJump, defineSpeedWithAngle
from thief import Thief
from badEndMenu import badEndMenu
from goodEndMenu import goodEndMenu

from pygame import mixer

class Main:
    def __init__(self) -> None:
        mixer.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True

        self.imageBack = pygame.image.load("./assets/sky_background.png").convert_alpha()
        self.imagefarground1 = pygame.image.load("./assets/farground_spr1.png").convert_alpha()
        self.imagefarground2 = pygame.image.load("./assets/farground_spr1.png").convert_alpha()
        self.imagefrontground1 = pygame.image.load("./assets/frontground_spr2.png").convert_alpha()
        self.imagefrontground2 = pygame.image.load("./assets/frontground_spr2.png").convert_alpha()

        self.clock = pygame.time.Clock()

        self.imageSmall = [pygame.image.load("./assets/gap_2.png").convert_alpha(), pygame.image.load("./assets/gap_1.png").convert_alpha(), pygame.image.load("./assets/gap_3.png").convert_alpha()]
        self.imagePlatform = [pygame.image.load("./assets/roof_1.png").convert_alpha(), pygame.image.load("./assets/roof_2.png").convert_alpha(), pygame.image.load("./assets/roof_3.png").convert_alpha(), pygame.image.load("./assets/roof_4.png").convert_alpha(), pygame.image.load("./assets/roof_5.png").convert_alpha()]
        self.imageBig = [pygame.image.load("./assets/lj1.png").convert_alpha(), pygame.image.load("./assets/lj2.png").convert_alpha()]
        
        self.imageTextPause = pygame.image.load("./assets/text_pause.png").convert_alpha()#PAUSE CODE
        self.imageTextResume = pygame.image.load("./assets/text_resume.png").convert_alpha()#PAUSE CODE
        self.imageKeyEscape = pygame.image.load("./assets/key_escape.png").convert_alpha()#PAUSE CODE
        self.imagePauseBack = pygame.image.load("./assets/pause_back.png").convert_alpha()#PAUSE CODE
        self.imageQuit = pygame.image.load("./assets/button_quit_0.png").convert_alpha()#PAUSE CODE

        self.platformGroup = pygame.sprite.Group()
        self.platformGroup.add(Platform(x=0, y=0, image=self.imagePlatform[random.randint(0, 4)]))
        self.platformGroup.add(Platform(x=640, y=0, image=self.imagePlatform[random.randint(0, 4)]))
        self.platformGroup.add(Platform(x=1280, y=0, image=self.imagePlatform[random.randint(0, 4)]))
        self.platformGroup.add(Platform(x=1920, y=0, image=self.imagePlatform[random.randint(0, 4)]))
        
        self.music = mixer.music.load("./assets/boss2.mp3")

        self.bumperGroup = pygame.sprite.Group()

        self.player = Player(200, 710)
        self.thief = Thief(1000, 744)

        self.tick = 0

        self.speed = 10
        self.thiefSpeed = 10
        self.fargroundSpeed = 2
        self.frontgroundSpeed = 10
        self.fargroundX = 0
        self.frontgroundX = 0
        self.anim = 0

        self.g = 9.81
        self.currentSpeed = 0
        self.thiefCurrentSpeed = 0
        self.nextPlatformHeight = 768

        self.isJumping = False
        self.needToFall = True
        self.thiefisJumping = False
        self.thiefNeedToFall = True

        self.ending = False
        self.badEnd = False
        self.goodEnd = False
        self.onPause = False #PAUSE CODE
        self.isPausing = False #PAUSE CODE
        self.thiefAnim = 0
        
        self.longJumpState = False
        self.thiefLongJumpState = False

        self.thiefTickSmallJump = 0
        self.thiefTickLongJump = 0
        self.thiefPosListLongJump = [572 ,534 ,497 ,462 ,428 ,396 ,365 ,336 ,308 ,282 ,257 ,234 ,212 ,192 ,173 ,156 ,140 ,126 ,113 ,102 ,92 ,84 ,77 ,72 ,68 ,66 ,65 ,65 ,65 ,66 ,68 ,71 ,75 ,80 ,86 ,93 ,101 ,110 ,120 ,131 ,143 ,156 ,170 ,185 ,201 ,218 ,236 ,255 ,275 ,296 ,318 ,341 ,365 ,390 ,416 ,443 ,471 ,500 ,530 ,561 ,593 ,626 ,660, 710, 744]
        self.thiefPosListSmallJump = [743,718,684,658,658,632,632,635,612,612,614,593,593,596,578,578,580,564,564,567,554,554,556,545,545,548,540,540,542,536,536,539,536,536,538,537,537,538,538,538,540,542,542,544,548,548,550,556,556,558,566,566,568,578,578,580,592,592,594,608,608,610,626,626,628,646,646,648,668,668,670,692,692,694,718,718,744]
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
                self.speed = 15
            self.player.collisionBox.y = self.player.rect.y

    def ThiefFall(self):
        self.thief.collisionBox.y += 5
        self.thiefNeedToFall = True
        for platform in self.platformGroup.sprites():
            for collision in platform.allCollision:
                if self.thief.collisionBox.colliderect(collision):
                    self.thiefNeedToFall = False
        self.thief.collisionBox.y = self.thief.rect.y

    def ThiefSmallJump(self):
        if self.thiefisJumping and not self.onPause:
            self.thief.setYPos(self.thiefPosListSmallJump[self.thiefTickSmallJump])
            self.thief.collisionBox.y = self.thiefPosListSmallJump[self.thiefTickSmallJump]
            self.thiefTickSmallJump += 3
            if self.thiefTickSmallJump >= len(self.thiefPosListSmallJump) - 2:
                self.thiefisJumping = False
                self.thief.setYPos(744)
                self.thief.collisionBox.y = 744
        else:
            self.thiefTickSmallJump = 0

    def platformMovement(self):
        for platform in self.platformGroup.sprites():
            platform.collision.x -= self.speed
            platform.jumpSurfaceCollision.x -= self.speed
            for collision in platform.allCollision:
                collision.x -= self.speed

    def bumperMovement(self):
        for bumper in self.bumperGroup.sprites():
            bumper.collision.x -= self.speed

    def deleteBumper(self, platformName):
        if platformName == "long":
            self.bumperGroup.remove(self.bumperGroup.sprites()[0])

    def bumperCollision(self):
            for bumper in self.bumperGroup.sprites():
                if self.player.collisionBox.colliderect(bumper.collision) and not self.longJumpState and not self.ending:
                    self.saveSpeed = self.speed
                    self.speed = 0
                    self.frontgroundSpeed = 0
                    self.fargroundSpeed = 0

                    self.bumperAnim = 1

                    self.longJumpState = True
                    bumper.collidedWithBumper = True

                    self.player.rect.y -= 100
                    self.player.collisionBox.y -= 100

                if self.thief.collisionBox.colliderect(bumper.collision):
                    self.thiefTickLongJump = 0
                    self.thiefLongJumpState = True
                    bumper.collidedWithBumper = True
                    self.thief.rect.y -= 100
                    self.thief.collisionBox.y -=100
                    self.thiefCurrentSpeed = defineSpeedWithAngle(-45, self.thiefSpeed)[1]
                    self.thiefSpeed = defineSpeedWithAngle(45, self.thiefSpeed)[0]

    def HoleCollision(self):
        for platform in self.platformGroup.sprites():
            if platform.name == "small" and not self.thiefisJumping and not self.thiefLongJumpState:
                if self.thief.collisionBox.colliderect(platform.jumpSurfaceCollision):
                    self.thiefTickSmallJump = 0
                    self.thiefisJumping = True

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
                                        
                self.player.setYPos(ySerieBasicJump(5, self.player.rect.y, self.currentSpeed, self.speed/20)[0])
                self.player.collisionBox.y = ySerieBasicJump(5, self.player.rect.y, self.currentSpeed, self.speed/20)[0]

                self.angle = 20

    def longJump(self):
        if self.longJumpState and self.needToFall and not self.onPause and self.speed != 0 and self.player.rect.y < 800:
            self.player.setYPos(ySerieBasicJump(5, self.player.rect.y, self.currentSpeed,self.speed/20)[0]) 
            self.player.collisionBox.y = ySerieBasicJump(5, self.player.rect.y, self.currentSpeed, self.speed/20)[0]
            self.currentSpeed = ySerieBasicJump(5, self.player.rect.y, self.currentSpeed, self.speed/20)[1]
            if self.bumperAnim < 6:
                self.bumperAnim += 1
        elif self.longJumpState and not self.onPause and self.speed != 0:
                self.player.setYPos(710)
                self.player.collisionBox.y = 710
                self.currentSpeed = 0
                self.speed = 10
                self.fargroundSpeed = 2
                self.frontgroundSpeed = 10
                self.longJumpState = False
        elif self.longJumpState and not self.onPause and self.player.rect.y > 800:
            self.longJumpState = False

    def playerAndThiefCollison(self):
        if (self.player.collisionBox.colliderect(self.thief.collisionBox)):
            self.goodEnd = True

    def thiefLongJump(self):
        if self.thiefLongJumpState and not self.onPause and self.speed != 0:
            self.thief.setYPos(self.thiefPosListLongJump[self.thiefTickLongJump])
            self.thief.collisionBox.y = self.thiefPosListLongJump[self.thiefTickLongJump]
            if self.tick % 2 == 0:
                self.thiefTickLongJump += 1
            if self.thiefTickLongJump == len(self.thiefPosListLongJump):
                self.thiefLongJumpState = False
        elif self.speed != 0:
            self.thiefTickLongJump = 0


    def updateThiefPosition(self):
        if self.tick % 5 == 0 and self.speed != 0 and not self.ending:
            self.thief.rect.x += - 0.5 * self.speed + 4
            self.thief.collisionBox.x += - 0.5 * self.speed + 4
        if self.ending:
            self.thief.rect.x += 5
            self.thief.collisionBox.x += 5
            if self.thief.rect.x > 1920:
                self.badEnd = True

    def createNewPlatform(self, delta):
        self.platfomType = [
            Platform(x=1920-delta, y=0, image=self.imagePlatform[random.randint(0, 4)]),
            SmallJump(x=1920-delta, y=0, image=self.imageSmall[random.randint(0, 2)]),
            LongJump(x=1920-delta, y=0, image=self.imageBig[random.randint(0, 1)]),
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

    def thieffallingPosition(self):
        self.thief.setYPos(ySerieBasicJump(5, self.thief.rect.y, self.thiefCurrentSpeed, self.thiefSpeed / 20)[0])
        self.thief.collisionBox.y = ySerieBasicJump(5, self.thief.rect.y, self.thiefCurrentSpeed, self.thiefSpeed / 20)[0]

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
                mixer.music.stop()
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

        if not self.ending:
            self.fargroundX = (self.fargroundX-self.fargroundSpeed)%-3072
            self.frontgroundX = (self.frontgroundX-self.frontgroundSpeed)%-3072

        #pygame.draw.rect(self.screen, (255, 0, 0), self.thief.collisionBox)

        if self.isJumping:
            self.screen.blit(self.player.images[0], self.player.getCoordinates())
        else:
            self.screen.blit(self.player.images[self.anim%4], self.player.getCoordinates())
        if self.tick % (10-(self.speed//5)) == 0 and self.speed != 0 and not self.onPause:
            self.anim += 1

        if self.thiefisJumping or self.thiefLongJumpState:
            self.screen.blit(self.thief.image[0], self.thief.getCoordinates())
        else:
            self.screen.blit(self.thief.image[self.thiefAnim%4], self.thief.getCoordinates())

        if self.tick % 5 == 0 and self.speed != 0:
            self.thiefAnim += 1

        for platform in self.platformGroup.sprites():
            self.screen.blit(platform.image, platform.getCordinates())
            #pygame.draw.rect(self.screen, (255, 0, 0), platform.jumpSurfaceCollision)

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

    def run(self):
        mixer.music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.tick = (self.tick+1)%60

            self.longJump()
            self.thiefLongJump()


            if self.goodEnd:
                self.running = False
                mixer.music.fadeout(1)
                mixer.music.stop()
                goodEndMenu().run()
            elif self.badEnd:
                self.running = False
                mixer.music.fadeout(1)
                mixer.music.stop()
                badEndMenu().run()
            elif not self.ending:
                self.thiefLongJump()
                self.refreshScreen()
                self.updateNewPlatform()
                self.platformMovement()
                self.bumperMovement()
                self.isKeySpacePressed()
                self.bumperCollision()
                self.fall()
                self.playerAndThiefCollison()
                self.ThiefFall()
                self.HoleCollision()
                self.ThiefSmallJump()
                self.updateThiefPosition()
            elif self.ending:
                self.thiefLongJump()
                self.refreshScreen()
                self.updateNewPlatform()
                self.ThiefFall()
                self.ThiefSmallJump()
                self.HoleCollision()
                self.bumperCollision()
                self.updateThiefPosition()
                self.fallingPosition()

            self.clock.tick(60)
