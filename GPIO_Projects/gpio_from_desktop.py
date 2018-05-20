from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause

#factory = PiGPIOFactory(host='192.168.2.113')

button = Button(2)
led = LED(17)#,pin_factory=factory)

led.source = button.values

pause()
