import picamera
from picamera import Color
import RPi.GPIO as GPIO
import gpiozero
import time
import datetime
import  Adafruit_DHT
from PIL import Image
from sys import platform
from sys import path

os_type = platform
if os_type == 'darwin':
    main_path = '/Users/guy/Documents/github/Rpi/'
elif os_type == 'win32':
    main_path = 'd:/users/guydvir/Documents/git/Rpi/'
elif os_type == 'linux':
    main_path = '/home/guy/Documents/github/Rpi/'


path.append(main_path + 'GPIO_Projects/lcd')
path.append(main_path + 'SmartHome')
path.append(main_path + 'modules')

import gmail_mod


class TempHumid():
    def __init__(self, gpio):
        self.run_it(gpio)
        
    def run_it(self,gpio):
        while True:
            h0,t0 = Adafruit_DHT.read(11,gpio)
            if h0 and t0:
                if h0 < 100 and t0 < 100 :
                    tstamp=str(datetime.datetime.now())[:-7]
                    h=h0
                    t=t0                
                    self.val=[t0,h0]
                    print(tstamp, "Temp: %d[C], Humid=%d%%"%(t0,h0))#self.val)
                    time.sleep(2)

        
class SoundDetect():
    def __init__(self, pin=13):
        GPIO.setmode(GPIO.BCM)
        SOUND_PIN = pin
        GPIO.setup(SOUND_PIN, GPIO.IN)
        GPIO.add_event_detect(SOUND_PIN, GPIO.RISING)#, callback=self.test)
        print(">> Sound Module started GPIO")
        self.detection()

    def detection(self):
        counter = 0
        pin = 13
        while True:
            if GPIO.event_detected(pin):
                counter +=1
                print("Got you-", counter)
                time.sleep(1)
                #self.output()


class Buzz():

    def __init__(self, gpio):
        self.buzzer = gpiozero.Buzzer(gpio)
        print(">> Buzzer Module started GPIO", gpio)
        
    def buzz(self):
        self.buzzer.on()
        time.sleep(0.5)
        self.buzzer.off()
        
    def light_buzz(self):
        self.buzzer.on()
        time.sleep(0.05)
        self.buzzer.off()
        
    def bizbuz(self):
        for i in range (5):
            self.buzzer.on()
            time.sleep(0.15)
            self.buzzer.off()
            time.sleep(0.1)

class Button():
    def __init__(self, gpio):
        self.button = gpiozero.Button(gpio)
        print(">> Button Module started GPIO",gpio)

#class LCDdisplay():
        
class Camera():

    def __init__(self, res='(1024, 768)',pic_dir='/home/guy/'):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1024,768)
        self.camera.rotation = 180
        #self.camera.ISO = 200
        #self.camera.brightness = 70
        self.path = pic_dir
        print(">> Camera Module started")
        
    def capture(self):
        tstamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.fname = self.path+tstamp+'.jpg'
        self.camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.camera.annotate_text_size = 36
        self.camera.annotate_foreground = Color('black')
        self.camera.annotate_background = Color('white')
        self.camera.capture(self.fname)

    def cap_show(self):
        self.capture()
        Image.open(self.fname).show()

    def send_cap(self):
        GmailDaemon.compose_mail(recipients=['dr.guydvir@gmail.com'], attach=[self.fname], body="Python automated email",subject='Pic4U')


    def preview(self,time1=5):
        self.camera.start_preview()
        time.sleep(time1)
        self.camera.stop_preview()
    

GmailDaemon = gmail_mod.GmailSender(pfile='/home/guy/Documents/github/Rpi/BuildingBlocks/p.txt', ufile='/home/guy/Documents/github/Rpi/BuildingBlocks/user.txt')

#temp_humid=TempHumid(12)
#pir = gpiozero.MotionSensor(19)
pic_button=Button(21)
vid_button=Button(20)
cam=Camera()
buzzer=Buzz(26)
sound_sensor = SoundDetect()
motion_counter=0

#cam.capture()
#cam.cap_show()


while True:
    if pic_button.button.is_pressed:
        #button.button.wait_for_press()
        buzzer.buzz()
        cam.capture()
        cam.cap_show()
    #if pir.motion_detected:
        #motion_counter +=1
        #buzzer.light_buzz()
        #print('motion_detected: #',motion_counter)
        #time.sleep(1)
    if vid_button.button.is_pressed:
        cam.preview()
