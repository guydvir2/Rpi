
from gpiozero import LED, Button
from signal import pause
from gpiozero import OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import InputDevice

from time import sleep
import gpiozero

class A:
    def __init__(self):
        factory112 = PiGPIOFactory(host='192.168.2.113')
        factory113 = PiGPIOFactory(host='192.168.2.113')

        self.Relay= OutputDevice(13, pin_factory=factory113,initial_value=False)
        #self.button= InputDevice(21, pin_factory=factory)

        self.led = LED(17)
        self.button = Button(21, pin_factory=factory112)
        self.led.source = self.button.values
        self.button.when_released = self.switchoff
        self.button.when_pressed = self.switchon
        #print(self.button.when_pressed)

        
    def switchon(self):
        print('on')
        self.Relay.on()

    def switchoff(self):
        print('off')
        self.Relay.off()
        
        
Rel = A()
pause()
