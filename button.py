import pygame
# will be used to create and test buttons

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

#load button images
start_img = pygame.image.load('resources/start_btn.png').convert_alpha()
exit_img = pygame.image.load('resources/exit_btn.png').convert_alpha()

class Button:
    def __init__(self, x, y, image, scale): # (x,y) determines pos, image = img path, scale = how big or small
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale))) #changes width&height
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) #determines pos

    def draw(self):

        screen.blit(self.image, (self.rect.x, self.rect.y))

    

start_button = Button(100, 200, start_img, 0.8)
exit_button = Button(450, 200, exit_img, 0.8)


# game loop
run = True
while run: 

    screen.fill((202, 228, 241))
    start_button.draw()
    exit_button.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()
