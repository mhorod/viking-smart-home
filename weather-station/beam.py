import RPi.GPIO as GPIO
import board

class Beam:
    def __init__(self):
        self.pin = 23
        GPIO.setup(self.pin, GPIO.IN)

    def obstacle_detected(self):
        return GPIO.input(self.pin) == 0
