import items

class speedboost(items.Items):
    def __init__(self, parent_screen):
        super().__init__(
            name="speedBoost",
            parent_screen=parent_screen,
            sprite="speedBoost.png"
        )

    def applySpeed(self, snakeSpeed):

        if snakeSpeed <= 0.09:
            print("Speed capped")
        else:
            snakeSpeed -= 0.01
        
        return snakeSpeed