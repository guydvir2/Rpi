import LocalSwitch
import time
import gpiozero
import use_lcd
from signal import pause

def show_status_lcd(switch,row):
    try:
        lcd_display=use_lcd.MyLCD()
        if row in [1,2]:
            while True:
                if switch.switch_state[0] is False:
                    s_state = 'off'
                elif s.switch_state[0] is True:
                    s_state = 'on'

                text='%s :%s'%(s.name, s_state)
                if row==1:
                    lcd_display.center_str(text1=text)
                elif row==2:
                    lcd_display.center_str(text2=text)

                sleep(2)
        else:
            print("row value must be 1 or 2")

    except OSError:
        print("LCD not installed correctly")
        
        
a=LocalSwitch.LocSwitch(5,21, name='Relay#1', mode='toggle')
b=LocalSwitch.LocSwitch(20,13, name='Relay#2', mode='toggle')
time.sleep(1)
show_status_lcd(a,1)
a.switch_state = 1
time.sleep(2)
a.switch_state = 0

#while True:
    #if a.switch_state[0] is False:
        #a_state = 'off'
    #elif a.switch_state[0] is True:
        #a_state = 'on'
##    if b.switch_state[0] is False:
##        b_state = 'off'
##    elif b.switch_state[0] is True:
##        b_state = 'on'
    #text1='%s :%s'%(a.name, a_state)
    #print(text1)
##    text2='%s :%s'%(b.name, b_state)
 ##   lcd_display.center_str(text1=text1, text2=text2)


    #time.sleep(1)
