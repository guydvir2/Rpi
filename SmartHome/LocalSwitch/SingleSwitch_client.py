import my_paths
import utils_localswitch
import localswitches
import time
import sys
from gmail_mod import GmailSender

# Define Switch :(Output GPIO, Input GPIO, name=text, mode='toggle'/'press', ext_log=None)
# Create a file logger to log outputs of switches

def load_services(log_file, dev_name):
    global file_logger, GmailDaemon
    path_define()
    file_logger = utils_localswitch.Log2File(path+'/SmartHome/'+log_file, screen=0, name_of_master=dev_name)
    GmailDaemon = GmailSender(sender_file=path+'/modules/ufile.txt', password_file=path+'/modules/pfile.txt')

def load_lcd():
    global lcd
    lcd = utils_localswitch.Output2LCD([sw1])#,ext_log=file_logger)
    if lcd.boot_success is True:
        file_logger.append_log(log_entry='[LCD Display] detected and loaded OK')
    else:
        file_logger.append_log(log_entry='[LCD Display] not present/ driver error', time_stamp=1)

def load_HW_switches():
    global sw1, dev_name
    sw1 = localswitches.SingleSwitch(19, 21, name=dev_name, mode='toggle', ext_log=file_logger)
    ##Timeout is a must
    time.sleep(2)

def load_watchdogs():
    sw1.watch_dog()

def tests():
    sw1.switch_state = 1
    time.sleep(1)
    sw1.switch_state = 0
    time.sleep(1)

def path_define():
    global path
    os_type = sys.platform
    if os_type == 'darwin':
        path = '/Users/guy/Documents/github/Rpi'
    elif os_type == 'win32':
        path = 'd:/users/guydvir/Documents/git/Rpi'
    elif os_type == 'linux':
        path = '/home/guy/Documents/github/Rpi'

## Program starts HERE:
dev_name='RoomLight'
log='SingleSwitche.log'

try:
    load_services(log,dev_name)
    load_HW_switches()
    load_watchdogs()
    load_lcd()
    body_message = utils_localswitch.XTractLastLogEvent(path+'/SmartHome/'+log).xport_chopped_log()

except:
    body_message='Fail to load correctly'

finally:
    GmailDaemon.compose_mail(recipients=['guydvir2@gmail.com'], subject='HomePi-Boot notification '+dev_name,body=body_message)
    
time.sleep(1)

tests()