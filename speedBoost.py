import items

class speedboost(items.Items):
    def __init__(self, parent_screen):
        super().__init__(
            name="speedBoost",
            parent_screen=parent_screen,
            sprite="speedBoost.png"
        )

    def applySpeed(self, snakeSpeed, *args):
        bulletvel = None

        if snakeSpeed <= 0.05:
            print("Speed capped")
        else:
            snakeSpeed -= 0.01

            if len(args) == 2:
                bulletvel = args[1] + 0.1
        
        return snakeSpeed, bulletvel