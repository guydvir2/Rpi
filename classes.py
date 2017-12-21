from gpiozero import *

#class dev(object):
    #def __init__(self,name,hdware,gpio):
        #self.name=name
        #self.hdware=hdware(gpio)

    #def activ(self):
        #globals()["self.hdware"]()


#dev1=dev("led",gpiozero.LED,17)
#dev1.activ




dev=["dev0","dev1","dev2"]
gpio_pin=[17,4]

with LED(17) as dev(0):
    dev.on()
    #dev(0).is_lit()
    #dev(0).off()
    #dev(0).is_lit()
    
