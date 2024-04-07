import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.rect = pygame.rect.Rect(x, y, 50, 140)
        
        self.collisionBox = pygame.rect.Rect(x, y, 50, 140)
        
        firstFrame = pygame.image.load("./assets/player_sheet140.png").convert_alpha().subsurface((0, 0, 140, 140))
        secondFrame = pygame.image.load("./assets/player_sheet140.png").convert_alpha().subsurface((140, 0, 140, 140))
        thirdFrame = pygame.image.load("./assets/player_sheet140.png").convert_alpha().subsurface((280, 0, 140, 140))
        fourthFrame = pygame.image.load("./assets/player_sheet140.png").convert_alpha().subsurface((420, 0, 140, 140))
        
        self.images = [firstFrame, secondFrame, thirdFrame, fourthFrame]
        
    def setYPos(self, y):
        self.rect.y = y
        
    def getCoordinates(self):
        return self.rect.x, self.rect.y