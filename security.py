class SecuritySystem:
    def __init__(self):
        self.alarm_on = False

    def toggle_alarm(self):
        self.alarm_on = not self.alarm_on