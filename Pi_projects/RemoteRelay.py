#import pigpio

#class rpi_relay(pigpio.pi):

    #def __init__(self,ip_addr,gpio=[4,22,6,26]):
        #pigpio.pi.__init__(self)
        #self.GPIO=gpio
        #self.rpi=pigpio.pi(ip_addr)
        #for t in range(len(self.GPIO)):
            #self.rpi.write(self.GPIO[t],0)

    #def switch_state(self,i,state):
        #self.rpi.write(self.GPIO[i],state)

    #def read_state(self,i):
        #self.rpi.write(self.GPIO[i],state)
       
#def switch_state(i,state):
	#rpi.write(GPIO[i],state)

#def read_state(i):
	#rpi.write(GPIO[i],state)  

      
#GPIO='192.168.2.112', '192.168.2.113'
#rpi=pigpio.pi(GPIO[0])
#read_state(0)
#print("OK")

#from gpiozero import *
from gpiozero import LEDBoard, MotionSensor, Button, Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause

ips = ['192.168.2.112', '192.168.2.113']
remotes = [PiGPIOFactory(host=ip) for ip in ips]
#remotes = PiGPIOFactory(ips[0])
button = Button(22) # button on this pi
buzzers = [Buzzer(22, pin_factory=r) for r in remotes] # buzzers on remote pins
for buzzer in buzzers:
	print (buzzer)
	buzzer.on()
buzzer.source = button.values
pause()

