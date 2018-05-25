import datetime
# import gpiozero
# from signal import pause
import time
import tkinter as tk
import threading


class MultiPressButton:
    def __init__(self, master=None):
        self.press_duration, self.notpressed_duration, self.end_press = datetime.timedelta(0), datetime.timedelta(
            0), datetime.timedelta(0)
        self.command, self.master = None, master
        self.counter, self.ext_press = 0, None

        self.thread = threading.Thread(target=self.button_monitor)
        self.thread.start()

    def button_monitor(self):
        t_int = 0.2

        while True:
            self.notpressed_duration = datetime.datetime.now() - self.end_press
            if self.ext_press is True:
                start_press_time = datetime.datetime.now()
                while self.ext_press is True:
                    t_now = datetime.datetime.now()
                    time.sleep(t_int / 2)
                    self.press_duration = t_now - start_press_time

                print("press duration:", self.press_duration.total_seconds())
                self.end_press = t_now
                self.press_conditions()

            elif self.ext_press is False:
                try:
                    if self.notpressed_duration.total_seconds() > 3 and self.command == 2:
                        print('reset')
                        self.command = 0
                except AttributeError:
                    pass

    def press_conditions(self):
        try:
            self.notpressed_duration.total_seconds()
        except AttributeError:
            self.notpressed_duration = datetime.timedelta(seconds=0.01)

        print(self.notpressed_duration.total_seconds())

        # Reset
        if self.press_duration.total_seconds() > 4:
            self.command = 0
            print(self.command)
            return self.command

        # standard press
        elif self.press_duration.total_seconds() < 0.5:
            if self.command == 2 and self.notpressed_duration.total_seconds() < 3:
                self.counter += 1
                print("counter is:", self.counter)
                self.notpressed_duration = datetime.timedelta(0)
                return self.command, self.counter
            else:
                self.command, self.counter = 1, 0
                print(self.command)
                return self.command

        # Enter program Mode
        elif 1 < self.press_duration.total_seconds() < 2.7:
            self.command = 2
            print(self.command)
            return self.command

    def actions(self):
        if self.command = 0:
            pass
    def get_status(self):
        return self.command


class TimeCounter:
    def __init__(self, counter):
        self.counter = counter

    def start(self):
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=self.counter)
        time_left = end_time - datetime.datetime.now()
        while time_left.total_seconds() > 0:
            time_left = end_time - datetime.datetime.now()
            print(time_left)


class GUIButton(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(self)
        self.frame.grid()
        self.var = tk.IntVar()
        self.button = tk.Button(self.frame, text='GUY', command=self.cb)
        self.button.grid()

    def cb(self):
        print(self.var.get())


class FakeInput:
    def __init__(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        self.press(1.5, 0.5)
        self.press(0.5, 0.5)
        self.press(0.5, 0.5)
        self.press(0.5, 0.5)
        self.press(0.5, 0.5)
        self.press(0.5, 0.5)

    def press(self, t1, t2):
        self.value = True
        time.sleep(t1)
        self.value = False
        time.sleep(t2)


def fake_press(input_func):
    def wrapper():
        return 'hi'

    return wrapper()


# button = gpiozero.Button(20)
# c = FakeInput()

a = MultiPressButton()
last_state = None
a.ext_press = True
time.sleep(2)
a.ext_press = False
