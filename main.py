import pygame 
from pygame.locals import *
import time
import math
from numpy import random
import button #button class
import apple #child of items class
import bullet
import speedBoost

#global variables
SIZE = 40
SURFACE_X = SIZE * 25 # 1000
SURFACE_Y = SIZE * 20 # 800
TEXT_COL = (255,255,255)

last_time = time.time()


class Snake(): #character
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
        self.last_move_time = time.time()
        self.move_delay = 0.15 #snake moves every 0.15 seconds
        self.bullets = []

    def increaseLength(self): #increments length and adds one rect to self.body array
        self.length += 1

        tail = self.body[-1] #most recently made element

        #controls spawn point of body part
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
        current_time = time.time()
        if current_time - self.last_move_time >= self.move_delay:
            self.last_move_time = current_time
        
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

    def shoot(self):
        bullet_x = self.body[0].centerx - 20
        bullet_y = self.body[0].top
        return bullet.Bullet(self.parent_screen, bullet_x, bullet_y, self.direction)

    def updateBullets(self):
        for bullet in self.bullets: #updates bullet direction
            bullet.update()
            
        for i in range(len(self.bullets)-1, -1, -1): #checks if bullets go out of screen
            if self.bullets[i].is_off_screen():
                self.bullets.pop(i)

        for bullet in self.bullets: #draws bullets
            bullet.draw()
                   
class Game:
    def __init__(self):
        pygame.init() 
        self.surface = pygame.display.set_mode((SURFACE_X, SURFACE_Y))
        self.font = pygame.font.SysFont("arialblack", 30)
        pygame.mixer.init()
        self.playBackgroundMusic()
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = apple.Apple(self.surface)
        self.apple.draw()
        self.newBullet = bullet.Bullet(self.surface, random.randint(0,24)*40, random.randint(0,19)*40, self.snake.direction)
        self.speedBoost = speedBoost.speedboost(self.surface)
        self.menu_state = "main" #when paused, menu state appears
        self.mouseReleased = True
        self.resumeBtn = self.buttonMaker(430, 200, "button_resume.png", 1)
        self.optionsBtn = self.buttonMaker(430, 275, "button_options.png", 1)
        self.exitBtn = self.buttonMaker(430, 350, "button_quit.png", 1)
        self.audioBtn = self.buttonMaker(430, 200, "button_audio.png", 1)
        self.backBtn = self.buttonMaker(430, 275, "button_back.png", 1)

    def play(self):
        self.renderBackground()
        self.snake.walk() #snake auto walk
        self.apple.draw()
        self.newBullet.draw()
        self.speedBoost.draw()
        self.snake.updateBullets()
        self.displayScore()
        
        # collision with apple
        if self.is_collision(self.snake.snakeRect, self.apple.rect):
            self.playSound("ding")
            self.snake.increaseLength()
            self.apple.move()

        if self.is_collision(self.snake.snakeRect, self.newBullet.rect):
            self.playSound("gun-reload")
            self.newBullet.reload()
            self.newBullet.move()

        if self.is_collision(self.snake.snakeRect, self.speedBoost.rect):
            self.playSound("lightning-strike")
            newSpeed,_ = self.speedBoost.applySpeed(self.snake.move_delay)
            self.snake.move_delay = newSpeed
            self.speedBoost.move()
        
        #bullet and apple collision
        for i in range(len(self.snake.bullets)):
            if self.is_collision(self.snake.bullets[i].rect, self.apple.rect):
                self.playSound("ding")
                self.snake.increaseLength()
                self.apple.move()
                self.snake.bullets.pop(i)

        for i in range(len(self.snake.bullets)):
            if self.is_collision(self.snake.bullets[i].rect, self.speedBoost.rect):
                self.playSound("lightning-strike")
                newSpeed, newVel = self.speedBoost.applySpeed(self.snake.move_delay, self.snake.bullets[i].vel)
                self.snake.move_delay = newSpeed
                self.snake.bullets[i].vel = newVel
                self.speedBoost.move()
                self.snake.bullets.pop(i)

        #snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.snakeRect, self.snake.body[i]):
                self.playSound("crash")
                raise "Game Over"

        #snake going out of bounds
        if self.snake.body[0].x < 0 or self.snake.body[0].x > SURFACE_X or self.snake.body[0].y < 0 or self.snake.body[0].y > SURFACE_Y:
            self.playSound("crash")
            raise "Game Over"    
    
    #maybe fix this or get rid of it, can't check collision this way
    def buttonMaker(self, x, y, img, scale): #will be used to load images for button instance
        image = pygame.image.load(f"resources/{img}").convert_alpha() #don't forget extension
        return button.Button(x, y, image, scale)
        
        
    def renderBackground(self):
        background = pygame.image.load("resources/background.jpg")
        self.surface.blit(background, (0,0))

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
        self.renderBackground()
        pygame.mixer.music.pause()
        line1 = self.font.render(f"GAME OVER! Your score is {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (100, 300))
        line2 = self.font.render(f"To play again press Enter. To exit press Escape!", True, (255,255,255))
        self.surface.blit(line2, (100,350))
        
    def displayScore(self):
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
        self.apple = apple.Apple(self.surface)

    def run(self):
        clock = pygame.time.Clock()
        running = True #game runs
        pause = False #controls whether game is paused
        game_over = False
        while(running):

            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    if event.type == pygame.MOUSEBUTTONUP:
                        self.mouseReleased = True

                    if event.key == K_ESCAPE and game_over == False: #pause game (brings up menu)
                        pause = True
                        game_over = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.rewind()
                        self.playBackgroundMusic()
                        pause = False
                        game_over = False
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

                        if event.key == K_SPACE:
                            if self.newBullet.getAmmo() <= 0:
                                self.playSound("gun-empty")
                                #message saying gun empty on screen
                            else:
                                self.playSound("gun-shot")
                                newBullet = self.snake.shoot() #instance of bullet class
                                self.snake.bullets.append(newBullet) #appending each obj to list
                                self.newBullet.shootAmmo()


                elif event.type == QUIT:
                    running = False

                if pause and game_over == False:
                    #self.drawText("PAUSED", self.font, (255,255,255), 450, 100)
                    #check menu state
                    if self.menu_state == "main":
                        if self.resumeBtn.isClicked(event, self.mouseReleased):
                            pause = False
                            
                        if self.optionsBtn.isClicked(event, self.mouseReleased):
                            self.menu_state = "options" #opens options menu

                        if self.exitBtn.isClicked(event, self.mouseReleased): #exit button
                            running = False

                    elif self.menu_state == "options":
                        if self.audioBtn.isClicked(event, self.mouseReleased):
                            pass

                        if self.backBtn.isClicked(event, self.mouseReleased):
                            self.menu_state = "main"

                    if self.menu_state == "main":
                        self.renderBackground()
                        self.resumeBtn.draw(self.surface)
                        self.optionsBtn.draw(self.surface)
                        self.exitBtn.draw(self.surface)

                    elif self.menu_state == "options":
                        self.renderBackground()
                        self.audioBtn.draw(self.surface)
                        self.backBtn.draw(self.surface)

            try:
                if not pause:
                    self.play()
                    
            except Exception as e: #when snake dies
                game_over = True
                pause = True
                self.showGameOver()

            pygame.display.flip()
            clock.tick(0) #uncapped

if __name__ == "__main__": #main func
    game = Game()
    game.run()