from gpiozero import MotionSensor
import picamera
import datetime

#from gpiozero import Buzzer
#from gpiozero import LED
from time import sleep
import use_lcd
#import wand
#import Image
import subprocess
import os

pir = MotionSensor(21)
#buz = Buzzer (17)
#led_red = LED (13)
lcd1=use_lcd.MyLCD()
camera=picamera.PiCamera()
camera.ISO = 500
#camera.shutter=500
camera.rotation=180
camera.resolution = (640, 480)

#with Image(blob=file_data) as image:
    #wand.display.display(IMAGE)

lcd1.center_str(text_in1='Alarm system', text_in2='Start')
x=0

while True:
        while pir.wait_for_motion():
                alarm_text = 'Detect #%d'%x
                lcd1.left_str(text_in1=alarm_text, to=2)
                print("detect",x)
                filename='/home/guy/image%d.jpg'%x

                camera.capture(filename)
                #image = Image.open(filename)
                #image.show()
                subprocess.run(filename)
                #os.startfile(filename)
                x +=1
        #buz.on()
        #led_red.on()
        #sleep(0.05)
        #buz.off()
        #sleep(2)
        #led_red.off()
        
                sleep(1)
    
        pir.wait_for_no_motion()
