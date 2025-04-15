import pygame 
from pygame.locals import *
import time
class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.snakeSound = pygame.mixer.Sound("resources/snake-hiss-95241.mp3")
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block_x = 100
        self.block_y = 100
        self.speed = 15
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill((25,52,105)) #clears screen so blocks don't save from last movement
        self.parent_screen.blit(self.block, (self.block_x,self.block_y))
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
        if self.direction == 'up':
            self.block_y -= self.speed
        if self.direction == 'down':
            self.block_y += self.speed
        if self.direction == 'left':
            self.block_x -= self.speed
        if self.direction == 'right':
            self.block_x += self.speed
        self.draw()

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