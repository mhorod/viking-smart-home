import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

import adafruit_dht
from bmp280 import BMP280
from smbus import SMBus

import time

class LCD:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.lcd = character_lcd.Character_LCD_RGB_I2C(i2c, 16, 2)

    def display(self, text):
        self.clear()
        self.lcd.message = text

    def clear(self):
        self.lcd.clear()

