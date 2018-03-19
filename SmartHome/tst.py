import time
# import gpiozero
import threading
import signal
import datetime
from sys import path
from sys import platform
import os

path.append('/home/guy/Documents/github/Rpi/GPIO_Projects/lcd')
path.append('/home/guy/Documents/github/Rpi/SmartHome')


# import use_lcd
# import LocalSwitch


class ShowStatusLCD:
    def __init__(self, switches):
        self.switches = switches
        self.file_log = FileLog(filename='/home/guy/Documents/github/Rpi/SmartHome/loc_switch.log')
        try:
            # Case of HW err
            self.lcd_display = use_lcd.MyLCD()
            self.t = threading.Thread(name='thread_disp_lcd', target=self.display_status_loop)
            self.t.start()
        except OSError:
            msg = "LCD hardware error"
            print(msg)
            self.file_log.append(msg)

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
    def __init__(self, filename, screen=0):
        self.detectOS()
        self.output2screen = screen
        self.filename = self.path + filename
        self.check_logfile_valid()
        self.first_boot_entry()

    def time_stamp(self):
        t = str(datetime.datetime.now())[:-5]
        return t

    def detectOS(self):
        os_type = platform
        if os_type == 'darwin':
            self.path = '/Users/guyd/Documents/github/Rpi/SmartHome/'
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
        msg = '[%s] %s' % (self.time_stamp(), log_entry)
        if self.valid_logfile is True:
            myfile = open(self.filename, 'a')
            myfile.write(msg + '\n')
            myfile.close()
        else:
            print('Log err')
        if self.output2screen == 1:
            print(msg)


class TestClass:
    def __init__(self, ext_log=None):
        self.now = 'boot' + str(datetime.datetime.now())
        self.external_log = ext_log
        self.external_log.append_log('Start')

    def update(self):
        self.now = "time update: " + str(datetime.datetime.now())
        self.external_log.append_log(self.now)
        return self.now


def log_it(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        a.append_log("Shit")
        print(result)
        return result

    return wrapper


# # Define Switch :(Output GPIO, Input GPIO, name=text, mode='toggle'/'press')
# sw1 = LocalSwitch.LocSwitch(5, 21, name='Relay#1', mode='toggle')
# sw2 = LocalSwitch.LocSwitch(20, 13, name='Relay#2', mode='toggle')
#
# # Disp on LCD
# ShowStatusLCD([sw1, sw2])
# time.sleep(1)
#
# # Make switch by code
# sw1.switch_state = 1
# time.sleep(5)
# sw2.switch_state = 1
#
# sw1.switch_state = 0
# time.sleep(5)
# sw2.switch_state = 0

# a = FileLog('/Users/guy/log.log')

test = TestClass(ext_log=Log2File('log.log', screen=1))
time.sleep(5)
test.update()
time.sleep(0.2)
test.update()
