import pygame
from pygame import mixer
from main import Main

class creditMenu:
    def __init__(self) -> None:
        mixer.init()
        
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True

        self.imageBack = pygame.image.load("./assets/sky_background.png").convert_alpha()
        self.imageLogo = pygame.image.load("./assets/logo_trans.png").convert_alpha()

        self.imageCredit = pygame.image.load("./assets/credits.png").convert_alpha()
        
        self.music = mixer.music.load("./assets/boss.mp3")
        self.launchGameSound = mixer.Sound("./assets/startButton_snd.mp3")

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

        if keys[pygame.K_SPACE] :
            self.running = False

    def draw(self):
        self.screen.blit(self.imageBack, (0, 0))
        # self.screen.blit(self.imagefarground1, (self.fargroundX1, 0))
        # self.screen.blit(self.imagefarground2, (self.fargroundX2, 0))
        # self.screen.blit(self.imagefrontground1, (self.frontgroundX1, 0))
        # self.screen.blit(self.imagefrontground2, (self.frontgroundX2, 0))
        self.screen.blit(self.imageLogo, (700, -25))  
        self.screen.blit(self.imageCredit, (700, 500))

        


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
creditMenu().run()