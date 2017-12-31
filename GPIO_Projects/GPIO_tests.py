from gpiozero.pins.pigpiod import PiGPIOPin
from gpiozero import LED
from signal import pause
from time import sleep



led = LED(PiGPIOPin(21, host='192.168.2.112'))
led.off()
#print(led.pin.number)
import pigpio
#pins=[20,21]
#pi2='192.168.2.112'
#pi112=pigpio.pi(pi2)
#for t in pins:
    #print(t, pi112.read(t))
    #pi112.write(t,1)
    #print("on")
    #sleep(10)
    #pi112.write(t,0)
    #print("off")

class relay(pigpio.pi):
    
    def __init__(self,ip_addr):
        pigpio.pi.__init__(self)
        self.GPIO=[4,5,6,12]
        self.rpi=pigpio.pi(ip_addr)
        for t in range(len(self.GPIO)):
            self.rpi.write(self.GPIO[t],0)

    def switch_state(self,i,state):
        self.rpi.write(self.GPIO[i],state)
        
pi_1=relay('192.168.2.112')
pi_2=relay('192.168.2.113')

x=0
pi_1.switch_state(x,0)
