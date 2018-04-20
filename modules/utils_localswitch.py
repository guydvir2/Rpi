from sys import platform
import datetime
import time
import os
import threading
from socket import gethostname

try:
    #import my_paths
    import getip
    import gpiozero
    #import use_lcd
    import localswitches

    all_rpi_modules = True

except ImportError:
    all_rpi_modules = False
    print('Fail to obtain one or more RaspberryPi modules')
    quit()


class Output2LCD:
    """ This class outputs data to 2 lines of LCD matrix,
    parameters:
    1)switches - max of 2 lines od data
    2) ext_log - use class Log2File to save what displayed on LCD"""

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
            try:
                self.log.append_log(msg)
            except AttributeError:
                pass
            finally:
                print(msg)

    def display_status_loop(self):
        while True:
            self.disp_switch_status(time2show=3)
            self.disp_time(time2show=3)

    def disp_switch_status(self, time2show=2):
        # time to display relays status on LCD
        t1 = 0
        t_stamp = datetime.datetime.now()
        status = [[] for i in range(len(self.switches))]
        last_status = [[] for i in range(len(self.switches))]
        self.lcd_display.clear_lcd()

        while t1 < time2show:
            textonlcd = ['', '']
            for i, current_switch in enumerate(self.switches):
                # Detect change
                if last_status[i] != current_switch.switch_state[0]:
                    if current_switch.switch_state[0] is False:
                        s = 'off'
                    elif current_switch.switch_state[0] is True:
                        s = 'on '
                    status[i] = '%s :%s' % (current_switch.name, s)
                    try:
                        textonlcd[i] = str(status[i])
                        self.log.append_log(status[i], time_stamp=1)
                    except AttributeError:
                        pass
                    last_status[i] = current_switch.switch_state[0]
                    self.lcd_display.center_str(textonlcd[0], textonlcd[1])
            # take it easy :)
            time.sleep(0.5)
            t1 = (datetime.datetime.now() - t_stamp).total_seconds()

    def disp_time(self, time2show=5):
        t2 = 0
        t_stamp = datetime.datetime.now()
        self.lcd_display.clear_lcd()
        while t2 < time2show:
            time_now = str(datetime.datetime.now())[:-5].split(' ')
            self.lcd_display.center_str(text1=time_now[0], text2=time_now[1])
            t2 = (datetime.datetime.now() - t_stamp).total_seconds()


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
        # msg = 'log start @%s' % (str(platform))
        msg = '\nlog start @ %s, IP: %s, OS: %s' % (gethostname(), str(getip.get_ip()[0]), platform)
        self.append_log(msg)
        self.append_log('*' * len(msg))

    def check_logfile_valid(self):
        if os.path.isfile(self.filename) is True:
            self.valid_logfile = True
        else:
            open(self.filename, 'a').close()
            self.valid_logfile = os.path.isfile(self.filename)
            if self.valid_logfile is True:
                msg = '>>Log file %s was created successfully' % self.filename
            else:
                msg = '>>Log file %s failed to create' % self.filename
            print(msg)
            self.append_log(msg, time_stamp=1)

    def append_log(self, log_entry='', time_stamp=-1):
        # permanent time_stamp
        if time_stamp is -1:
            if self.time_stamp_in_log == 1:
                msg = '[%s] %s' % (self.time_stamp(), log_entry)
            else:
                msg = '%s' % log_entry
        # ADHOC time_stamp - over-rides permanent one
        elif time_stamp is 1:
            msg = '[%s] %s' % (self.time_stamp(), log_entry)
        elif time_stamp is 0:
            msg = '%s' % log_entry

        if self.valid_logfile is True:
            myfile = open(self.filename, 'a')
            myfile.write(msg + '\n')
            myfile.close()
        else:
            print('Log err')
        if self.output2screen == 1:
            print(msg)


class XTractLastLogEvent:
    def __init__(self, filename):
        self.fname = filename
        self.chopped_log = []
        self.read_logfile()

    def read_logfile(self):
        if os.path.isfile(self.fname) is True:
            with open(self.fname, 'r') as f:
                data_file = f.readlines()
                for line in reversed(data_file):
                    if 'log start' in line:
                        self.chopped_log.insert(0, line)
                        break
                    else:
                        self.chopped_log.insert(0, line)
        else:
            print('file', self.fname, ' not found')

    def xport_chopped_log(self):
        if self.chopped_log != []:
            return self.chopped_log
        else:
            return ('failed action')


if __name__ == "__main__":
    cut_log = XTractLastLogEvent(filename='/Users/guy/Documents/github/Rpi/SmartHome/2SingleSwitches.log')
    for i, line in enumerate(cut_log.xport_chopped_log()):
        print(i, line)
