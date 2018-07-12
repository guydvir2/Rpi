from gpiozero import Button, OutputDevice

from sys import platform, path
import os
import datetime



class GPIOMonitor:
    def __init__(self, ip=None, alias='gpio_monitor',
                 listen_pins=[21, 20], trigger_pins=[16, 26], 
                 log_filename='/home/guy/Documents/AlarmMonitor.log'):
                # listen_pins = [sys.arm, alarm.on], trigger_pins=[full, home]
        self.last_state=[None for i in range(4)]
        self.cbit=cbit.CBit(1000)
        
        if ip is not None:
            self.factory = PiGPIOFactory(host=ip)
        else:
            self.factory=None
            self.ip_pi = getip.get_ip()[0]
            
        self.alias = alias
        self.fullarm_hw = OutputDevice(trigger_pins[0], pin_factory=self.factory)
        self.homearm_hw = OutputDevice(trigger_pins[1], pin_factory=self.factory)
        self.sysarm_hw = Button(listen_pins[0], pin_factory=self.factory)
        self.alarm_hw = Button(listen_pins[1], pin_factory=self.factory)
        
        self.logger = Log2File(log_filename, name_of_master=self.alias, 
            time_in_log=1, screen=1)
        
        self.check_state_on_boot(trigger_pins, listen_pins)
        
        self.monitor_state()

    def monitor_state(self):
        def const_check_state():
            tmp_status=self.fullarm_hw.value, self.homearm_hw.value, self.sysarm_hw.value, self.alarm_hw.value 
            if tmp_status != self.last_state:
                for i, current_gpio in enumerate(tmp_status):
                    if self.last_state[i] != current_gpio:
                        self.last_state[i] = current_gpio
                        self.notify('[%s] :%s'%(msgs[i], current_gpio))
        
        msgs=['Full-mode Arm','Home-mode','System Arm state','Alarm state']
        
        self.cbit.append_process(const_check_state)
        self.cbit.init_thread()

    def check_state_on_boot(self, trigger_pins, listen_pins):
        # check triggers at boot
        self.notify("%s start" % self.alias)
        self.notify("IP [%s]" % self.ip_pi)
        self.notify("trigger IOs [%d, %d]" % (trigger_pins[0], trigger_pins[1]))
        self.notify("Indications IOs [%d, %d]" % (listen_pins[0], listen_pins[1]))

        if any([self.homearm_hw.value, self.fullarm_hw.value]):
            al_stat = '@BOOT- System Armed'
        else:
            al_stat = '@Boot -System Unarmed'

        self.notify(al_stat)

    def notify(self, msg):
        self.logger.append_log(msg)

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

from localswitches import Log2File
import getip
import cbit


GPIOMonitor()

