import pygame


class Thief(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.rect = pygame.rect.Rect(x, y, 50, 140)

        self.collisionBox = pygame.rect.Rect(x, y, 50, 140)

        firstFrame = pygame.image.load("./assets/funkyThief_sheet.png").convert_alpha().subsurface((0, 0, 105, 105))
        secondFrame = pygame.image.load("./assets/funkyThief_sheet.png").convert_alpha().subsurface((105, 0, 105, 105))
        thirdFrame = pygame.image.load("./assets/funkyThief_sheet.png").convert_alpha().subsurface((210, 0, 105, 105))
        fourthFrame = pygame.image.load("./assets/funkyThief_sheet.png").convert_alpha().subsurface((315, 0, 105, 105))

        self.image = [firstFrame, secondFrame, thirdFrame, fourthFrame]

    def setYPos(self, y):
        self.rect.y = y

    def getCoordinates(self):
        return self.rect.x, self.rect.y
