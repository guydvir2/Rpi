from gpiozero import MotionSensor
from gpiozero import Buzzer
from gpiozero import LED
from time import sleep

pir = MotionSensor(4)
buz = Buzzer (17)
led_red = LED (13)
buz

while True:
    while pir.wait_for_motion():
        print("Hello Shachar ! :) ")
        buz.on()
        led_red.on()
        sleep(0.05)
        buz.off()
        sleep(2)
        led_red.off()
        
        sleep(5)
    
    pir.wait_for_no_motion()
