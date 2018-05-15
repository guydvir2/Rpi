import my_paths
import utils_localswitch
import localswitches
import time
import sys
from gmail_mod import GmailSender


# Define Switch :(Output GPIO, Input GPIO, name=text, mode='toggle'/'press', ext_log=None)
# Create a file logger to log outputs of switches

def load_services(log_file, dev_name):
    global file_logger, GmailDaemon, path, home

    os_type = sys.platform
    if os_type == 'darwin':
        home = '/Users/guy'
    elif os_type == 'win32':
        home = 'd:/users/guydvir'
    elif os_type == 'linux':
        home = '/home/guy'
    path = home + '/Documents/github/Rpi'

    file_logger = utils_localswitch.Log2File(home + '/Documents/' + log_file, screen=0, name_of_master=dev_name)
    GmailDaemon = GmailSender(sender_file=path + '/modules/ufile.txt', password_file=path + '/modules/pfile.txt')


def load_lcd():
    global lcd
    lcd = utils_localswitch.Output2LCD([double_switch.switch0, double_switch.switch1])  # , ext_log=file_logger)
    if lcd.boot_success is True:
        file_logger.append_log(log_entry='[LCD Display] detected and loaded OK')
    else:
        file_logger.append_log(log_entry='[LCD Display] not present/ driver error', time_stamp=1)


def load_HW_switches():
    global double_switch, dev_name
    double_switch = localswitches.DoubleSwitch(21, 20, 26, 16, name=dev_name, ext_log=file_logger, sw0_name=' /UP',
                                               sw1_name=' /DOWN', mode='press')
    """Timeout is a must"""
    time.sleep(2)


def load_watchdogs():
    double_switch.watch_dog()


def tests():
    time.sleep(1)
    double_switch.switch0.switch_state = 1
    time.sleep(2)
    double_switch.switch1.switch_state = 1
    time.sleep(2)
    double_switch.switch0.switch_state = 1
    time.sleep(0.5)
    double_switch.switch0.switch_state = 0


## Program starts HERE:
dev_name = 'Window'
log = 'DoubleSwitches.log'

try:
    load_services(log, dev_name)
    load_HW_switches()
    load_watchdogs()
    # load_lcd()
    tests()

    body_message = utils_localswitch.XTractLastLogEvent(home + '/Documents/' + log).xport_chopped_log()
except:
    body_message = 'Fail to load correctly'

finally:
    pass
    # GmailDaemon.compose_mail(recipients=['guydvir2@gmail.com'], subject='HomePi-Boot ' + dev_name, body=body_message)
