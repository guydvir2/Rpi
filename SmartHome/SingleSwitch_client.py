import my_paths
import envelope_localswitch
import localswitches
import time

file_logger = envelope_localswitch.Log2File('SingleSwitch.log', screen=0)
sw1 = localswitches.SingleSwitch(26, 21, name='Relay#1', mode='toggle', ext_log=file_logger)

# Disp on LCD
envelope_localswitch.ShowStatusLCD([sw1])# ,ext_log=file_logger)
time.sleep(1)

# Make switch by code
sw1.switch_state = 1
time.sleep(1)
sw1.switch_state = 0
time.sleep(1)
