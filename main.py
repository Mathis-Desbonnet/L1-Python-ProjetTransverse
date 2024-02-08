import pygame
from player import Player
from plateform import Platform

class Main():
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1920, 1080))
        self.running = True
        self.player = Player()
        self.platform = Platform()
        
    def draw(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (100, 100, 100, 100))
        
    def refreshScreen(self):
        self.draw()
        pygame.display.flip()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                        
            self.refreshScreen()
Main().run()