import pygame 
from pygame.locals import *

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snakeSound = pygame.mixer.Sound("resources/snake-hiss-95241.mp3")
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block_x = 100
        self.block_y = 100

    def draw(self):
        self.parent_screen.fill((25,52,105)) #clears screen so blocks don't save from last movement
        self.parent_screen.blit(self.block, (self.block_x,self.block_y))
        pygame.display.flip()

    def moveLeft(self):
        self.block_x -= 10
        self.draw()

    def moveDown(self):
        self.block_y += 10
        self.draw()

    def moveRight(self):
        self.block_x += 10
        self.draw()

    def moveUp(self):
        self.block_y -= 10
        self.draw()

    def hiss(self):
        pygame.mixer.Sound.play(self.snakeSound)

class Game:
    def __init__(self):
        pygame.init() 
        self.surface = pygame.display.set_mode((1000, 500))
        self.surface.fill((25,52,105))
        self.snake = Snake(self.surface)
        self.snake.draw()

    def run(self):
        running = True
        while(running):
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.moveUp()
                    if event.key == K_DOWN:
                        self.snake.moveDown()
                    if event.key == K_RIGHT:
                        self.snake.moveRight()
                    if event.key == K_LEFT:
                        self.snake.moveLeft()
                    if event.key == K_SPACE:
                        self.snake.hiss()
                elif event.type == QUIT:
                    running = False

if __name__ == "__main__":
    game = Game()
    game.run()