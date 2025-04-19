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
        surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def isClicked(self, event, mouseRelease):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouseRelease:
            if self.rect.collidepoint(event.pos):
                return True
        return False
