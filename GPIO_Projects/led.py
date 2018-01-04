from gpiozero import LED
from time import sleep

tim_del=0.2
r=50

led = LED(17)
for x in range (r):
    led.on()
    sleep(tim_del)
    led.off()
    sleep(tim_del)

print ("OK, that was ", r, "blinks")


