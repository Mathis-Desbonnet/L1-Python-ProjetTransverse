import pygame

class mainMenu:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True
        self.imageBack = pygame.image.load("./assets/sky_background.png").convert_alpha()
        self.imageLaunch = pygame.image.load("./assets/button_play_0.png").convert_alpha()
        self.imageLaunch2 = pygame.image.load("./assets/button_play_1.png").convert_alpha()
        self.imageStory = pygame.image.load("./assets/button_story_0.png").convert_alpha()
        self.imageStory2 = pygame.image.load("./assets/button_story_1.png").convert_alpha()
        self.imageQuit = pygame.image.load("./assets/button_quit_0.png").convert_alpha()
        self.imageQuit2 = pygame.image.load("./assets/button_quit_1.png").convert_alpha()

        self.clock = pygame.time.Clock()
        self.tick = 0
        self.buttonNbr = 0
        self.upIn = False
        self.downIn = False
        self.spaceIn = False

    def isKeySpacePressed(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_DOWN] :
            if not self.downIn and self.buttonNbr < 2:
                self.buttonNbr += 1
                self.downIn = True
                print(self.buttonNbr)
        else : self.downIn = False

        if keys[pygame.K_UP]:
            if not self.upIn and self.buttonNbr > 0:
                self.buttonNbr -= 1
                self.upIn = True
                print(self.buttonNbr)
        else : self.upIn = False

        if keys[pygame.K_SPACE] :
            if not self.spaceIn :
                if self.buttonNbr == 0 : #Launch
                    from main import Main
                    self.running = False
                elif self.buttonNbr == 1 : #Story
                    print("Il y entre un poulet et ressort une tourte")
                else : self.running = False #Quit game

    def draw(self):
        self.screen.blit(self.imageBack, (0, 0))
        if self.buttonNbr == 0 :
            self.screen.blit(self.imageLaunch2, (600, 300))
            self.screen.blit(self.imageStory, (600, 450))
            self.screen.blit(self.imageQuit, (600, 600))
        elif self.buttonNbr == 1 :
            self.screen.blit(self.imageLaunch, (600, 300))
            self.screen.blit(self.imageStory2, (600, 450))
            self.screen.blit(self.imageQuit, (600, 600))
        else :
            self.screen.blit(self.imageLaunch, (600, 300))
            self.screen.blit(self.imageStory, (600, 450))
            self.screen.blit(self.imageQuit2, (600, 600))


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
            self.isKeySpacePressed()

            self.clock.tick(60)


mainMenu().run()