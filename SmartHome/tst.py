import LocalSwitch
import time
import gpiozero
from signal import pause
a=LocalSwitch.LocSwitch(5,21, name='Test')
#b=LocalSwitch.LocSwitch(20,4)
#time.sleep(3)

#b.get_status
#for x in range(10):
 #   print(x)

#a = gpiozero.Button(11)
#b = gpiozero.Buzzer(4)
#b.source = a.values

pause()
