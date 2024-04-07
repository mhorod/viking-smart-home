import time

class Robot:
    def __init__(self, min_time_between_gathering):
        self.stuck = False
        self.gathering_wood = False
        self.last_time_gathered_wood = 0
        self.min_time_between_gathering = min_time_between_gathering

    def gather_wood(self):
        if time.time() - self.last_time_gathered_wood < self.min_time_between_gathering:
            return
        self.last_time_gathered_wood = time.time()
        self.gathering_wood = True

    def finish_gathering_wood(self):
        self.gathering_wood = False
