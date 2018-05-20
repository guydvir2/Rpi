from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(21)
sl=0.01
while True:
    buzzer.on()
    sleep(sl)
    buzzer.off()
    sleep(sl)

#while True:
    #buzzer.beep()

buzzer.off()
