import RPi.GPIO as GPIO
import time
 
#GPIO SETUP
channel = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
 
def callback(channel):
        if GPIO.input(channel):
                print ("Movement Detected1!")
        else:
                print ("Movement Detected2!")
 
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

while True:
        time.sleep(1)
