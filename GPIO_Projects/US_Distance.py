from gpiozero import DistanceSensor
from time import sleep

ultrasonic = DistanceSensor(echo=21, trigger=20)

while True:
    print("Y")  
    print('Distance: ', ultrasonic.distance * 100)
    sleep(1)
    
    #print("T")
    #ultrasonic.wait_for_in_range()
    #print("In range")
    #ultrasonic.wait_for_out_of_range()
    #print("Out of range")
    #sleep(1)
    #print(ultrasonic.distance)
