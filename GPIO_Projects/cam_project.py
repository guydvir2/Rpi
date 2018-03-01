import picamera
import RPi.GPIO as GPIO
import gpiozero
import time
import datetime
from PIL import Image

class Buzz():
    def __init__(self, gpio):
        self.buzzer = gpiozero.Buzzer(gpio)
        
    def buzz(self):
        self.buzzer.on()
        time.sleep(0.5)
        self.buzzer.off()
        
    def bizbuz(self):
        for i in range (5):
            self.buzzer.on()
            time.sleep(0.015)
            self.buzzer.off()
            time.sleep(0.1)

class Button():
    def __init__(self, gpio):
        self.button = gpiozero.Button(gpio)

#class LCDdisplay():
        
class Camera():
    def __init__(self, res='(1024, 768)',dir1='/home/guy/'):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1024,768)
        self.camera.rotation = 180
        #self.camera.ISO = 200
        #self.camera.brightness = 70
        self.path = dir1
        
    def capture(self):
        tstamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        fname = self.path+tstamp+'.jpg'
        self.camera.capture(fname)
        Image.open(fname).show()

    def preview(self,time1=5):
        self.camera.start_preview()
        time.sleep(time1)
        self.camera.stop_preview()
    
    
    
b=Buzz(20)
#b.bizbuz()
cam=Camera()
cam.capture()

#img = Image.open('/home/guy/20180223_215741.jpg')
#img.show()
#cam.preview()

    

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#out_pins=[11,12]
#in_pins=[21,22]

#GPIO.setup(out_pins, GPIO.OUT)
#GPIO.setup(in_pins, GPIO.IN)

#GPIO.output(out_pins[1],True)
#print(GPIO.getmode)

##print(dir(GPIO))
#GPIO.cleanup
