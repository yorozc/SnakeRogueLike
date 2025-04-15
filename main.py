import pygame 
from pygame.locals import *
import time

SIZE = 40

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.snakeSound = pygame.mixer.Sound("resources/snake-hiss-95241.mp3")
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block_x = [SIZE]*length
        self.block_y = [SIZE]*length
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill((25,52,105)) #clears screen so blocks don't save from last movement
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.block_x[i],self.block_y[i]))
        pygame.display.flip()

    def moveLeft(self):
        self.direction = 'left'

    def moveDown(self):
        self.direction = 'down'

    def moveRight(self):
        self.direction = 'right'

    def moveUp(self):
        self.direction = 'up'

    def hiss(self):
        pygame.mixer.Sound.play(self.snakeSound)
    
    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]

        if self.direction == 'up':
            self.block_y[0] -= SIZE
        if self.direction == 'down':
            self.block_y[0] += SIZE
        if self.direction == 'left':
            self.block_x[0] -= SIZE
        if self.direction == 'right':
            self.block_x[0] += SIZE

        self.draw()

class Game:
    def __init__(self):
        pygame.init() 
        self.surface = pygame.display.set_mode((1000, 500))
        self.surface.fill((25,52,105))
        self.snake = Snake(self.surface,2)
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
                        self.snake.direction = 'up'

                    if event.key == K_DOWN:
                        self.snake.moveDown()
                        self.snake.direction = 'down'

                    if event.key == K_RIGHT:
                        self.snake.moveRight()
                        self.snake.direction = 'right'

                    if event.key == K_LEFT:
                        self.snake.moveLeft()
                        self.snake.direction = 'left'

                    if event.key == K_SPACE:
                        self.snake.hiss()

                elif event.type == QUIT:
                    running = False

            self.snake.walk() #snake auto walk
            time.sleep(0.2)

if __name__ == "__main__":
    game = Game()
    game.run()