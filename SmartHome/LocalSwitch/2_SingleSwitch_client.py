import my_paths
import utils_localswitch
import localswitches
import time
import sys
from gmail_mod import GmailSender
import wifi_shut


# Define Switch :(Output GPIO, Input GPIO, name=text, mode='toggle'/'press', ext_log=None)
# Create a file logger to log outputs of switches

def load_services(log_file, dev_name):
    global file_logger, GmailDaemon
    path_define()
    file_logger = utils_localswitch.Log2File(home + '/Documents/' + log_file, screen=0, name_of_master=dev_name)
    GmailDaemon = GmailSender(sender_file=path + '/modules/ufile.txt', password_file=path + '/modules/pfile.txt')


def load_lcd():
    global lcd
    lcd = utils_localswitch.Output2LCD([sw1, sw2])  # ,ext_log=file_logger)
    if lcd.boot_success is True:
        file_logger.append_log(log_entry='[LCD Display] detected and loaded OK')
    else:
        file_logger.append_log(log_entry='[LCD Display] not present/ driver error', time_stamp=1)


def load_HW_switches():
    global sw1, sw2, dev_name
    sw1 = localswitches.SingleSwitch(19, 21, name=dev_name + '#1', mode='toggle', ext_log=file_logger)
    sw2 = localswitches.SingleSwitch(26, 20, name=dev_name + '#2', mode='toggle', ext_log=file_logger)
    # Timeout is a must
    time.sleep(2)

def load_local_timetable():




def load_watchdogs():
    sw1.watch_dog()
    sw2.watch_dog()


def tests():
    sw1.switch_state = 1
    time.sleep(5)
    sw2.switch_state = 1

    sw1.switch_state = 0
    time.sleep(5)
    sw2.switch_state = 0


def path_define():
    global path, home
    os_type = sys.platform
    if os_type == 'darwin':
        home = '/Users/guy'
    elif os_type == 'win32':
        home = 'd:/users/guydvir'
    elif os_type == 'linux':
        home = '/home/guy'
    path = home + '/Documents/github/Rpi'


## Program starts HERE:
dev_name = 'PergulaLights'
log = '2SingleSwitches.log'

try:
    load_services(log, dev_name)
    load_HW_switches()
    load_watchdogs()
    load_lcd()
    body_message = utils_localswitch.XTractLastLogEvent(home + '/Documents/' + log).xport_chopped_log()

except:
    body_message = 'Fail to load correctly'

finally:
    GmailDaemon.compose_mail(recipients=['guydvir2@gmail.com'], subject='HomePi-Boot notification ' + dev_name,
                             body=body_message)

time.sleep(1)

tests()
