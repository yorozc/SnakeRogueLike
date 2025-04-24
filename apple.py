import items

class Apple(items.Items):
    def __init__(self, parent_screen):
        super().__init__(
            name="Apple",
            parent_screen=parent_screen,
            sprite = "apple.jpg"
        )