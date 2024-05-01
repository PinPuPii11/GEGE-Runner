import pygame
import sys
from button import Button

class IntroScreen:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("GEGE Runner")
        