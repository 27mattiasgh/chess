import time
import datetime
class Clock:
    def __init__(self):
        self.active = False 
        self.white = None
        self.black = None

    def start(self):
        while self.active is not None:
            if self.active == 'white': 
                self.white -= 0.1
            else: 
                self.black -= 0.1
                round(self.black, 1)
            time.sleep(0.1)

    def reset(self, time:int):
        self.active = 'white'
        self.white = self.black = time

    def swtich(self, player):
        if player == 'white':
            self.active = 'white'
        if player == 'black':
            self.active = 'black'

    def convert(self, seconds:int):
        return str(datetime.timedelta(seconds=seconds))
    