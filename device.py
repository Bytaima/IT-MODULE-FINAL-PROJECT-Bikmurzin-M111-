from door import Door

class Device:
    def __init__(self, name):
        self.name = name
        self.light = False
        self.temperature = 0

    def toggle_light(self):
        self.light = not self.light

    def set_temperature(self, temperature):
        self.temperature = temperature