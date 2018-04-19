import my_paths
import utils_localswitch
import localswitches
import time
from gmail_mod import GmailSender

# Define Switch :(Output GPIO, Input GPIO, name=text, mode='toggle'/'press', ext_log=None)
# Create a file logger to log outputs of switches
try:
    file_logger = utils_localswitch.Log2File('2SingleSwitches.log', screen=0)
    sw1 = localswitches.SingleSwitch(19, 21, name='Relay#1', mode='toggle', ext_log=file_logger)
    sw2 = localswitches.SingleSwitch(26, 20, name='Relay#2', mode='toggle', ext_log=file_logger)
    path='/home/guy/Documents/github/Rpi/modules/'
    GmailDaemon = GmailSender(sender_file=path+'ufile.txt', password_file=path+'pfile.txt')

    # Disp on LCD
    utils_localswitch.Output2LCD([sw1, sw2],ext_log=file_logger)
    GmailDaemon.compose_mail(recipients=['guydvir2@gmail.com'], subject='Load Summary Rpi-Switch',body='System loaded OK')

except:
    GmailDaemon.compose_mail(recipients=['guydvir2@gmail.com'], subject='Load Summary Rpi-Switch',body='Fail to load correctly')
time.sleep(1)

# Make switch by code
sw1.switch_state = 1
time.sleep(5)
sw2.switch_state = 1

sw1.switch_state = 0
time.sleep(5)
sw2.switch_state = 0
