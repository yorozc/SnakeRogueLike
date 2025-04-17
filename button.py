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
        self.clicked = False

    def draw(self):
        action = False
        #mouse pos
        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

    

start_button = Button(100, 200, start_img, 0.8)
exit_button = Button(450, 200, exit_img, 0.8)

def start_menu():
    img = pygame.image.load("resources/background.jpg")
    screen.blit(img, (0,0))

# game loop
run = True
while run: 

    screen.fill((202, 228, 241))
    
    if start_button.draw():
        start_menu()
    
    if exit_button.draw():
        print("Clicked exit")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()
