import datetime
import gpiozero
import time
import tkinter as tk
import threading


class TimeCounter:
    def __init__(self, init_counter=0):
        self.counter = init_counter
        self.stat, self.break_loop = None, False

    def start(self):
        self.break_loop = False
        self.thread = threading.Thread(target=self.run_counter)
        self.thread.start()

    def run_counter(self):
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=self.counter*10)
        time_left = end_time - datetime.datetime.now()

        print("Start:%s, End:%s" % (start_time, end_time))
        self.dev.on()
        while time_left.total_seconds() > 0:
            time_left = end_time - datetime.datetime.now()
            self.stat = True
            if self.break_loop is True:
                print("count force stopped:")
                break
        self.stat = False
        self.dev.off()
        self.counter = 0

        print('Countdown ended:%s' % (datetime.datetime.now() - start_time), datetime.datetime.now())

    def add_time(self, t=0):
        self.counter = t

    def stop(self):
        self.break_loop = True

    def get_state(self):
        return self.stat


class MultiPressButton(TimeCounter):
    def __init__(self, master=None, ext_press=None, dev=None):
        self.press_duration, self.notpressed_duration, self.end_press = datetime.timedelta(0), datetime.timedelta(
            0), datetime.timedelta(0)
        self.command, self.master , self.dev= None, master, dev
        self.counter, self.ext_press = 0, ext_press
        TimeCounter.__init__(self, init_counter=0)

        self.thread = threading.Thread(target=self.button_monitor)
        self.thread.start()

    def button_monitor(self):
        t_int = 0.2

        while True:
            self.notpressed_duration = datetime.datetime.now() - self.end_press
            #print(self.ext_press)
            if self.ext_press.value is True:
                start_press_time = datetime.datetime.now()
                #self.dev.on()
                while self.ext_press.value is True:
                    t_now = datetime.datetime.now()
                    time.sleep(t_int / 2)
                    self.press_duration = t_now - start_press_time

                self.end_press = t_now
                self.press_conditions()
                #self.dev.off()

            elif self.ext_press.value is False:
                try:
                    if self.notpressed_duration.total_seconds() > 4 and self.command == 2:
                        print('exit prog mode')
                        self.command = 1
                        self.start()
                except AttributeError:
                    pass

            self.notpressed_duration = datetime.datetime.now() - self.end_press

    def press_conditions(self):
        try:
            self.notpressed_duration.total_seconds()
        except AttributeError:
            self.notpressed_duration = datetime.timedelta(seconds=0.01)

        print("button pressed for:[%f] seconds ; duration from last press:[%f] seconds " % (
            self.press_duration.total_seconds(), self.notpressed_duration.total_seconds()))

        # Reset press
        if self.press_duration.total_seconds() > 4:
            self.command, self.counter = 0, 0

        # Short press
        elif self.press_duration.total_seconds() < 0.5:
            # Add inc to counter is prog mode
            if self.command == 2 and self.notpressed_duration.total_seconds() < 3:
                self.counter += 1
                self.notpressed_duration = datetime.timedelta(0)
            # on/off
            else:
                self.command, self.counter = 1, 0

        # Enter program Mode
        elif 1 < self.press_duration.total_seconds() < 2.7:
            self.command = 2

        self.actions()

    def actions(self):
        if self.command == 0:
            print("Hard Reset")
            self.stop()
        elif self.command == 1:
            print("toggle on/off")
            self.dev.toggle()
            self.stat = not self.stat
        elif self.command == 2:
            print("prog mode:", self.counter)
            self.add_time(self.counter)
        print(self.stat)

    def sim_press(self, t1, t2=None):
        self.ext_press = True
        time.sleep(t1)
        self.ext_press = False
        if t2 is not None:
            time.sleep(t2)

    def get_status(self):
        return self.command


# class GUIButton(tk.Frame):
#     def __init__(self, master):
#         tk.Frame.__init__(self, master)
#         self.frame = tk.Frame(self)
#         self.frame.grid()
#         self.var = tk.IntVar()
#         self.button = tk.Button(self.frame, text='GUY', command=self.cb)
#         self.button.grid()
#
#     def cb(self):
#         print(self.var.get())

button = gpiozero.Button(20)
device = gpiozero.OutputDevice(26)

a = MultiPressButton(ext_press=button, dev=device)
#a.sim_press(0.3, 1)
#a.sim_press(0.5, 1)
#a.sim_press(2, 0.2)
#a.sim_press(0.5, 1)
#a.sim_press(0.5, 1)
#a.sim_press(0.5, 1)
#a.sim_press(0.5, 1)
#a.sim_press(0.5, 1)
#a.sim_press(0.5, 1)

# timer = TimeCounter()
# timer.add_time(3)
# timer.start()
# print(timer.get_state())
# time.sleep(1)
# # timer.add_time(3)
# # timer.start()
# timer.stop()
# time.sleep(1)
# timer.add_time(3)
# print(timer.get_state())
# timer.start()
#
# # time.sleep(2)
