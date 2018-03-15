import LocalSwitch
import time
import gpiozero
import threading
from signal import pause
import use_lcd
import datetime


class ShowStatusLCD:
    def __init__(self,switches):
        self.switches = switches
        try:
            # Case of HW err
            self.lcd_display=use_lcd.MyLCD()
            self.t = threading.Thread(name='thread_disp_lcd', target=self.display_status_loop)
            self.t.start()
        except OSError:
            print("LCD hardware error")

    def display_status_loop(self):
        status=[[] for i in range(len(self.switches))]
        while True:
            t_stamp=datetime.datetime.now()
            t1, t2 = 0, 0
            
            while t1<10:
                for i,current_switch in enumerate(self.switches):
                    if current_switch.switch_state[0] is False:
                        status[i] = '%s :%s'%(current_switch.name, 'off')
                    elif current_switch.switch_state[0] is True:
                        status[i] = '%s :%s'%(current_switch.name, 'on ')

                    self.lcd_display.center_str(text1=str(status[0]), text2=str(status[1]))
                    time.sleep(1)
                    t1=(datetime.datetime.now()-t_stamp).total_seconds()
         
            self.lcd_display.clear_lcd()
            while t2<15:
                self.show_time()
                t2=(datetime.datetime.now()-t_stamp).total_seconds()

    def show_time(self):
        timeNow = str(datetime.datetime.now())[:-5].split(' ')
        self.lcd_display.center_str(text1=timeNow[0], text2=timeNow[1])
        

# Define Switch :(Output GPIO, Input GPIO, name=text, mode='toggle'/'press')
sw1=LocalSwitch.LocSwitch(5,21, name='Relay#1', mode='toggle')
sw2=LocalSwitch.LocSwitch(20,13, name='Relay#2', mode='toggle')

# Disp on LCD
ShowStatusLCD([sw1,sw2])
time.sleep(1)

# Make switch by code
sw1.switch_state = 1
time.sleep(5)
sw2.switch_state = 1

sw1.switch_state = 0
time.sleep(5)
sw2.switch_state = 0
