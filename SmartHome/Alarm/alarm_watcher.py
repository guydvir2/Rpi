from gpiozero import Button, Device
from signal import pause
from gpiozero.pins.pigpio import PiGPIOFactory
from sys import platform, path
import datetime
import tkinter as tk
from tkinter import ttk


class GPIOMonitor:
    def __init__(self, pin, pin_factory=None, alias='gpio_monitor',
                 trigger_pins=[20,21],listen_pins=[16,26]):

        if pin_factory is None:
            self.factory = PiGPIOFactory(host='localhost')
        else:
            self.factory = PiGPIOFactory(host=pin_factory)
            
        self.trigger_pins, self.listen_pins = trigger_pins, listen_pins

        self.alias = alias
        self.create_gpios()
        self.change_state_notifications()

        self.logger = Log2File('/home/guy/Documents/AlarmMonitor.log',
                               name_of_master=self.alias, time_in_log=1, screen=1)
#        self.cbit = CBit()
#        self.cbit.append_process(self.constant_chk_gpio)
#        self.cbit.init_thread()
        self.run_gmail_service()
        self.check_state_on_boot(pin, pin_factory)
        
    def create_gpios(self):
        self.trigger_vector, self.listen_vector=[],[]
        
        for pin in self.trigger_pins:
            self.trigger_vector.append(Button(pin, pin_factory=self.factory))
        for pin1 in self.listen_pins:
            self.listen_vector.append(Button(pin1, pin_factory=self.factory))
            
#        self.full_alarm_sw = Button(self.trigger_pins[0], 
#                                    pin_factory=self.factory)
#        self.home_alarm_sw = Button(self.trigger_pins[1], 
#                                    pin_factory=self.factory)
#        self.alarm_setoff_ind = Button(self.listen_pins[0], 
#                                       pin_factory=self.factory)
#        self.alarm_armed_ind = Button(self.listen_pins[1], 
#                                      pin_factory=self.factory)
    
    def change_state_notifications(self):
        # Triggers        
        msgs=['Full-mode alarm switched OFF','Full-mode alarm switched ON','Home-mode alarm switched OFF','Home-mode alarm switched ON' ]
        for i,trig in enumerate(self.trigger_vector):
            trig.when_released = lambda: self.notify(msgs[i])
            trig.when_pressed = lambda: self.notify(msgs[i+1])
#        self.full_alarm_sw.when_released = lambda: \
#        self.notify()
#        self.full_alarm_sw.when_pressed = lambda: \
#        self.notify()
#        self.home_alarm_sw.when_released = lambda: \
#        self.notify()
#        self.home_alarm_sw.when_pressed = lambda: \
#        self.notify()
        
        # Indications 
        msgs=['Alarm Stopped','Alarm is ON','System Armed''System Disarmed']
        for i,listen in enumerate(self.listen_vector):
            listen.when_released = lambda: self.notify(msgs[i])
            listen.when_pressed = lambda: self.notify(msgs[i+1])
            
#        self.alarm_setoff_ind.when_released = lambda: \
#        self.notify('Alarm Stopped')
#        self.alarm_setoff_ind.when_pressed = lambda: \
#        self.notify('Alarm is ON')
#        self.alarm_armed_ind.when_released = lambda: \
#        self.notify('Alarm is Armed')
#        self.alarm_armed_ind.when_pressed = lambda: \
#        self.notify('Alarm is Disarmed')
        
    def check_state_on_boot(self, pin, pin_factory):
        boot_msg = "%s start, monitoring GPIO [%d] of IP [%s]" % (self.alias, pin,pin_factory)
        # check triggers at boot
        if any(self.trigger_vector):
            al_stat='System Armed'
        else:
            al_stat='System Unarmed'
            
#        if 
#
##        if self.trigger_vector[0].is_pressed == True:
##                al_stat='On in Full-mode'
##        elif self.home_alarm_sw.is_pressed == True:
##                al_stat='On in Home-mode'
#        elif self.home_alarm_sw.is_pressed == False and self.full_alarm_sw.is_pressed == False:
#            al_stat = 'Alarm is Off'
#            
#        for n,trigger in enumerate(self.trigger_pins):
#            print(trigger,trigger.is_pressed)
#
#        self.notify(boot_msg + ' alarm is [%s]'%al_stat)


    def run_gmail_service(self):
        path = main_path + 'modules/'
        self.gmail = gmail_mod.GmailSender(sender_file=path + 'ufile.txt',
                                           password_file=path + 'pfile.txt')

    def email_notify(self, msg, sbj=None):
        self.gmail.compose_mail(recipients=['guydvir.tech@gmail.com'],
                                body=msg, subject=sbj)

    def notify(self, msg):
        self.logger.append_log(msg)
        #self.email_notify(msg=self.logger.msg, sbj='HomePi: %s' % (self.alias))


