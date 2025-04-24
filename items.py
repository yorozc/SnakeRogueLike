import pygame
from pygame.locals import *
import random

class Items:
    def __init__(self, name, parent_screen, sprite):
        self.parent_screen = parent_screen
        self.name = name
        self.sprite = pygame.image.load(f"resources/{sprite}").convert()
        self.sprite = pygame.transform.scale(self.sprite, (40, 40))
        self.rect = self.sprite.get_rect()

    def draw(self): #draws item to screen
        pygame.draw.rect(self.parent_screen, (255, 0,255), self.rect)
        self.parent_screen.blit(self.sprite, self.rect)

    def move(self): #used for spawning
        self.rect.x = random.randint(0,24)*40
        self.rect.y = random.randint(0,19)*40
        self.draw()

    def use(self):
        pass
