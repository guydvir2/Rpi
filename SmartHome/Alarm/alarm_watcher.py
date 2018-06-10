from gpiozero import Button
from signal import pause
from gpiozero.pins.pigpio import PiGPIOFactory
from sys import platform, path
import datetime
import tkinter as tk
from tkinter import ttk
from time import sleep


class GPIOMonitor:
    def __init__(self, pin, pin_factory=None, alias='gpio_monitor',
                 trigger_pins=[17, 21], listen_pins=[16, 26]):

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
        self.cbit = CBit()
        self.run_gmail_service()
        self.check_state_on_boot(pin, pin_factory)

    def create_gpios(self):
        self.trigger_vector, self.listen_vector = [], []

        for pin in self.trigger_pins:
            self.trigger_vector.append(Button(pin, pin_factory=self.factory))
        for pin1 in self.listen_pins:
            self.listen_vector.append(Button(pin1, pin_factory=self.factory))
            
        print(self.trigger_vector, self.listen_vector)


    def change_state_notifications(self):
        # Triggers        
        msgs = ['Full-mode alarm switched OFF', 'Full-mode alarm switched ON', 'Home-mode alarm switched OFF',
                'Home-mode alarm switched ON']
        for i, trig in enumerate(self.trigger_vector):
            trig.when_released = lambda: self.notify(msgs[i])
            trig.when_pressed = lambda: self.notify(msgs[i + 1])

        # Indications 
        msgs = ['Alarm Stopped', 'Alarm is ON', 'System Armed''System Disarmed']
        for i, listen in enumerate(self.listen_vector):
            listen.when_released = lambda: self.notify(msgs[i])
            listen.when_pressed = lambda: self.notify(msgs[i + 1])

    def check_state_on_boot(self, pin, pin_factory):
        boot_msg = "%s start, monitoring GPIO [%d] of IP [%s]" % (self.alias, pin, pin_factory)
        # check triggers at boot
        if any(self.trigger_vector):
            al_stat = 'System Armed'
        else:
            al_stat = 'System Unarmed'
                                                                                                                                               

    def run_gmail_service(self):
        path = main_path + 'modules/'
        self.gmail = gmail_mod.GmailSender(sender_file=path + 'ufile.txt',
                                           password_file=path + 'pfile.txt')

    def email_notify(self, msg, sbj=None):
        self.gmail.compose_mail(recipients=['guydvir.tech@gmail.com'],
                                body=msg, subject=sbj)

    def notify(self, msg):
        self.logger.append_log(msg)
        # self.email_notify(msg=self.logger.msg, sbj='HomePi: %s' % (self.alias))


class AlarmControlGUI(ttk.Frame, GPIOMonitor):
    def __init__(self, master=None):
        self.log_stack = []
        self.arm_value = tk.IntVar()
        self.alarm_on_value = tk.IntVar()
        self.arm_home_value = tk.IntVar()
        self.arm_full_value = tk.IntVar()
        self.armed_ent_value = tk.StringVar()
        self.alert_ent_value = tk.StringVar()
        
        ttk.Frame.__init__(self)
        GPIOMonitor.__init__(self, 21, '192.168.2.113', 'Alarm Monitor')
        # Frames
        self.mainframe = ttk.Frame(master)
        self.mainframe.grid()
        self.dashboard_frame = ttk.LabelFrame(self.mainframe, text="System Arm modes")
        self.dashboard_frame.grid(row=1, column=0, pady=10)
        self.indicators_frame = ttk.Labelframe(self.mainframe, text="System Indicators")
        self.indicators_frame.grid(row=1, column=1)
        self.activity_log_frame = ttk.Frame(self.mainframe)
        self.activity_log_frame.grid(row=0, column=0, columnspan=3)
        self.status_frame = ttk.Label(self.mainframe)
        self.status_frame.grid(row=2, column=0)#, columnspan=3)

        self.create_buttons()
        self.create_indicators()
        self.constant_chk_gpio()

        self.cbit.append_process(self.constant_chk_gpio)
        self.cbit.init_thread()
        self.log_window()
        self.write2log("BOOT")
        self.status_bar()

    def create_buttons(self):
        # Buttons
        pdx, pdy = 4, 4
        

        self.full_arm_button = tk.Checkbutton(self.dashboard_frame, text="Full", width=10, variable=self.arm_full_value,
                                              indicatoron=0, height=2, command=lambda: self.arm_buttons(0))
        self.full_arm_button.grid(row=0, column=0, padx=pdx, pady=pdy)

        self.home_arm_button = tk.Checkbutton(self.dashboard_frame, text="Home", width=10, variable=self.arm_home_value,
                                              indicatoron=0, height=2, command=lambda: self.arm_buttons(1))
        self.home_arm_button.grid(row=0, column=1, padx=pdx, pady=pdy)

        self.exit_button = ttk.Button(self.mainframe, text="EXIT", command=self.exit_button_cb)
        self.exit_button.grid(row=1, column=2, padx=pdx, pady=pdy)

    def create_indicators(self):
        pdx, pdy = 4, 4
        system_armed_label = tk.Label(self.indicators_frame, text='Armed: ', height=2)
        system_armed_label.grid(row=0, column=0, padx=pdx, pady=pdy)
        self.system_armed_ent = ttk.Entry(self.indicators_frame, width=3, textvariable=self.armed_ent_value)
        self.system_armed_ent.grid(row=0, column=1, padx=pdx, pady=pdy)

        self.setoff_alarm_label = ttk.Label(self.indicators_frame, text='Alarming: ')
        self.setoff_alarm_label.grid(row=0, column=2, padx=pdx, pady=pdy)
        self.setoff_alarm_ent = ttk.Entry(self.indicators_frame, width=3, textvariable=self.alert_ent_value)
        self.setoff_alarm_ent.grid(row=0, column=3, padx=pdx, pady=pdy)


    def constant_chk_gpio(self):
        # arm ind
        if self.listen_vector[0].is_pressed == True:
            self.armed_ent_value.set('On')
        else:
            self.armed_ent_value.set('Off')
        # alert ind
        if self.listen_vector[1].is_pressed == True:
            self.alert_ent_value.set('On')
        else:
            self.alert_ent_value.set('Off')
            
        # print(self.listen_vector[0].is_pressed, self.listen_vector[1].is_pressed)
      
    def arm_buttons(self, but_num):
        # Full Arm was pressed
        if but_num == 0:
            if self.arm_home_value.get() == 1:
                self.arm_home_value.set(0)
                print("Button_1 was Reset")
                sleep(0.5)
            #       add another action to deactivate

            else:
                sleep(0.5)
                print("pressed OK")
                pass
        #     add action to but 0
        # Home Arm was pressed
        elif but_num == 1:
            if self.arm_full_value.get() == 1:
                self.arm_full_value.set(0)
                print("Button_0 was Reset")
                sleep(0.5)
                # add another action to deactivate

            else:
                sleep(0.5)
                pass
            #     add action to but 1

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

    def status_bar(self):
        ttk.Label(self.status_frame, text='Hey').grid(row=0, column=1)
        self.clock()

    def clock(self):
        clock_label = ttk.Label(self.status_frame)
        clock_label.grid(row=0, column=0)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clock_label.config(text=time)
        root.after(500, self.clock)

    def exit_button_cb(self):
        quit()


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


root = tk.Tk()
AlarmControlGUI(root)

root.mainloop()
