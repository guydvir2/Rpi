import lcddriver
import time
import subprocess
from gpiozero import LED

def convert_time(x):
    hours=int(x/3600)
    minutes=int((x/3600-hours)*60)
    seconds=x-hours*3600-minutes*60
    time_str=str("%02d:%02d:%02d" %(hours, minutes, seconds))
    return time_str

def center_str(text_in):
    text_out=" "*round((16-len(text_in))/2)+text_in
    return text_out

display = lcddriver.lcd()
led = LED(17)
#vcc=LED(4)

#vcc.on()

display.lcd_clear()
speed_time=5
display.lcd_display_string(center_str("Let's Start !!"), 1)
time.sleep (2)
display.lcd_clear()
text1="time left:"

counter=20


for x in range (counter+1):
    led.on()
    time.sleep (0.5/speed_time)
    display.lcd_display_string(text1,1) # Write line of text to first line of display
    display.lcd_display_string(center_str(convert_time(counter-x)), 2) # Write line of text to second line of display
    led.off()
    time.sleep(0.5/speed_time)
    

if x==counter :
    display.lcd_clear()
    display.lcd_display_string("time's up ", 1)
    display.lcd_display_string(center_str("B O O M"), 2)
    time.sleep(5)
    display.lcd_clear()
    #vcc.off()
