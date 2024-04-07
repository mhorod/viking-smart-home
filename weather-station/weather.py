from dataclasses import dataclass

import board
import adafruit_dht
from bmp280 import BMP280
from smbus import SMBus

@dataclass
class Weather:
    temperature: float
    humidity: float
    pressure: float

class WeatherStation:
    def __init__(self):
        self.dht = adafruit_dht.DHT11(board.D17)
        self.bmp280 = bmp280 = BMP280(i2c_dev=SMBus(1))

        self.last_humidity = None

    def temperature(self):
        return self.bmp280.get_temperature()

    def pressure(self):
        return self.bmp280.get_pressure()

    def humidity(self):
        try:
            self.last_humidity = self.dht.humidity
        except:
            pass

        return self.last_humidity

    def weather(self):
        return Weather(self.temperature(), self.humidity(), self.pressure())
