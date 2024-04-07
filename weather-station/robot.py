import time
from dataclasses import dataclass

@dataclass
class DriveCommand:
    x: int
    y: int

class Robot:
    def __init__(self, min_time_between_gathering):
        self.stuck = False
        self.gathering_wood = False
        self.last_time_gathered_wood = 0
        self.min_time_between_gathering = min_time_between_gathering
        self.auto_driving = False

        self.path = []
        self.cmd = 0

    def gather_wood(self):
        if time.time() - self.last_time_gathered_wood < self.min_time_between_gathering:
            return
        self.last_time_gathered_wood = time.time()
        self.gathering_wood = True
        self.auto_driving = True

        now = time.time()
        self.path = [
                (DriveCommand(1, 0), now + 10),
                (DriveCommand(0, 1), now + 15),
                (DriveCommand(2, 0), now + 25)
            ]
        self.cmd = 0

    def finish_gathering_wood(self):
        self.gathering_wood = False
        self.auto_driving = False

    def manual_driving(self):
        self.auto_driving = False
        self.path = []

    def get_current_command(self):
        if not self.auto_driving:
            return False

        if self.cmd >= len(self.path):
            self.path = []
            self.finish_gathering_wood()
            return

        now = time.time()
        if now > self.path[self.cmd][1]:
            self.cmd += 1

        if self.cmd >= len(self.path):
            self.path = []
            self.finish_gathering_wood()
            return

        return self.path[self.cmd][0]
