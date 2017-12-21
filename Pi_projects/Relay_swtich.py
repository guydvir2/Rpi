import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

### PINOUT
# +VCC to 5v
# - to GND
# S to GPIO#

#
chan_list = [4]
GPIO.setup(chan_list, GPIO.OUT)
delay=10**(0)

for t in chan_list:
    for st in range(1,-1,-1):
        GPIO.output(t,st ) # turns on
        print ("GPIO %d switched %d"%(t,GPIO.input(t)))
        sleep(delay)

#GPIO.cleanup()