class AlarmControlGUI(ttk.Frame, GPIOMonitor):
    def __init__(self, master=None):
        ttk.Frame.__init__(self)
        GPIOMonitor.__init__(self, 21, '192.168.2.113', 'Alarm Monitor')
        # Frames
        self.mainframe = ttk.Frame(master)
        self.mainframe.grid()
        self.dashboard_frame = ttk.LabelFrame(self.mainframe, text="Commands")
        self.dashboard_frame.grid(row=1, column=0)
        self.indicators_frame = ttk.Labelframe(self.mainframe, 
                                               text="Indicators State")
        self.indicators_frame.grid(row=1, column=1)
        self.activity_log_frame = ttk.Frame(self.mainframe)
        self.activity_log_frame.grid(row=0, column=0, columnspan=2)
        
        self.create_buttons()

    def create_buttons(self):
        # Buttons
        pdx=4
        pdy=4
        self.arm_value=tk.IntVar()
        self.alarm_on_value = tk.IntVar()
        self.arm_home_value = tk.IntVar()
        self.arm_full_value = tk.IntVar()
        
        self.full_arm_button = tk.Checkbutton(self.dashboard_frame, 
                                              text="Full",width=10,
                                              variable=self.arm_full_value, 
                                              indicatoron=0, height=2)
        self.full_arm_button.grid(row=0, column=0,padx=pdx, pady=pdy)
        
        self.home_arm_button = tk.Checkbutton(self.dashboard_frame, 
                                               text="Home",width = 10,
                                               variable=self.arm_home_value, 
                                               indicatoron=0, height=2)                                    
        self.home_arm_button.grid(row=0, column=1,padx=pdx, pady=pdy)
        
        self.exit_button = ttk.Button(self.dashboard_frame, text="EXIT")
        self.exit_button.grid(row=0, column=2,padx=pdx, pady=pdy)

        self.onoff_label = tk.Label(self.indicators_frame, text='Arm State', fg='red')
        #self.onoff_label['fg']='blue'
        self.onoff_label.grid(row=0, column=0)
        self.onoff_ind = ttk.Entry(self.indicators_frame, width=3)
        self.onoff_ind.grid(row=0, column=1)

        self.alarm_label = ttk.Label(self.indicators_frame, text='Alarm')
        self.alarm_label.grid(row=0, column=2)
        self.alarm_ind = ttk.Entry(self.indicators_frame, width=3)
        self.alarm_ind.grid(row=0, column=3)

        self.log_stack = []
        self.log_window()
        self.write2log("BOOTgt")
        self.constant_chk_gpio()
    
    def constant_chk_gpio(self):
#        self.arm_value.set(self.alarm_armed_ind.is_pressed)
#        self.alarm_on_value.set(self.alarm_setoff_ind.is_pressed)
# print(self.alarm_armed_ind.is_pressed,self.alarm_setoff_ind.is_pressed )
        print(self.listen_vector)
        
    def log_window(self):
        # Create log window
        self.log_text = tk.Text(self.activity_log_frame, bg='white', wrap=tk.NONE, height=10)
        self.log_text.grid(row=0, column=0)  # , sticky=tk.E + tk.W+tk.N+tk.S)
        scrollbar_y = ttk.Scrollbar(self.activity_log_frame, orient=tk.VERTICAL)
        scrollbar_y.grid(row=0, column=1, sticky=tk.N + tk.S)
        scrollbar_y.config(command=self.log_text.yview)
        scrollbar_x = ttk.Scrollbar(self.activity_log_frame, orient=tk.HORIZONTAL)
        scrollbar_x.grid(row=0, column=0, sticky=tk.E + tk.W + tk.S)
        scrollbar_x.config(command=self.log_text.xview)

        self.log_text.config(yscrollcommand=scrollbar_y.set)
        self.log_text.config(xscrollcommand=scrollbar_x.set)
        self.log_text.config(state=tk.DISABLED)

    def write2log(self, text_in):
        try:
            self.log_text.config(state=tk.NORMAL)
            time2log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-5]
            start = tk.END
            if self.log_stack != []:
                for msg in self.log_stack:
                    self.log_text.insert(start, msg)
                    start = tk.END
                self.log_stack = []
            self.log_text.insert(start, "[" + str(time2log) + "] " + text_in + "\n")
            self.log_text.config(state=tk.DISABLED)
        except AttributeError:
            # Stack log prior to boot of log
            time2log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.log_stack.append('[' + str(time2log) + '] ' + text_in + '\n')


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
from cbit import CBit

#GPIOMonitor(21, '192.168.2.113', 'Alarm Monitor')
#pause()

root = tk.Tk()
AlarmControlGUI(root)

root.mainloop()
