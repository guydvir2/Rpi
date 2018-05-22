import datetime
import gpiozero
from signal import pause
import time


class MultiPressButton:
    def __init__(self, master):
        self.press_time, self.released_time , self.last_released_time, self.end_press= datetime.timedelta(0), datetime.timedelta(0), datetime.timedelta(0), datetime.timedelta(0)
        self.status, self.command, self.master = None, None, master
        self.counter, self.state =0, 0
        self.button_monitor()

    def button_monitor(self):
        t_int=0.2
        while True:
            self.released_time =datetime.datetime.now() - self.end_press
            if self.master.value is True:
                start_press_time = datetime.datetime.now()
                while self.master.value is True:
                    t_now= datetime.datetime.now()
                    time.sleep(t_int/2)
                    self.press_time = t_now - start_press_time
                    
                print("press duration:", self.press_time.total_seconds())
                self.end_press = t_now
                self.press_conditions()

    def press_conditions(self):
        try:
            self.released_time.total_seconds()
        except AttributeError:
            self.released_time = datetime.timedelta(seconds=0.01)

        print(self.released_time.total_seconds())
        # Reset
        if self.press_time.total_seconds() > 4:
            self.command = 0#, datetime.timedelta(0), datetime.timedelta(0)
            print(self.command)
            
        #standard press
        elif self.press_time.total_seconds() < 0.5:
            if self.command == 2 and self.released_time.total_seconds() < 3:
                self.counter +=1
                print("counter is:",self.counter)
                self.released_time = datetime.timedelta(0)
            else:
                self.command, self.counter = 1,0
                print(self.command)

        # Enter program Mode
        elif 1< self.press_time.total_seconds() < 2.7:
            self.command = 2
            print(self.command)
            
def print_hi():
    print("hi")
    
button = gpiozero.Button(20)
a=MultiPressButton(button)

print("KAKI")

pause()
