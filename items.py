import pygame
from pygame.locals import *
import random

class Items:
    def __init__(self, parent_screen, sprite):
        self.parent_screen = parent_screen
        self.sprite = pygame.image.load(f"resources/{sprite}").convert()
        self.sprite = pygame.transform.scale(self.sprite, (40, 40))
        self.spriteRect = self.sprite.get_rect()
        self.spriteRect.x = random.randint(0,24)*40
        self.spriteRect.y = random.randint(0,19)*40

    def draw(self): #draws item to screen
        pygame.draw.rect(self.parent_screen, (255, 0,255), self.spriteRect)
        self.parent_screen.blit(self.sprite, self.spriteRect)

    def move(self):
        self.spriteRect.x = random.randint(0,24)*40
        self.spriteRect.y = random.randint(0,19)*40
        self.draw()
