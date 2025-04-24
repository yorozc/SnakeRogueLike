import items

class Apple(items.Items):
    def __init__(self, parent_surface):
        super().__init__(
            name="Apple",
            parent_screen=parent_surface,
            sprite = "apple.jpg"
        )