from gpiozero import Button
from signal import pause
from gpiozero.pins.pigpio import PiGPIOFactory
import os
from socket import gethostname
from sys import platform
from sys import path
import datetime
from time import sleep



class GPIOMonitor:
    def __init__(self, pin, pin_factory=None, alias='gpio_monitor'):
        
        if pin_factory is None:
                local_factory = PiGPIOFactory(host='localhost')
        else:
                local_factory = PiGPIOFactory(host=pin_factory)
                        
        self.button= Button(21,pin_factory=local_factory)
        self.button.when_released = lambda : self.notify('alarm set off')
        self.button.when_pressed = lambda : self.notify('alarm set on')
        self.alias = alias

        self.logger = Log2File('/home/guy/Documents/AlarmMonitor.log',
                               name_of_master=self.alias,time_in_log=1,screen=1)
        self.run_gmail_service()
        self.check_state_on_boot(pin, pin_factory)
        #self.notify("%s start, monitoring GPIO [%d] of IP [%s]"%
        #(self.alias,pin, pin_factory))
        
        
    def run_gmail_service(self):
        globals = main_path
        path=main_path+'modules/'
        self.gmail = gmail_mod.GmailSender(sender_file=path + 'ufile.txt',
                                           password_file=path + 'pfile.txt')
                                           
    def email_notify(self,msg,sbj=None):
        self.gmail.compose_mail(recipients=['guydvir.tech@gmail.com'],
                                body=msg, subject=sbj)
          
    def notify(self, msg):
        self.logger.append_log(msg)
        self.email_notify(msg=self.logger.msg, sbj='HomePi: %s'%(self.alias))
        
    def check_state_on_boot(self,pin, pin_factory):
        boot_msg="%s start, monitoring GPIO [%d] of IP [%s]"%(self.alias,pin, pin_factory)
        
        if self.button.is_pressed == True:
            self.notify(boot_msg+ ' alarm is on')
        else:
            self.notify(boot_msg+' alarm is off')
            

        
        

os_type = platform
if os_type == 'darwin':
    main_path = '/Users/guy/Documents/github/Rpi/'
elif os_type == 'win32':
    main_path = 'd:/users/guydvir/Documents/git/Rpi/'
elif os_type == 'linux':
    main_path = '/home/guy/Documents/github/Rpi/'


path.append(main_path + 'GPIO_Projects/lcd')
path.append(main_path + 'SmartHome/LocalSwitch')
path.append(main_path + 'modules')
import gmail_mod
from localswitches import Log2File
from localswitches import XTractLastLogEvent
 
GPIOMonitor(21,'192.168.2.113','Alarm Monitor')
pause()
