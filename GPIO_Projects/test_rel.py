import gpiozero
from time import sleep

def local_gpio_test(pins=[20,21]):
	
	#pin=6
	#pins=[21,6,22,4]
	rel_t=0.5
	i=0

	while True:
		
		relay=gpiozero.OutputDevice(pins[i])
		relay.on()
		sleep(rel_t)
		relay.off()
		sleep(rel_t)
		if i<3:
			i +=1
		else:
			i=0
