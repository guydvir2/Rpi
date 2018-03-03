import LocalSwitch
import time
import gpiozero
#import use_lcd
from signal import pause

a=LocalSwitch.LocSwitch(5,21, name='Relay#1', mode='toggle')
b=LocalSwitch.LocSwitch(4,13, name='Relay#2', mode='toggle')
#lcd_display=use_lcd.MyLCD()
time.sleep(1)
a.switch_state = 1
time.sleep(2)
a.switch_state = 0

while True:
    if a.switch_state[0] is False:
        a_state = 'off'
    elif a.switch_state[0] is True:
        a_state = 'on'
#    if b.switch_state[0] is False:
#        b_state = 'off'
#    elif b.switch_state[0] is True:
#        b_state = 'on'
    text1='%s :%s'%(a.name, a_state)
#    print(text1)
#    text2='%s :%s'%(b.name, b_state)
 #   lcd_display.center_str(text1=text1, text2=text2)


    time.sleep(1)
