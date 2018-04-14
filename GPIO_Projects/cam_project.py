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
import use_lcd


class TempHumid():
    def __init__(self, gpio):
        self.gpio = gpio

    def measure(self):
        res=[]
        h0,t0 = Adafruit_DHT.read(11,self.gpio)
        if h0 and t0:
            if h0 < 100 and t0 < 100 :
                res=[t0, h0]
        return res


class SoundDetect():
    def __init__(self, pin=13):
        GPIO.setmode(GPIO.BCM)
        SOUND_PIN = pin
        GPIO.setup(SOUND_PIN, GPIO.IN)
        GPIO.add_event_detect(SOUND_PIN, GPIO.RISING)#, callback=self.test)
        print(">> Sound Module started GPIO")
        #self.detection(pin)
        self.pin=pin

    def detection(self):
        return GPIO.event_detected(self.pin)
        #counter = 0
        #while True:
            #if GPIO.event_detected(pin):
                ##counter +=1
                #print("Sound Heard", counter)
                #time.sleep(1)
                #return 1


class VibSensor():
    def __init__(self, gpio):
        channel = gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.IN)
        GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
        print(">> Vib Module Module started GPIO", gpio)

    def detection(self,pin=13):
        return GPIO.input(pin)


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

    
def show_lcd(text1='',text2='', to=2):
    try:
        lcd.center_str(text1,text2, to=to)
        print(text1+'\n'+text2)

    except NameError:
        print(text1+'\n'+text2)

GmailDaemon = gmail_mod.GmailSender(pfile='/home/guy/Documents/github/Rpi/BuildingBlocks/p.txt', ufile='/home/guy/Documents/github/Rpi/BuildingBlocks/user.txt')

pic_button=Button(21)
vid_button=Button(20)
buzzer=Buzz(26)
motion_counter=0
vib_count=0
sound_count=0

vib_sense=VibSensor(13)
temp_humid=TempHumid(19)
pir = gpiozero.MotionSensor(12)
cam=Camera()
sound_sensor = SoundDetect(6)


try:
    lcd=use_lcd.MyLCD()
    show_lcd("Hello","World")
except OSError:
    print('Fail to run LCD')

while True:
    tstamp = str(datetime.datetime.now())[:-7]

    #if pic_button.button.is_pressed:
        #buzzer.buzz()
        #cam.capture()
        #show_lcd(text1='Picture', text2=tstamp, to=2)
        #cam.cap_show()
        ##cam.send_cap()
    if pir.motion_detected:
        motion_counter +=1
        buzzer.light_buzz()
        cam.capture()
        cam.cap_show()

        show_lcd(text1='motion_det: #'+str(motion_counter))
        time.sleep(2)
    #if vid_button.button.is_pressed:
        #show_lcd(text1='show video', text2=tstamp, to=2)
        #cam.preview()
        #show_lcd(text1='stop video', text2=tstamp, to=2)
    #if vib_sense.detection() == 1:
        #vib_count +=1
        #buzzer.buzz()
        ##show_lcd(text1='vibration: '+str(vib_count), text2=tstamp, to=1)
    #if sound_sensor.detection()==1:
        #sound_count +=1
        #show_lcd(text1='Sound: '+str(sound_count), text2=tstamp, to=1)
    #th= temp_humid.measure()
    #if th != []:
        #show_lcd(text1='Temp: %d Hum: %d'%(th[0],th[1]), text2=tstamp, to=5)
