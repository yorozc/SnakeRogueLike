import pygame 
from pygame.locals import *
import time
from numpy import random

SIZE = 40
SURFACE_X = SIZE * 25 # 1000
SURFACE_Y = SIZE *20 # 800
TEXT_COL = (255,255,255)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.apple = pygame.transform.scale(self.apple, (SIZE, SIZE))
        self.appleRect = self.apple.get_rect()
        self.appleRect.x = random.randint(0,24)*SIZE
        self.appleRect.y = random.randint(0,19)*SIZE

    def draw(self):
        pygame.draw.rect(self.parent_screen, (255, 0, 255), self.appleRect)
        self.parent_screen.blit(self.apple, self.appleRect)

    def move(self):
        self.appleRect.x = random.randint(0,24)*SIZE
        self.appleRect.y = random.randint(0,19)*SIZE
        self.draw()

class Snake():
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.speed = 40
        self.snakeSound = pygame.mixer.Sound("resources/snake-hiss-95241.mp3")
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block = pygame.transform.scale(self.block, (SIZE, SIZE))
        self.snakeRect = self.block.get_rect()
        self.snakeRect.topleft = (0, 0)
        self.direction = 'right'
        self.body = []
        self.body.append(self.snakeRect)
        

    def increaseLength(self): #increments length and adds one to sprite group
        self.length += 1

        tail = self.body[-1] #most recently made element

        if self.direction == 'up':
            new_pos = (tail.x, tail.y + SIZE)
        if self.direction == 'down':
           new_pos = (tail.x, tail.y - SIZE)
        if self.direction == 'left':
            new_pos = (tail.x + SIZE, tail.y)
        if self.direction == 'right':
            new_pos = (tail.x - SIZE, tail.y)

        new_part = self.block.get_rect(topleft=new_pos)
        self.body.append(new_part)

    def draw(self):
        self.parent_screen.fill((25,52,105)) #clears screen so blocks don't save from last movement
        for i in range(self.length):
            pygame.draw.rect(self.parent_screen, (0, 255, 255), self.body[i])
            self.parent_screen.blit(self.block, self.body[i])


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
    
    
    def walk(self): #controls snake auto walk and the parts behind the head (self.body[0])
        
        for i in range(self.length-1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y

        if self.direction == 'up':
            self.body[0].y -= self.speed
        if self.direction == 'down':
            self.body[0].y += self.speed
        if self.direction == 'left':
            self.body[0].x -= self.speed
        if self.direction == 'right':
            self.body[0].x += self.speed

        self.draw()
        
class Game:
    def __init__(self):
        pygame.init() 
        self.surface = pygame.display.set_mode((SURFACE_X, SURFACE_Y))
        self.font = pygame.font.SysFont("arialblack", 30)
        pygame.mixer.init()
        self.playBackgroundMusic()
        self.surface.fill((25,52,105))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play(self):
        self.snake.walk() #snake auto walk
        self.apple.draw()
        self.displayScore()
        
        if self.is_collision(self.snake.snakeRect, self.apple.appleRect):
            self.playSound("ding")
            self.snake.increaseLength()
            self.apple.move()

        #snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.snakeRect, self.snake.body[i]):
                self.playSound("crash")
                raise "Game Over"

        #snake going out of bounds
        if self.snake.snakeRect.x < 0 or self.snake.snakeRect.x > SURFACE_X or self.snake.snakeRect.y < 0 or self.snake.snakeRect.y > SURFACE_Y:
            self.playSound("crash")
            raise "Game Over"    

    #used to draw text 
    def drawText(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.surface.blit(img, (x,y))

    def playBackgroundMusic(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

    def playSound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        sound.set_volume(0.1)
        pygame.mixer.Sound.play(sound)

    def showGameOver(self):
        pygame.mixer.music.pause()
        self.surface.fill((25,52,105))
        #font = pygame.font.SysFont('arialblack', 30)
        line1 = self.font.render(f"GAME OVER! Your score is {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (100, 300))
        line2 = self.font.render(f"To play again press Enter. To exit press Escape!", True, (255,255,255))
        self.surface.blit(line2, (100,350))
        pygame.display.flip()

    def displayScore(self):
        #font = pygame.font.SysFont('arialblack', 30)
        score = self.font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score, (800,10))
            
    #checks for collision between player and item
    def is_collision(self, rect1, rect2):
        if rect1.colliderect(rect2):
            return True
        return False
    
    #resets snake and apple spawn when player decides to retry
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True #game runs
        pause = False #controls whether game is paused
        while(running):
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause = True
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.rewind()
                        self.playBackgroundMusic()
                        pause = False
                        self.reset()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.moveUp()

                        if event.key == K_DOWN:
                            self.snake.moveDown()

                        if event.key == K_RIGHT:
                            self.snake.moveRight()

                        if event.key == K_LEFT:
                            self.snake.moveLeft()

                        if event.key == K_s:
                            self.snake.hiss()

                    else:
                        print("Game is paused")
                        self.drawText("Game is paused", self.font, (255,255,255), 100, 250)
                        pygame.display.flip()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()
                    pygame.display.flip()

            except Exception as e:

                self.showGameOver()
                pause = True

            time.sleep(0.2) 

if __name__ == "__main__": #main func
    game = Game()
    game.run()