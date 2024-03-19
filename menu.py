import pygame


class Main:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True
        self.imageBack = pygame.image.load("./assets/sky_background.png").convert_alpha()
        self.clock = pygame.time.Clock()
        self.tick = 0
        self.buttonNbr = 0
        self.upIn = False
        self.downIn = False

    def isKeySpacePressed(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_DOWN] :
            if not self.downIn :
                self.buttonNbr += 1
                self.downIn = True
                print(self.buttonNbr)
        else : self.downIn = False

        if keys[pygame.K_UP]:
            if not self.upIn :
                self.buttonNbr -= 1
                self.upIn = True
                print(self.buttonNbr)
        else : self.upIn = False

        if keys[pygame.K_SPACE] :
            if not self.spaceIn :
                if buttonNbr == 0 :
                    print("Et là on passe au jeu :D")
                elif buttonNbr == 1 :
                    print("Il entre un poulet et ressort une tourte")

    def draw(self):
        self.screen.blit(self.imageBack, (0, 0))

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


Main().run()
