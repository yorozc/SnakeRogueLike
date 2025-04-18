import pygame
# will be used to create and test buttons

class Button:
    def __init__(self, x, y, image, scale): # (x,y) determines pos, image = img path, scale = how big or small
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale))) #changes width&height
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) #determines pos
        self.clicked = False

    def draw(self, surface):
        action = False
        #mouse pos
        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
