import time


class MultiPressButton:
    def __init__(self, master, status):
        self.press_time, self.released_time = None, None
        self.status, self.command, self.master = status, None, master

    def button_monitor(self):
        while True:
            if self.status is True:
                start_press_time = time.time()
                while self.status is True:
                    self.press_time = time.time() - start_press_time
                print(self.press_time)
            elif self.status is False:
                start_released_time = time.time()
                while self.status is False:
                    self.released_time = time.time() - start_released_time
                print(self.released_time)

            return self.press_time, self.released_time

    def press_conditions(self):
        if self.press_time > 3:
            self.command, self.press_time, self.released_time = 0, 0, 0
        if self.released_time > 3:
            self.command, self.press_time, self.released_time = 0, 0, 0

        if self.press_time < 0.5 and self.released_time < 2:
            self.command, self.press_time, self.released_time = 1, 0, 0
