class Door:
    def __init__(self):
        self.is_closed = True

    def toggle(self):
        self.is_closed = not self.is_closed