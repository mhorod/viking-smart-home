from threading import Thread

from flask import Flask, jsonify, request, render_template

from weather import WeatherStation
from lcd import LCD
from beam import Beam


from dataclasses import dataclass
import time

from messages import *
from modules import *
from fireplace import *

class Display(Thread):
    def __init__(self, message_queue, modules):
        super().__init__()
        self.lcd = LCD()
        self.beam = Beam()
        self.weather_station = weather_station
        self.modules = modules
        self.message_queue = message_queue

        self.messages = []
        self.current_message = 0
        self.last_message_change = 0

    def run(self):
        while True:
            for module in self.modules:
                module.update()

            if time.time() - self.last_message_change > 4:
                self.next_message()
                self.last_message_change = time.time()
                
    def next_message(self):
        self.current_message += 1
        if self.current_message >= len(self.messages):
            self.messages = self.message_queue.get_messages()
            self.current_message = 0

        if len(self.messages) == 0:
            return

        msg = self.messages[self.current_message]
        self.lcd.display(msg.text)


drive_command = DriveCommand(0, 0)

app = Flask(__name__)
weather_station = WeatherStation()

robot = Robot(120)
beam = Beam()
fireplace = Fireplace()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/v1/weather')
def get_weather():
    return jsonify(weather_station.weather())

@app.route('/v1/drive', methods=["POST"])
def drive_robot():
    global drive_command
    drive = request.data
    x, y = drive[0], drive[1]
    drive_command = DriveCommand(x, y)
    if (x, y) != (0, 0):
        robot.manual_driving()
    return ""

@app.route('/v1/drive', methods=["GET"])
def get_robot_drive():
    command = drive_command
    if robot.auto_driving:
        cmd = robot.get_current_command()
        if cmd is not None:
            command = cmd
    return jsonify(command)

@app.route('/v1/beam', methods=["GET"])
def get_beam():
    return "1" if beam.obstacle_detected() else "0"


@app.route('/v1/scheduleFireplace', methods=['POST'])
def schedule_fireplace():
    fireplace.scheduled.append(request.data.decode("utf-8"))
    return ""

@app.route('/v1/scheduleFireplace', methods=['DELETE'])
def unschedule_fireplace():
    fireplace.scheduled.remove(request.data.decode("utf-8"))
    return ""

@app.route('/v1/scheduledFireplace', methods=['GET'])
def scheduled_fireplace():
    return jsonify(fireplace.scheduled)

@app.route('/v1/stuck', methods=['POST'])
def robot_got_stuck():
    robot.stuck = request.data.decode("utf-8") == "1"
    return ""

@app.route('/v1/gatheringFinished')
def gathering_finished():
    robot.finish_gathering_wood()
    return ""

message_queue = MessageQueue()
modules = [
    WeatherMonitor(message_queue, weather_station),
    CoffeeSuggestor(message_queue, weather_station, 997, 300, 120),
    KeyDetector(message_queue, 3600, 300),
    TemperatureMonitor(weather_station, robot, 30),
    RobotMonitor(message_queue, robot),
    #InstagramLikersMonitor(message_queue)
]

display = Display(message_queue, modules)
display.start()
app.run(port=8000, host="0.0.0.0")
