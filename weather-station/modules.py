from messages import *
from beam import *
from instagram import *
from robot import *

class CoffeeMessage(Message, HasTimeLimit):
    def __init__(self, time_to_live):
        super().__init__("COFFEEE!!!", "COFFEE_MESSAGE")
        self.time_to_live = time_to_live

    def get_time_to_live(self):
        return self.time_to_live


class CoffeeSuggestor:
    def __init__(self,
            message_queue, 
            weather_station, 
            pressure_threshold, 
            time_between_suggestions,
            suggesting_for
        ):
        self.last_time_coffee_suggested = 0
        self.message_queue = message_queue
        self.time_between_suggestions = time_between_suggestions
        self.suggesting_for = suggesting_for
        self.weather_station = weather_station
        self.pressure_threshold = pressure_threshold


    def update(self):
        if self.weather_station.pressure() <= self.pressure_threshold:
            if time.time() - self.last_time_coffee_suggested > self.time_between_suggestions:
                self.message_queue.push(CoffeeMessage(self.suggesting_for))
                self.last_time_coffee_suggested = time.time()


class WelcomeBackMessage(Message, HasTimeLimit):
    def __init__(self, time_to_live):
        super().__init__("Welcome back!!!", "WELCOME_BACK_MESSAGE")
        self.time_to_live = time_to_live

    def get_time_to_live(self):
        return self.time_to_live


class KeyDetector:
    def __init__(self, message_queue, min_time_between_greetings, greeting_for):
        self.message_queue = message_queue
        self.message_queue.set_type_limit("WELCOME_BACK_MESSAGE", 1)
        self.beam = Beam()
        self.keys_detected = self.beam.obstacle_detected()
        self.min_time_between_greetings = min_time_between_greetings
        self.greeting_for = greeting_for
        self.last_time_greeted = 0

    def update(self):
        if self.beam.obstacle_detected() and not self.keys_detected:
            if time.time() - self.last_time_greeted > self.min_time_between_greetings:
                self.message_queue.push(WelcomeBackMessage(self.greeting_for))

        self.keys_detected = self.beam.obstacle_detected()


class TemperatureMonitor:
    def __init__(self,
            weather_station, 
            robot,
            temperature_threshold, 
        ):
        self.weather_station = weather_station
        self.robot = robot
        self.temperature_threshold = temperature_threshold

    def update(self):
        if self.weather_station.temperature() < self.temperature_threshold:
            self.robot.gather_wood()

class WeatherMonitor:
    TEMPERATURE_MESSAGE = "TEMPERATURE_MESSAGE"
    HUMIDITY_MESSAGE = "HUMIDITY_MESSAGE"
    def __init__(self, message_queue, weather_station):
        self.message_queue = message_queue
        self.weather_station = weather_station
        self.message_queue.set_type_limit(WeatherMonitor.TEMPERATURE_MESSAGE, 1)
        self.message_queue.set_type_limit(WeatherMonitor.HUMIDITY_MESSAGE, 1)

    def update(self):
        weather = self.weather_station.weather()

        temperature_message = Message(
                f"{weather.temperature:.2f} C\n{weather.pressure:.2f} hPa", WeatherMonitor.TEMPERATURE_MESSAGE)
        self.message_queue.push(temperature_message)

        if weather.humidity is not None:
            humidity_message = Message(f"humidity: {weather.humidity:.1f}%", WeatherMonitor.HUMIDITY_MESSAGE)
            self.message_queue.push(humidity_message)


class LikersMessage(Message, HasTimeLimit):
    def __init__(self, text):
        super().__init__(text, "LIKERS_MESSAGE")

    def get_time_to_live(self):
        return 120

class InstagramLikersMonitor:
    def __init__(self, message_queue):
        self.message_queue = message_queue
        self.post_likers = PostLikers()
        self.last_time_likers_updated = 0
        self.update_interval = 300
        self.likers = []
    
    def update(self):
        if time.time() - self.last_time_likers_updated > self.update_interval:
            self.last_time_likers_updated = time.time()
            self.likers = self.post_likers.get_likers()

            for i in range(0, len(self.likers), 2):
                ppl = self.likers[i:i+2]
                text = "\n".join("<3 " + name for name in ppl)
                self.message_queue.push(LikersMessage(text))

class RobotSentForWoodMessage(Message, HasTimeLimit):
    def __init__(self, time_to_live):
        super().__init__("Iza Viking was\nsent for wood", "ROBOT_WOOD_MESSAGE")
        self.time_to_live = time_to_live

    def get_time_to_live(self):
        return self.time_to_live

class RobotCollectedWoodMessage(Message, HasTimeLimit):
    def __init__(self, time_to_live):
        super().__init__("Iza Viking was\ncollected wood", "ROBOT_WOOD_MESSAGE")
        self.time_to_live = time_to_live

    def get_time_to_live(self):
        return self.time_to_live

class RobotGotStuck(Message, HasTimeLimit):
    ROBOT_GOT_STUCK_MESSAGE = "ROBOT_GOT_STUCK_MESSAGE"
    def __init__(self, time_to_live):
        super().__init__("Iza Viking\ngot stuck", self.ROBOT_GOT_STUCK_MESSAGE)
        self.time_to_live = time_to_live

    def get_time_to_live(self):
        return self.time_to_live

class RobotMonitor:
    def __init__(self, message_queue, robot):
        self.message_queue = message_queue
        self.robot = robot
        self.message_queue.set_type_limit("ROBOT_SENT_FOR_WOOD", 1)
        self.message_queue.set_type_limit("ROBOT_GOT_STUCK_MESSAGE", 1)

        self.robot_gathering_wood = self.robot.gathering_wood
    
    def update(self):
        if self.robot.stuck:
            self.message_queue.push(RobotGotStuck(120))

        if self.robot.gathering_wood and not self.robot_gathering_wood:
            self.message_queue.push(RobotSentForWoodMessage(120))
        elif not self.robot.gathering_wood and self.robot_gathering_wood:
            self.message_queue.push(RobotCollectedWoodMessage(120))

        self.robot_gathering_wood = self.robot.gathering_wood

