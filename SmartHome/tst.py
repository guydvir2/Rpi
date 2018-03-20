from sys import platform

os_type = platform
if os_type == 'darwin':
    main_path = '/Users/guy/Documents/github/Rpi/'
elif os_type == 'win32':
    main_path = 'd:/users/guydvir/Documents/git/Rpi/'
elif os_type == 'linux':
    main_path = '/home/guy/Documents/github/Rpi/'

from sys import path

path.append(main_path + 'GPIO_Projects/lcd')
path.append(main_path + 'SmartHome')

import time
import threading
import signal
import datetime

import os

try:
    import gpiozero
    import use_lcd
    import LocalSwitch

    ok_modules = True

except ImportError:  # (ModuleNotFoundError,
    ok_modules = False
    print('Fail to obtain one or more modules')


class ShowStatusLCD:
    def __init__(self, switches, ext_log=None):
        self.switches = switches
        self.log = ext_log
        try:
            # Case of HW err
            self.lcd_display = use_lcd.MyLCD()
            self.t = threading.Thread(name='thread_disp_lcd', target=self.display_status_loop)
            self.t.start()
        except OSError:
            msg = "LCD hardware error"
            print(msg)
            self.log.append(msg)

    def display_status_loop(self):
        status = [[] for i in range(len(self.switches))]
        while True:
            t_stamp = datetime.datetime.now()
            t1, t2 = 0, 0

            while t1 < 10:
                for i, current_switch in enumerate(self.switches):
                    if current_switch.switch_state[0] is False:
                        status[i] = '%s :%s' % (current_switch.name, 'off')
                    elif current_switch.switch_state[0] is True:
                        status[i] = '%s :%s' % (current_switch.name, 'on ')

                    self.lcd_display.center_str(text1=str(status[0]), text2=str(status[1]))
                    time.sleep(1)
                    t1 = (datetime.datetime.now() - t_stamp).total_seconds()

            self.lcd_display.clear_lcd()
            while t2 < 15:
                self.show_time()
                t2 = (datetime.datetime.now() - t_stamp).total_seconds()

    def show_time(self):
        timeNow = str(datetime.datetime.now())[:-5].split(' ')
        self.lcd_display.center_str(text1=timeNow[0], text2=timeNow[1])


class Log2File:
    def __init__(self, filename, screen=0, time_in_log=0):
        self.detectOS()
        self.output2screen = screen
        self.time_stamp_in_log = time_in_log
        self.filename = self.path + filename
        self.check_logfile_valid()
        self.first_boot_entry()

    def time_stamp(self):
        t = str(datetime.datetime.now())[:-5]
        return t

    def detectOS(self):
        os_type = platform
        if os_type == 'darwin':
            self.path = '/Users/guy/Documents/github/Rpi/SmartHome/'
        elif os_type == 'win32':
            self.path = 'd:/users/guydvir/Documents/git/Rpi/SmartHome/'
        elif os_type == 'linux':
            self.path = '/home/guy/Documents/github/Rpi/SmartHome/'

    def first_boot_entry(self):
        msg = 'log start @%s' % (str(platform))
        self.append_log(msg)
        self.append_log('*' * len(msg))

    def check_logfile_valid(self):
        if os.path.isfile(self.filename) is True:
            self.valid_logfile = True
        else:
            open(self.filename, 'a').close()
            self.valid_logfile = os.path.isfile(self.filename)
            if self.valid_logfile is True:
                print('>>Log file %s was created successfully' % self.filename)
            else:
                print('>>Log file %s failed to create' % self.filename)

    def append_log(self, log_entry=''):
        if self.time_stamp_in_log == 1:
            msg = '[%s] %s' % (self.time_stamp(), log_entry)
        else:
            msg = '%s' % log_entry

        if self.valid_logfile is True:
            myfile = open(self.filename, 'a')
            myfile.write(msg + '\n')
            myfile.close()
        else:
            print('Log err')
        if self.output2screen == 1:
            print(msg)


def log_it(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        a.append_log("Shit")
        print(result)
        return result

    return wrapper


# Define Switch :(Output GPIO, Input GPIO, name=text, mode='toggle'/'press', ext_log=None)
file_logger = Log2File('Newlog.log', screen=0)
sw1 = LocalSwitch.LocSwitch(5,21, name='Relay#1', mode='toggle', ext_log=file_logger)
sw2 = LocalSwitch.LocSwitch(13,20, name='Relay#2', mode='toggle', ext_log=file_logger)

# Disp on LCD
ShowStatusLCD([sw1, sw2])
time.sleep(1)

# Make switch by code
sw1.switch_state = 1
time.sleep(5)
sw2.switch_state = 1

sw1.switch_state = 0
time.sleep(5)
sw2.switch_state = 0
