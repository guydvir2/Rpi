from gpiozero import MotionSensor
#from gpiozero import Buzzer
from gpiozero import LED
from time import sleep
import  Adafruit_DHT
import lcddriver
import picamera





def center_str(text_in):
    text_out=" "*round((16-len(text_in))/2)+text_in
    return text_out

display = lcddriver.lcd()
pir = MotionSensor(4)
led_red = LED (17)
camera = picamera.PiCamera()

#buz = Buzzer (17)
#buz

display.lcd_clear()
display.lcd_display_string(center_str("Hello"), 1)
sleep (2)
display.lcd_clear()



x=0
while True:
    while pir.wait_for_motion():
        x +=1
        print("Alarm #",x)
        display.lcd_clear()
        display.lcd_display_string(center_str("Shachar"), 1)
        display.lcd_display_string("Alarm #"+str(x), 2)
        camera.capture('/home/guy/image%d.jpg'%x)
        #buz.on()
        #led_red.on()
        #buz.off()
        #sleep(2)
        #sleep(5)
        #led_red.off()
        sleep(3)
    
    pir.wait_for_no_motion()
