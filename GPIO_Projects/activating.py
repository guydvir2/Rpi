import time
import gpiozero
from signal import pause
import datetime
import picamera


####### GPIO Def ###########
buzz=gpiozero.Buzzer(4)
button1=gpiozero.Button(26)
led1=gpiozero.LED(17)
cam=picamera.PiCamera()
############################

led1.off()
hold_time=2
cam.resolution = (1024, 768)

def now(p):
    t = datetime.datetime.now()
    a = t.strftime('%d-%m-%Y, %H:%M:%S')
    if p == 0:
        return t
    elif p == 1:
        return a
        
    
def take_picture(i,file):
    time.sleep(i)
    cam.capture(file)
    print('Click!')

    
def small_alarm():
    buzz.blink(0.01, 0.08, 2)
    led1.blink(0.5,0.5,3)

def big_alarm():
    buzz.blink(0.1, 0.08, 2)
    led1.blink(2,1,3)

def push_button():
    start_time=time.time()
    diff=0
    
    while button1.is_active and (diff <hold_time) :
        now_time=time.time()
        diff=-start_time+now_time
       
    if diff < hold_time :
        print("pushed")
        small_alarm()
        
    else:
        long_push()


def long_push():
    print("big push")
    big_alarm()
    take_picture(1,'/home/guy/snap.jpg')
    

button1.hold_time=hold_time
button1.when_held= long_push
button1.when_pressed = push_button
tol_seconds=5

print(now(1))
j=0;
while True:
    if datetime.datetime.now() -datetime.datetime(2017,6,30,19,00,00) < datetime.timedelta(0, 5)
        print ("not yet...",j)
        j +=1
        

pause()

