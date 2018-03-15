import datetime
import sys
from time import sleep

sys.path.append('/home/guy/Documents/github/Rpi/GPIO_Projects/lcd')
import use_lcd
lcd=use_lcd.MyLCD()
now = str(datetime.datetime.now())
print(now)

try:
    while True:
        now = str(datetime.datetime.now())[:-5].split(' ')
        lcd.center_str(text1=now[0], text2=now[1])
except KeyboardInterrupt:
    print('End by user,',now[0],now[1])
    lcd.clear_lcd()
    lcd.center_str(text1='Stopped')
    sleep(3)
    lcd.clear_lcd()
