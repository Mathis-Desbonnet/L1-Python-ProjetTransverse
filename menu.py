import pygame
from pygame import mixer
from main import Main

class mainMenu:
    def __init__(self) -> None:
        mixer.init()
        
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True
        self.imageLaunch = pygame.image.load("./assets/button_play_0.png").convert_alpha()
        self.imageLaunch2 = pygame.image.load("./assets/button_play_1.png").convert_alpha()
        self.imageStory = pygame.image.load("./assets/button_story_0.png").convert_alpha()
        self.imageStory2 = pygame.image.load("./assets/button_story_1.png").convert_alpha()
        self.imageQuit = pygame.image.load("./assets/button_quit_0.png").convert_alpha()
        self.imageQuit2 = pygame.image.load("./assets/button_quit_1.png").convert_alpha()

        self.imageBack = pygame.image.load("./assets/sky_background.png").convert_alpha()
        self.imagefarground1 = pygame.image.load("./assets/farground_spr1.png").convert_alpha()
        self.imagefarground2 = pygame.image.load("./assets/farground_spr2.png").convert_alpha()
        self.imagefrontground1 = pygame.image.load("./assets/frontground_spr1.png").convert_alpha()
        self.imagefrontground2 = pygame.image.load("./assets/frontground_spr2.png").convert_alpha()
        self.imageLogo = pygame.image.load("./assets/logo_trans.png").convert_alpha()
        
        self.music = mixer.music.load("./assets/boss.mp3")

        self.clock = pygame.time.Clock()
        self.tick = 0
        self.buttonNbr = 0
        self.upIn = False
        self.downIn = False
        self.spaceIn = False

        self.fargroundSpeed = 1
        self.frontgroundSpeed = 2
        self.fargroundX1 = 0
        self.fargroundX2 = 3072
        self.frontgroundX1 = 0
        self.frontgroundX2 = 3072


    def isKeySpacePressed(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_DOWN] :
            if not self.downIn and self.buttonNbr < 2:
                self.buttonNbr += 1
                self.downIn = True
        else : self.downIn = False

        if keys[pygame.K_UP]:
            if not self.upIn and self.buttonNbr > 0:
                self.buttonNbr -= 1
                self.upIn = True
        else : self.upIn = False

        if keys[pygame.K_SPACE] :
            if not self.spaceIn :
                if self.buttonNbr == 0 : #Launch
                    mixer.music.fadeout(1)
                    Main().run()
                    self.running = False
                else : self.running = False #Quit game

    def draw(self):
        self.screen.blit(self.imageBack, (0, 0))
        self.screen.blit(self.imagefarground1, (self.fargroundX1, 0))
        self.screen.blit(self.imagefarground2, (self.fargroundX2, 0))
        self.screen.blit(self.imagefrontground1, (self.frontgroundX1, 0))
        self.screen.blit(self.imagefrontground2, (self.frontgroundX2, 0))
        self.screen.blit(self.imageLogo, (700, -25))  


        if self.fargroundX1 <= -3072 : self.fargroundX1 = 3072
        if self.fargroundX2 <= -3072 : self.fargroundX2 = 3072

        self.fargroundX1 = (self.fargroundX1-self.fargroundSpeed)
        self.fargroundX2 = (self.fargroundX2-self.fargroundSpeed)

        if self.frontgroundX1 <= -3072 : self.frontgroundX1 = 3072
        if self.frontgroundX2 <= -3072 : self.frontgroundX2 = 3072

        self.frontgroundX1 = (self.frontgroundX1-self.frontgroundSpeed)
        self.frontgroundX2 = (self.frontgroundX2-self.frontgroundSpeed)

        if self.buttonNbr == 0 :
            self.screen.blit(self.imageLaunch2, (600, 506))
            self.screen.blit(self.imageStory, (600, 656))
            self.screen.blit(self.imageQuit, (600, 806))
        elif self.buttonNbr == 1 :
            self.screen.blit(self.imageLaunch, (600, 506))
            self.screen.blit(self.imageStory2, (600, 656))
            self.screen.blit(self.imageQuit, (600, 806))
        else :
            self.screen.blit(self.imageLaunch, (600, 506))
            self.screen.blit(self.imageStory, (600, 656))
            self.screen.blit(self.imageQuit2, (600, 806))


    def refreshScreen(self):
        self.draw()
        pygame.display.flip()

    def run(self):
        mixer.music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.tick = (self.tick+1)%60

            self.refreshScreen()
            self.isKeySpacePressed()

            self.clock.tick(60)