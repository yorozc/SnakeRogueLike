import items

class Bullet(items.Items):
    def __init__(self, parent_surface):
        super().__init__(
            name="bullet",
            parent_screen=parent_surface,
            sprite="bullet-export.png"
        )
        self.ammo = 0

    def collect(self): 
        self.ammo += 1
        print(self.ammo)
    
    def shoot(self):
        if self.ammo <= 0:
            self.ammo = 0
            print(self.ammo)
        else:   
            self.ammo -= 1
            print(self.ammo)