# from gpiozero import Button, Device
from signal import pause
# from gpiozero.pins.pigpio import PiGPIOFactory
from sys import platform, path
import datetime
import tkinter as tk
from tkinter import ttk


class GPIOMonitor:
    def __init__(self, pin, pin_factory=None, alias='gpio_monitor'):

        if pin_factory is None:
            local_factory = PiGPIOFactory(host='localhost')
        else:
            local_factory = PiGPIOFactory(host=pin_factory)

        self.button = Button(21, pin_factory=local_factory)
        self.button.when_released = lambda: self.notify('alarm set off')
        self.button.when_pressed = lambda: self.notify('alarm set on')
        self.alias = alias

        self.logger = Log2File('/home/guy/Documents/AlarmMonitor.log',
                               name_of_master=self.alias, time_in_log=1, screen=1)
        self.run_gmail_service()
        self.check_state_on_boot(pin, pin_factory)
        # self.notify("%s start, monitoring GPIO [%d] of IP [%s]"%
        # (self.alias,pin, pin_factory))

    def run_gmail_service(self):
        # globals = main_path
        path = main_path + 'modules/'
        self.gmail = gmail_mod.GmailSender(sender_file=path + 'ufile.txt',
                                           password_file=path + 'pfile.txt')

    def email_notify(self, msg, sbj=None):
        self.gmail.compose_mail(recipients=['guydvir.tech@gmail.com'],
                                body=msg, subject=sbj)

    def notify(self, msg):
        self.logger.append_log(msg)
        self.email_notify(msg=self.logger.msg, sbj='HomePi: %s' % (self.alias))

    def check_state_on_boot(self, pin, pin_factory):
        boot_msg = "%s start, monitoring GPIO [%d] of IP [%s]" % (self.alias, pin, pin_factory)

        if self.button.is_pressed == True:
            self.notify(boot_msg + ' alarm is on')
        else:
            self.notify(boot_msg + ' alarm is off')


class AlarmControlGUI(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self)
        # Frames
        self.mainframe = ttk.Frame(master)
        self.mainframe.grid()
        self.dashboard_frame = ttk.LabelFrame(self.mainframe, text="Commands")
        self.dashboard_frame.grid(row=1, column=0)
        self.indicators_frame = ttk.Labelframe(self.mainframe, text="Indicators State")
        self.indicators_frame.grid(row=1, column=1)
        self.activity_log_frame = ttk.Frame(self.mainframe)
        self.activity_log_frame.grid(row=0, column=0, columnspan=2)

        # Buttons
        self.full_arm_button = ttk.Button(self.dashboard_frame, text="Full-mode Arm")
        self.full_arm_button.grid(row=0, column=0)
        self.home_arm_button = ttk.Button(self.dashboard_frame, text="Home-mode Arm")
        self.home_arm_button.grid(row=0, column=1)
        self.exit_button = ttk.Button(self.dashboard_frame, text="Home-mode Arm")
        self.exit_button.grid(row=0, column=2)

        self.onoff_label = ttk.Label(self.indicators_frame, text='Arm State')
        self.onoff_label.grid(row=0, column=0)
        self.onoff_ind = ttk.Entry(self.indicators_frame, width=3)
        self.onoff_ind.grid(row=0, column=1)

        self.alarm_label = ttk.Label(self.indicators_frame, text='exit')
        self.alarm_label.grid(row=0, column=2)
        self.alarm_ind = ttk.Entry(self.indicators_frame, width=3)
        self.alarm_ind.grid(row=0, column=3)

        self.log_stack = []
        self.log_window()
        self.write2log("BOOTgt"
                       "\ngw"
                       "\nrgw"
                       "\nrt"
                       "\ngw"
                       "\nrg"
                       "rtg"
                       "rt"
                       "g"
                       "ert"
                       "ge"
                       "rtg"
                       "ert"
                       "g"
                       "ertg"
                       "er"
                       "th"
                       "rtyj"
                       "u"
                       "jtu"
                       "jkt"
                       "uyj"
                       "tu"
                       "jt"
                       "yuj"
                       "ty"
                       "ujt"
                       "yu")

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

# from localswitches import Log2File

# GPIOMonitor(21, '192.168.2.113', 'Alarm Monitor')
# pause()

root = tk.Tk()
AlarmControlGUI(root)

root.mainloop()
