
from gpiozero.pins.pigpiod import PiGPIOPin
from gpiozero import LED
from signal import pause
import time

#led_pi2 = LED(PiGPIOPin(17, host='192.168.2.112'))
#led_pi2.on()


led_pi1 = LED(PiGPIOPin(22, host='192.168.2.113'))
led_pi1.on()

time.sleep(5)

#led_pi1.off()
led_pi2.off()
