# fire_alarm.py
class FireAlarm:
    def __init__(self):
        self.fire_detected = False

    def activate_alarm(self):
        self.fire_detected = True