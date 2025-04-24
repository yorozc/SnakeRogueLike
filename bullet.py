import items

SIZE = 40
SURFACE_X = SIZE * 25 # 1000
SURFACE_Y = SIZE * 20 # 800
class Bullet(items.Items):
    def __init__(self, parent_screen, x, y, direction):
        super().__init__(
            name="bullet",
            parent_screen=parent_screen,
            sprite="bullet-export.png"
        )
        #x and y of snake head
        self.rect.x = x
        self.rect.y = y
        self._ammo = 0
        self.vel = 8
        self.direction = direction

    def collect(self):
        self._ammo += 1

    def getAmmo(self):
        return self._ammo

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.vel
        if self.direction == 'down':
            self.rect.y += self.vel
        if self.direction == 'left':
            self.rect.x -= self.vel
        if self.direction == 'right':
            self.rect.x += self.vel

    def is_off_screen(self):
        return self.rect.x < 0 or self.rect.x > SURFACE_X or self.rect.y < 0 or self.rect.y > SURFACE_Y
            