import RPi.GPIO as GPIO
import time
import datetime
import os


GPIO.setmode(GPIO.BCM)
SOUND_PIN = 6
GPIO.setup(SOUND_PIN, GPIO.IN)

count = 0

def DETECTED(SOUND_PIN):
   global count
   nowtime = datetime.datetime.now()
   count += 1

   print ("Sound Detected! " + str(nowtime) + " " + str(count))
   #os.system("/home/pi/scripts/playfile.py")

   return nowtime
print ("Sound Module Test (CTRL+C to exit)")
time.sleep(2)
print ("Ready")

try:
   GPIO.add_event_detect(SOUND_PIN, GPIO.RISING, callback=DETECTED)
   while 1:
      time.sleep(100)
except KeyboardInterrupt:
   print (" Quit")
   GPIO.cleanup()
