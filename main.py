import pygame 
from pygame.locals import *
import time
from numpy import random

SIZE = 40
SURFACE_X = 1000
SURFACE_Y = 800

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE
        self.draw()

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.snakeSound = pygame.mixer.Sound("resources/snake-hiss-95241.mp3")
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block_x = [SIZE]*length #[40, 40, 40]
        self.block_y = [SIZE]*length
        self.direction = 'down'

    def increaseLength(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)

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
        self.surface = pygame.display.set_mode((SURFACE_X, SURFACE_Y))
        self.surface.fill((25,52,105))
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play(self):
        self.snake.walk() #snake auto walk
        self.apple.draw()

        if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.apple.x, self.apple.y):
            print("Collision occured")
            self.snake.increaseLength()
            self.apple.move()
            

    def is_collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
                return True
        return False 

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

            self.play()
            time.sleep(0.2)

if __name__ == "__main__":
    game = Game()
    game.run()