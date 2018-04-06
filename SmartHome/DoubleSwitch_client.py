import my_paths
import utils_localswitch
import localswitches
import time

# Define DoubleSwitch :(Input GPIO X2,Output GPIO X2,  name=text, ext_log=None)
# Create a file logger to log outputs of switches

file_logger = utils_localswitch.Log2File('double_switch.log', screen=0)
double_switch = localswitches.DoubleSwitch(26, 19, 21, 20, name='DS')

# Disp on LCD
utils_localswitch.Output2LCD([double_switch.switch0, double_switch.switch1])#, ext_log=file_logger)
time.sleep(1)

# Make switch by code
time.sleep(2)
double_switch.switch0.switch_state = 1
time.sleep(2)
double_switch.switch1.switch_state = 1
time.sleep(0.7)
double_switch.switch0.switch_state = 1

