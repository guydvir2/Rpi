from gpiozero import DistanceSensor
from time import sleep

ultrasonic = DistanceSensor(echo=19, trigger=6)

while True:
    print("Y")  
    ultrasonic.wait_for_in_range()
    print("In range")
    ultrasonic.wait_for_out_of_range()
    print("Out of range")
    
    #print("T")
    #ultrasonic.wait_for_in_range()
    #print("In range")
    #ultrasonic.wait_for_out_of_range()
    #print("Out of range")
    #sleep(1)
    #print(ultrasonic.distance)
