import tkinter as tk
from tkinter import ttk
from time import sleep
import datetime
# import gpiozero
# import pigpio
# from gpiozero import OutputDevice
# from gpiozero.pins.pigpio import PiGPIOFactory
import time
import os


class Com2Log:
    """ This class sends status logs to main GUI"""

    def __init__(self, master, nick):
        self.nick = nick
        self.master = master

    def message(self, text1):

        time_now = str(datetime.datetime.now())[:-5]
        text2 = '[%s] %s' % (time_now, text1)
        try:
            self.master.master.master.master.master.master.master.write2log(text2)
        except AttributeError:
            print(text2)


class ScheduledEvents(ttk.Frame):

    def __init__(self, master, tasks=[], sw=[0], **kwargs):

        ttk.Frame.__init__(self, master)
        self.tasks = tasks
        self.kwargs = kwargs
        self.sw, self.run_id = sw, None
        self.ent_var = tk.StringVar()
        self.ent_var.set("No Schedule")  # Varabile displays remaining time to SCHED

        self.style = ttk.Style()
        self.style.configure("Blue2.TLabel", background=self.master.master.master.bg)

        self.remain_time_ent = ttk.Label(self, textvariable=self.ent_var, \
            **kwargs, anchor=tk.E, style="Blue2.TLabel")
        self.remain_time_ent.grid(row=0, column=0, sticky=tk.W + tk.E)

        self.prep_to_run()

    def prep_to_run(self):

        if self.tasks != []:
            self.result_vector, self.future_on = [0] * len(self.tasks), [0] * len(self.tasks)

            if self.check_integrity_time_table() == 0:
                self.run_schedule()
            else:
                print("Errors in TimeTable")

            self.switch_descision()

    def update_sched(self, tasks=[]):

        self.tasks = tasks
        self.close_device()
        self.prep_to_run()

        print(self.master.master.nick, "Schedule update, done ")

    def check_integrity_time_table(self):
        time_err, days_err = 0, 0

        for i in range(len(self.tasks)):
            time1 = datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time()
            time2 = datetime.datetime.strptime(self.tasks[i][2], '%H:%M:%S').time()

            for day_in_task in self.tasks[i][0]:
                if not day_in_task in range(1, 8):
                    print("day of task %d is not valid" % i)
                    days_err += 1

                if not time2 > time1:
                    print("Time interval of task %d is not valid" % i)
                    time_err += 1

        if time_err + days_err == 0:
            return 0  # No Errors
        else:
            return 1  # Errors on TimeTable

    def run_schedule(self):

        def time_diff(t1):
            t2 = datetime.datetime.now().time()
            today1 = datetime.date.today()
            return datetime.datetime.combine(today1, t1) - datetime.datetime.combine(today1, t2)

        def chop_microseconds(delta):
            return delta - datetime.timedelta(microseconds=delta.microseconds)

        for i, current_task in enumerate(self.tasks):  # Total tasks
            self.result_vector[i] = [2] * len(current_task[0])
            self.future_on[i] = [2] * len(current_task[0])

            for m, day_in_task in enumerate(current_task[0]):  # days in same task
                day_diff = day_in_task - datetime.datetime.today().isoweekday()

                # Today
                if day_in_task == datetime.date.today().isoweekday():
                    start_time = datetime.datetime.strptime(current_task[1], \
                                                            '%H:%M:%S').time()
                    stop_time = datetime.datetime.strptime(current_task[2], \
                                                           '%H:%M:%S').time()

                    # Before Time
                    if start_time > datetime.datetime.now().time():
                        self.result_vector[i][m] = -1
                        new_date = datetime.datetime.combine(datetime.date.today() \
                                                             + datetime.timedelta(day_diff), datetime.datetime. \
                                                             strptime(current_task[1], '%H:%M:%S').time())

                    # In Time
                    elif start_time < (datetime.datetime.now() - \
                                       datetime.timedelta(seconds=1)).time() and \
                            (datetime.datetime.now() + datetime.timedelta(seconds=1)). \
                                    time() < stop_time:
                        self.result_vector[i][m] = 1
                        new_date = datetime.datetime.combine(datetime.date.today(), \
                                                             datetime.datetime.strptime(current_task[2],
                                                                                        '%H:%M:%S').time())
                        # print("innnn")

                    # Time to Off
                    elif (datetime.datetime.now() + datetime.timedelta(seconds=2)). \
                            time() > stop_time and datetime.datetime.now().time() < \
                            stop_time:
                        self.result_vector[i][m] = 0
                        # print("offff")
                        new_date = datetime.datetime.combine(datetime.date.today() \
                                                             + datetime.timedelta(7), datetime.datetime. \
                                                             strptime(current_task[1], '%H:%M:%S').time())

                    # Byond Command Times
                    else:
                        self.result_vector[i][m] = -1
                        new_date = datetime.datetime.combine(datetime.date.today() \
                                                             + datetime.timedelta(7), datetime.datetime.strptime \
                                                                 (current_task[1], '%H:%M:%S').time())

                # Day in Future
                elif day_in_task > datetime.date.today().isoweekday():
                    self.result_vector[i][m] = -1
                    new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta
                    (day_diff), datetime.datetime.strptime(current_task[1], '%H:%M:%S').time())


                # Day in Past, Next in Future
                elif day_in_task < datetime.date.today().isoweekday():
                    self.result_vector[i][m] = -1
                    new_date = datetime.datetime.combine(datetime.date.today() \
                                                         + datetime.timedelta(7 + day_diff), datetime.datetime. \
                                                         strptime(current_task[1], '%H:%M:%S').time())

                self.future_on[i][m] = chop_microseconds(new_date - datetime.datetime.now())

        return self.get_state()

    def get_state(self):
        ans, min_time = [-1, -1], []
        for x, res_vec in enumerate(self.result_vector):
            min_time.append(min(self.future_on[x]))
            for op in res_vec:
                if op in [0, 1]:
                    ans = [op, x]  # op state = on/off x= task number

        return [ans, min_time, min(min_time)]

    def switch_descision(self):
        # Check what Sched vector are supplied:
        def check_state(sch_stat):
            ButtonClass = self.master.master.master

            def update_label(txt, color='black'):
                self.remain_time_ent['foreground'] = color
                self.ent_var.set(txt)

            # sw  to pass to x_switch method
            # if task is on ---------** and task_state is On ----------_**
            if not sch_stat [0][0] ==-1 and ButtonClass.task_state[self.sw][sch_stat[0][1]] == 1:

                ## TTO CHECK what is sw ( change to self.sw)
                if not bool(sch_stat[0][0]) == 1:# ButtonClass.get_state()[self.sw]:#[sch_stat[0][1]]]:
                    ButtonClass.ext_press(self.sw, sch_stat[0][0], "Schedule Switch")

                # TO DELETE
                # ButtonClass.ext_press(sw[sch_stat[0][1]], sch_stat[0][0], "Schedule Switch")
                # ButtonClass.ext_press(self.sw, sch_stat[0][0], "Schedule Switch")
                pass

            # Reset task status after sched end ( in case it was cancelled )
            elif sch_stat[0][0] == 0 and ButtonClass.task_state[self.sw][sch_stat[0][1]] == 0:
                ButtonClass.task_state[self.sw][sch_stat[0][1]] = 1
                update_label("task %s restored" % str(sch_stat[0][1]), 'green')
                print("task:", sch_stat[0][1], "Schedule restored")

            # if in "On" state : show time left to "On" in color green
            if sch_stat[0][0] == 1 and ButtonClass.task_state[self.sw][sch_stat[0][1]] == 1:
                update_label('On: ' + str(sch_stat[2]), 'green')

            # if in "off state": time to next on, in all tasks
            elif sch_stat[0][0] == -1 and ButtonClass.task_state[self.sw][sch_stat[1].index(sch_stat[2])] == 1:
                # ButtonClass.task_state[sch_stat[0][1]] == 1:
                update_label('wait: ' + str(sch_stat[2]), 'red')

            # Stop running sch when it is aready ON
            elif sch_stat[0][0] == 1 and ButtonClass.task_state[self.sw][sch_stat[0][1]] == 0:
                update_label("cancelled: " + str(sch_stat[2]), 'red')

            # Disable future task
            elif sch_stat[0][0] == -1 and ButtonClass.task_state[self.sw][
                sch_stat[1].index(sch_stat[2])] == 0:  # ButtonClass.task_state[sch_stat[0][1]] == 0:
                update_label("Skip: " + str(sch_stat[2]), 'orange')

        check_state(self.run_schedule())

        self.run_id = self.after(500, self.switch_descision)

    def close_device(self):
        if self.run_id != None:
            self.after_cancel(self.run_id)
            self.ent_var.set("Not Active")
            self.remain_time_ent['foreground'] = 'red'


class TimeOutCounter(ttk.Frame):
    """TimeoutCounter Class"""

    def __init__(self, master=None, remote=0, sw=0):
        ttk.Frame.__init__(self, master)
        self.frame = ttk.Frame(self)
        self.frame.grid()
        self.but_var = tk.StringVar()
        self.ent_var = tk.StringVar()
        self.lbl_var = tk.StringVar()
        self.style = ttk.Style()
        self.on = False
        self.sw = sw
        self.run_id = None
        # print(self.master.master.__doc__)

        if remote == 1:  # Use without GUI, as counter only
            self.remote = 1
            self.build_gui(gui='no')
            self.restart()

        elif not remote == 1:
            self.build_gui()
            self.restart()

    def restart(self):
        self.update_ent("Enter", 'blue')
        self.tic, self.toc = 0, 0
        self.on_off_status = 0
        self.but_var.set("Start")
        self.lbl_var.set('End time: ')

    def build_gui(self, gui=''):

        if gui == 'yes':  # GUI is on
            self.button = ttk.Button(self.frame, textvariable=self.but_var, 
                                     command=self.read_time)
            self.button.grid(row=0, column=1)
            self.button.bind('<Button-1>', self.press_but)
            self.button.bind('<ButtonRelease-1>', self.release_but)

            self.label = ttk.Label(self.frame, textvariable=self.lbl_var, 
                                   relief=tk.RIDGE, anchor=tk.N)
            self.label.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)

        self.entry = ttk.Entry(self.frame, textvariable=self.ent_var, 
                               justify=tk.CENTER, width=10)
        self.entry.bind('<Button-1>', self.clear_ent)
        self.entry.bind('<FocusOut>', self.clear_ent)
        self.entry.grid(row=0, column=0)

    def press_but(self, event):

        if self.on:
            print('stop')
            self.but_var.set('Cont.')
            self.after_cancel(self.a)
            self.on = False
        elif not self.on:
            print('press start')
            self.but_var.set('Stop')
            self.on = True

        self.tic = time.time()

    def release_but(self, event):

        self.toc = time.time() - self.tic
        print(self.toc)
        self.tic = 0

    def validate_time(self, time_input):
        timeformat = "%H:%M:%S"
        try:
            validtime = datetime.datetime.strptime(time_input, timeformat)
            a = validtime.timetuple()
            b = datetime.timedelta(hours=a.tm_hour, minutes=a.tm_min, seconds=a.tm_sec).total_seconds()
            # print('Valid time format')
            return b
        except ValueError:
            # print("invalid time format")
            return None

    def read_time(self):

        if self.toc > 0.5:
            print("long press")
            self.succ_end()
        else:
            if self.on:
                try:
                    if type(int(self.ent_var.get())) is int:
                        b = int(self.ent_var.get())
                        self.time_out(seconds=int(self.ent_var.get()))
                        t = (datetime.datetime.now() + datetime.timedelta(seconds=int(b))).strftime("%Y-%m-%d %H:%M:%S")
                        self.lbl_var.set('End time: ' + str(t))
                        if len(self.ent_var.get()) > self.entry.cget('width'):
                            self.entry["width"] = len(self.ent_var.get())
                except ValueError:
                    time1 = self.validate_time(self.ent_var.get())
                    if time1 is not None:
                        t = (datetime.datetime.now() + datetime.timedelta(seconds=int(time1))).strftime(
                            "%Y-%m-%d %H:%M:%S")
                        self.lbl_var.set('End time: ' + str(t))
                        self.time_out(seconds=time1)
                    else:
                        if not self.ent_var.get() == 'Enter':
                            self.update_ent("Bad format", 'red')
                            # time.sleep(2)
                            # self.restart()

    def time_out(self, days=0, seconds=0):

        def update_clock():
            time_left = future - datetime.datetime.now()
            if time_left.total_seconds() > 0:
                time_str = str(time_left).split('.')[0]
                self.ent_var.set(time_str)
                self.on_off_status = 1
                self.run_id = self.after(500, update_clock)
            else:
                self.on_off_status = 0
                self.succ_end()

            if self.remote == 1 and not self.master.master.master.get_state()[self.sw] == self.on_off_status:
                self.master.master.master.ext_press(self.sw, self.on_off_status, "TimeOut Switch")

        now = datetime.datetime.now()
        future = now + datetime.timedelta(days, seconds)
        update_clock()

    def update_ent(self, text, color='black'):
        self.style.configure('Guy.TEntry', foreground=color)
        self.entry['style'] = 'Guy.TEntry'
        self.ent_var.set(text)

    def clear_ent(self, event):
        if type(self.ent_var.get()) is str:
            self.ent_var.set('')

    def succ_end(self):
        try:
            self.after_cancel(self.a)
            self.restart()
        except AttributeError:
            pass
        self.on = False
        self.restart()

    def close_device(self):
        if self.run_id != None:
            self.after_cancel(self.run_id)


class Indicators:
    # This Calss displays output state of GPIO
    def __init__(self, master, frame, pdy=0, pdx=3, cols=[]):
        self.master = master
        self.frame = frame
        self.x = 0
        self.update_indicators()
       # print(self.master.get_state())
        self.run_id = None

    def update_indicators(self):

        if self.x == 120 or self.x == 1:
            self.ping_it()
            self.x = 1
        elif self.x > 20:
            self.master.master.conn_lbl['style'] = 'B.TLabel'


        self.x += 1

        for i, but in enumerate(self.master.master.buts):
            if self.master.get_state()[i] == False:
                fg, text2 = 'red', ' (Off)'
            elif self.master.get_state()[i] == True:
                fg, text2 = 'green', ' (On)'

            but.config(fg=fg)
            but.config(text=self.master.master.buts_names[i] + text2)

        self.run_id = self.frame.after(500, self.update_indicators)

    def ping_it(self):
        conn_stat = ['Connected', 'Lost']
        style = ['Green.TLabel', 'Red.TLabel']
        ping_result = os.system('ping %s -c 1 >NULL' % self.master.master.ip_out)
        self.master.master.conn_status_var.set(conn_stat[ping_result])
        self.master.master.conn_lbl['style'] = style[ping_result]

    def close_device(self):
        if self.run_id != None:
            self.master.master.conn_status_var.set('Stop')
            self.frame.after_cancel(self.run_id)
            self.x = 0



class HWRemoteInput:
    # This class create a link between input_pins(HW buttons) to output pins
    def __init__(self, master=None, ip='', input_pins=[]):
        self.master = master
        factory = PiGPIOFactory(host=ip)

        if self.master is None:
            nick = 'RemoteInput Device'
        else:
            nick = self.master.nick

        self.input_pins = ["Pin_" + str(input_pins[i]) for i in range(len(input_pins))]
        for sw in range(len(self.input_pins)):
            self.input_pins[sw] = gpiozero.Button(input_pins[sw], pin_factory=factory)
            self.input_pins[sw].when_pressed = lambda arg=[sw, 1]: self.pressed(arg)
            # Line below is used when button switched off - setting the command to off
            self.input_pins[sw].when_released = lambda arg=[sw, 0]: self.pressed(arg)

        self.com = Com2Log(self.master, nick)
        self.com.message("[Remote-Intput][IP:%s][GPIO pins:%s]" % (ip, input_pins))

    # Detect press and make switch
    def pressed(self, arg):
        self.master.switch_type = 'HWButton Switch'
        sw, state = arg[0], arg[1]  #
        self.master.ext_press(sw, state, self.master.switch_type)

    def get_state(self):
        stat = []
        for sw in (self.input_pins):
            stat.append([sw.value])
        return stat

    # Close device
    def close_device(self):
        for sw in self.output_pins:
            sw.close()
        print("Device shut done")


class HWRemoteOutput:
    # This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
    def __init__(self, master=None, ip='', output_pins=[]):
        self.master = master

        if self.master is None:
            nick = 'RemoteOutput Device'
        else:
            nick = self.master.nick
        factory = PiGPIOFactory(host=ip)
        self.output_pins = ["Pin_" + str(output_pins[i]) for i in range(len(output_pins))]
        for sw in range(len(self.output_pins)):
            self.output_pins[sw] = OutputDevice(output_pins[sw], pin_factory=factory, initial_value=False)

        self.com = Com2Log(self.master, nick)
        self.com.message("[Remote-Output][IP:%s][GPIO pins:%s]" % (ip, output_pins))

    # Make the switch
    def set_state(self, sw, state):
        if state == 1:
            self.output_pins[sw].on()
        elif state == 0:
            self.output_pins[sw].off()

    # Inquiry
    def get_state(self):
        stat = []
        for sw in range(len(self.output_pins)):
            stat.append(self.output_pins[sw].value)
        return stat

    # Close device
    def close_device(self):
        for sw in self.output_pins:
            sw.close()
        self.output_pins[0].close()
        self.com.message("Device shut done")


class CoreButton(ttk.Frame):

    def __init__(self, master, nickname='CoreBut.inc', hw_in=[], hw_out=[], ip_in='', \
                 ip_out='', sched_vector=[], sched_vector2=[], num_buts=1,on_off=1):

        ttk.Frame.__init__(self, master)
        print(self.__class__.__name__)

        # Styles
        self.style = ttk.Style()
        self.bg = 'light steel blue'
        self.style.configure("Azure.TFrame", background='azure4')
        self.style.configure("Blue.TFrame", background='blue')
        self.style.configure("Blue2.TFrame", background=self.bg)
        self.style.configure("Red.TButton", foreground='red')
        self.style.configure("Blue2.TLabel", background=self.bg)
        self.style.configure('B.TLabel', font=('helvetica', 8), \
            background=self.bg)
        self.style.configure('Green.TLabel', font=('helvetica', 8), \
            background=self.bg, foreground='green')
        self.style.configure('Red.TLabel', font=('helvetica', 8), \
            background=self.bg, foreground='red')
        self.style.configure('Title.TLabel', font=('helvetica', 10, 'bold'), \
            background=self.bg, foreground='black')

        # Frames
        # Buttons&Indicators
        py, px = 2, 2
        self.main_frame = ttk.Frame(self, style="Blue2.TFrame", \
            relief=tk.RIDGE, padding=2)
        self.main_frame.grid()

        # Display nickname of button
        ttk.Label(self.main_frame, text=self.nick, style="Title.TLabel").grid(row=0, column=0)

        self.buttons_frame = ttk.Frame(self.main_frame, height=80, width=140, \
            style="Blue2.TFrame")
        self.buttons_frame.grid_propagate(0)
        self.buttons_frame.columnconfigure(0, weight=1)
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.grid(row=1, column=0, pady=py, padx=px)

        self.sub_frame = ttk.Frame(self.buttons_frame, \
            style="Azure.TFrame", padding=(10, 5, 10, 5), relief=tk.RAISED)
        self.sub_frame.grid()

        # Counters
        self.timers_frame = ttk.Frame(self.main_frame, relief=tk.RIDGE, \
            border=2, style="Blue2.TFrame")
        self.timers_frame.grid(row=2, column=0, pady=py, padx=px, sticky=tk.E + tk.W)
        self.timers_frame.columnconfigure(0, weight=1)
        self.timers_frame.columnconfigure(1, weight=1)

        # Extra GUI
        self.switches_frame = ttk.Frame(self.main_frame, relief=tk.RIDGE, \
            style="Blue2.TFrame", padding=2, border=2)
        self.switches_frame.grid(row=3, column=0, pady=py, padx=px, sticky=tk.W + tk.E)

        # Connection to IP
        self.connection_frame = ttk.Frame(self.main_frame, relief=tk.RIDGE, \
            border=2, style="Blue2.TFrame", padding=2)
        self.connection_frame.columnconfigure(1, weight=1)
        self.connection_frame.grid(row=4, column=0, pady=py, padx=px, sticky=tk.E + tk.W)
        self.conn_status_var = tk.StringVar()
        self.conn_status_var.set('wait...')

        if ip_in == '': ip_in = ip_out  # in case remote input is not defined
        self.HW_input = None
        self.task_state, self.switch_type = [[1] * len(sched_vector), [1] * len(sched_vector2)], ''
        self.nick, self.ip_out = nickname, ip_out
        self.SchRun = []


        self.on_off_var = tk.IntVar()  # Enables/Disables All button's GUI
        self.on_off_var.set(on_off)
        self.enable_disable_sched_var = tk.IntVar()  # Enables/ Disables Sched ( task_state)
        self.but_stat, self.buts = [tk.IntVar() for i in range(num_buts)], []

        # create log
        self.com = Com2Log(self, self.nick)

        # Init Counter module
        self.Counter = TimeOutCounter(self.timers_frame, remote=1, sw=0)
        self.Counter.grid(row=0, column=1, pady=2, sticky=tk.W)

        self.counter_label = ttk.Label(self.timers_frame, text="TimeOut: ", style="Blue2.TLabel")
        self.counter_label.grid(row=0, column=0, sticky=tk.E)


        # Init Schedule module
        if not sched_vector == []:
            self.SchRun.append(ScheduledEvents(self.timers_frame, tasks=sched_vector, sw=0))
            self.SchRun[0].grid(row=1, column=0, pady=3, columnspan=2)
        else:
            self.SchRun.append(ScheduledEvents(self.timers_frame))
            self.SchRun[0].grid(row=1, column=0, pady=3, columnspan=2)
        
        # this section refer to UPDOWN button only
        if not sched_vector2 == [] and self.__class__.__name__ == 'UpDownButton':
            self.SchRun.append(ScheduledEvents(self.timers_frame, tasks=sched_vector2, sw=1))
            self.SchRun[1].grid(row=0, column=0, pady=3, columnspan=2)
        elif sched_vector2 == [] and self.__class__.__name__ == 'UpDownButton':
            self.SchRun.append(ScheduledEvents(self.timers_frame))
            self.SchRun[1].grid(row=0, column=0, pady=3, columnspan=2)
         
        
        # Run Gui
        self.build_gui()
        self.extras_gui()
        self.connection_gui()
               

        if self.pigpio_valid(self.ip_out) ==1:
            print("Reach")

            # self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
            # self.Indicators = Indicators(self.HW_output, self.buttons_frame, pdx=8)
            # if not hw_in == []: self.HW_input = HWRemoteInput(self, ip_in, hw_in)
    
        elif self.pigpio_valid(self.ip_out) == 0:
            print("Fail to reach")
            self.unSuccLoad()

        if self.on_off_var.get() == 0:
            self.disable_but()

    def pigpio_valid(self, address):
        return 1

        if pigpio.pi(address).connected == True:
            result =1
        else:
            result =0
        return result



    def build_gui(self):
        raise NotImplementedError('You have to override method build_gui()')

    def extras_gui(self):
    
        self.ck1 = tk.Checkbutton(self.switches_frame, text='On/Off', \
            variable=self.on_off_var, indicatoron=1, command= \
            self.disable_but, bg='light steel blue')
        self.ck1.grid(row=0, column=0, padx=2)

        self.ck2 = tk.Checkbutton(self.switches_frame, text='Schedule', \
            variable=self.enable_disable_sched_var, indicatoron=1, \
            command=lambda: self.disable_sched_task \
            (task_num='all'), bg='light steel blue')
        self.ck2.grid(row=0, column=1, padx=2)
        
        

        # to mark checkbot on/ off according active task
        # TO CHECK task_number = self.SchRun[0].get_state()[0][1]
        self.enable_disable_sched_var.set(1)#self.task_state[task_number])

        # ttk.Button(self.switches_frame, text='Update Schedule', command=self.update_schedule).\
        # grid(row=8, column=0)

    def connection_gui(self):
        ttk.Label(self.connection_frame, text=self.ip_out + ' :', \
            style='B.TLabel').grid(row=0, column=0)
        self.conn_lbl = ttk.Label(self.connection_frame, textvariable=self.conn_status_var, style='G.TLabel')
        self.conn_lbl.grid(row=0, column=1)

    def sf_button_press(self, sw=0,btype=''):

        if btype == '' :
            self.switch_type = 'SFButton Switch'
        else :
            self.switch_type = btype

        self.Counter.on = self.but_stat[sw].get()
        self.Counter.read_time()

        self.switch_logic(sw)

        for i, ButSch in enumerate(self.SchRun):
            if ButSch.get_state()[0][0] == 1 :
                if self.switch_type == 'SFButton Switch': # For SF Buttons
                    if self.task_state[i][ButSch.get_state()[0][1]] == 1:
                        self.disable_sched_task(sw=i)

                elif self.switch_type == 'MainsSwitch':
                    if self.task_state[i][ButSch.get_state()[0][1]] == 1:
                        if self.but_stat[1].get()== 0:
                            self.disable_sched_task(sw=i)

    def ext_press(self, sw, state, type_s):

        self.switch_type = type_s
        self.but_stat[sw].set(state)

        if not type_s == "Schedule Switch" :
            for i, ButSch in enumerate(self.SchRun):
                if ButSch.get_state()[0][0] == 1 :
                    if self.task_state[i][ButSch.get_state()[0][1]] == 1:
                        if self.HW_output.get_state()[i] is True :#
                            # ADD self.but_stat[i].get() == 0 and \: if need only from on to off
                            self.disable_sched_task(sw=i)

        self.switch_logic(sw)

    def disable_sched_task(self, state=None, sw=0, task_num=None):

        #print("in disable task")
        #states = ['Cancelled', 'Enabled']
        try:  # if there is a schedule

            # all tasks - set "on" or "off"
            if task_num == 'all':
                for i, task in enumerate(self.task_state):
                    if task !=[]:
                        self.task_state[i] = [self.enable_disable_sched_var.get() for i in task]
                        if self.enable_disable_sched_var.get() == 0:
                            self.but_stat[i].set(self.enable_disable_sched_var.get())
                            self.switch_logic(i)

            # specific task
            elif task_num != 'all':
                self.task_state[sw][self.SchRun[sw].get_state()[0][1]] = 0
                self.switch_logic(sw)

            # enable/ disable task regradless ScrRun state
            elif state is not None and state is not None:
                self.task_state[sw][task_num] = state
                self.switch_logic(sw)

        except AttributeError:
            # No schedule to stop
            print("ATTR ERR")
        print("tasks", self.task_state)

    def execute_command(self, sw, stat, add_txt=''):
        if not self.HW_output.get_state()[sw] == stat:
            self.HW_output.set_state(sw, stat)
            self.but_stat[sw].set(stat)

            text1 = ''
            for i, current_but in enumerate(self.buts_names):
                text1 = text1 + '[ %s:%s ]' % (current_but, str(self.HW_output.get_state()[i]))

            self.com.message('[ %s ][ %s ]' % (self.nick, self.switch_type) + text1)

    def get_state(self):
        # hardware status
        return self.HW_output.get_state()

    def device_status(self):
        # for future use in outer GUI
        return self.get_state(), self.SchRun.get_state()

    def update_schedule(self, new_sched=[]):
        # updating sched vetors AFTER button is already running and active
        self.SchRun.update_sched(new_sched)

    def close_all(self):
        # this method runs prior to reloading of gui
        self.SchRun.close_device()
        self.Indicators.close_device()
        self.HW_output.close_device()
        try:
            if self.HW_input != []:
                self.HW_input.close_device()
        except AttributeError:
            print(self.nick, "No input to close")
        self.Counter.close_device()
        self.destroy()
        self.com.message(self.nick, 'Closed')

    def disable_but(self):
        # this method runs in On/Off checkbox is selected
        state = [tk.DISABLED, tk.NORMAL]
        # set gui to on/off
        for i, but in enumerate(self.buts):
            but.config(state=state[self.on_off_var.get()])
            # TO RESTORE
            # self.execute_command(i, 0)  # Turn off sw=1
        # set run_schedule on/ off
        self.enable_disable_sched_var.set(self.on_off_var.get())  # Uncheck sched checkbox

        if self.on_off_var.get() == 0:
            for i in range(len(self.SchRun)):
                self.SchRun[i].close_device()
            # self.Indicators.close_device()
        else:
            for i in range(len(self.SchRun)):
                self.SchRun[i].prep_to_run()
            self.Indicators.update_indicators()

    def unSuccLoad(self):
        # this methd runs if any fail to reach ip/ pigpiod on host

        state = [tk.DISABLED, tk.NORMAL]
         
        for i, but in enumerate(self.buts):
            but.config(state=state[0])
    
        self.on_off_var.set(0)
        self.enable_disable_sched_var.set(0)  # Uncheck sched checkbox
        self.ck1.config(state=state[0])
        self.ck2.config(state=state[0])
        for sch in self.SchRun:
            sch.close_device()




class ToggleButton(CoreButton):
    """ToggleButton Class"""

    def __init__(self, master, nickname="Gen.ToggleButton", hw_in=[], hw_out=[], \
                 ip_in='', ip_out='', sched_vector=[], buts_names=['Toggle'],on_off=1):
        self.buts_names = buts_names
        self.nick = nickname
        self.master = master

        CoreButton.__init__(self, master, nickname=nickname, hw_in=hw_in, \
            hw_out=hw_out, ip_in=ip_in, ip_out=ip_out, \
            sched_vector=sched_vector, num_buts=1,on_off=on_off)
              

    def build_gui(self, height=3, width=13):
        self.button_0 = tk.Checkbutton(self.sub_frame, text=self.buts_names[0], \
            variable=self.but_stat[0], indicatoron=0, height=height, width=width, \
            command=self.sf_button_press)
        self.button_0.grid(row=0, column=0)
        self.buts.append(self.button_0)

    def switch_logic(self, sw=0):
        #
        self.execute_command(sw=sw, stat=self.but_stat[sw].get())
        if self.but_stat[sw].get() == 0:  # Abourt Conter
            self.Counter.succ_end()


class UpDownButton(CoreButton):
    """UpDown2 Class"""

    def __init__(self, master, nickname="Gen.UpDownButton", hw_in=[], \
        hw_out=[], ip_in='', ip_out='', sched_vector=[], sched_vector2=[], buts_names=['DOWN', 'UP'], on_off=1):

        self.buts_names = buts_names
        self.master = master
        self.nick = nickname

        CoreButton.__init__(self, master, nickname=nickname, hw_in=hw_in, \
            hw_out=hw_out, ip_in=ip_in, ip_out=ip_out, \
            sched_vector=sched_vector, sched_vector2=sched_vector2, num_buts=2, on_off=on_off)

        # Disabke Counter in this Button
        self.Counter.grid_forget()
        self.counter_label.grid_forget()


    def build_gui(self, height=1, width=13):
        self.button_0 = tk.Checkbutton(self.sub_frame, text=self.buts_names[0], \
            variable=self.but_stat[0], indicatoron=0, height=height, width=width, \
            command=lambda: self.sf_button_press(0))
        self.button_0.grid(row=1, column=0, pady=(2, 0))
        self.buts.append(self.button_0)

        self.button_1 = tk.Checkbutton(self.sub_frame, text=self.buts_names[1], \
            variable=self.but_stat[1], indicatoron=0, height=height, width=width, \
            command=lambda: self.sf_button_press(1))
        self.button_1.grid(row=0, column=0)
        self.buts.append(self.button_1)

    def switch_logic(self, sw):
        sw_i = [0, 1]
        sleep_time = 0.5  # seconds

        if self.but_stat[sw_i[sw]].get() == 1:  # Pressed to turn on
            if self.but_stat[sw_i[sw - 1]].get() == 1:  # If other button is "on"
                self.execute_command(sw_i[sw - 1], 0, 'Logic Switch')  # turn other off")
                #print("other set to 0")
                sleep(sleep_time)
                self.execute_command(sw_i[sw], 1)  # turn on")
                sleep(sleep_time)
                #print("button set to 1")
            elif self.but_stat[sw_i[sw - 1]].get() == 0:  # if other is off
                self.execute_command(sw_i[sw], 1)  # turn on")
                sleep(sleep_time)

        elif self.but_stat[sw_i[sw]].get() == 0:  # if pressed to turn off
             self.execute_command(sw_i[sw], 0)#  turn off")
             sleep(sleep_time)


class MainsButton(CoreButton):
    """Main2 Class"""

    def __init__(self, master, nickname="Gen.MainsButton", hw_in=[], hw_out=[],
            ip_in='', ip_out='', sched_vector=[], buts_names=['Toggle', 'MainSwitch'],on_off=1):

        self.buts_names = buts_names
        self.master = master
        self.nick = nickname

        CoreButton.__init__(self, master, nickname=nickname, hw_in=hw_in, \
            hw_out=hw_out, ip_in=ip_in, ip_out=ip_out, \
            sched_vector=sched_vector, num_buts=2, on_off=on_off)
            

    def build_gui(self, height=2, width=13):

        self.button_0 = tk.Checkbutton(self.sub_frame, text=self.buts_names[0], \
            variable=self.but_stat[0], indicatoron=0, height=height, \
            width=width, command=self.sf_button_press)
        self.button_0.grid(row=1, column=0, pady=(2, 0), sticky=tk.W)
        self.buts.append(self.button_0)

        self.button_1 = tk.Checkbutton(self.sub_frame, text=self.buts_names[1], \
            variable=self.but_stat[1], indicatoron=0, height=1, \
            width=width, command=lambda :self.sf_button_press(sw=1, btype='MainsSwitch'))
        self.button_1.grid(row=0, column=0)

        self.buts.append(self.button_1)

    def switch_logic(self, sw):

        if self.but_stat[1].get() == 0 :#and self.but_stat[0].get() == 0:
            self.execute_command(1,0)
            self.execute_command(0, 0)
            self.but_stat[0].set(0)
            self.Counter.succ_end()

        elif self.but_stat[1].get() == 1 and self.but_stat[0].get() == 0:
            self.execute_command(1,1)
            self.execute_command(0, 0)

        elif self.but_stat[1].get() == 1 and self.but_stat[0].get() == 1:
            self.execute_command(1,1)
            self.execute_command(0, 1)



button_list = {1: 'UpDownButton', 2: 'ToggleButton', 3: 'MainsButton'}

if __name__ == "__main__":
    root = tk.Tk()


    # e = ToggleButton(root, nickname='LivingRoom Lights', ip_out='192.168.2.113', \
    #     hw_out=[22,6],hw_in=[13],sched_vector=[[[4], "02:24:30", "23:12:10"], \
    #     [[2], "19:42:00", "23:50:10"], [[5], "19:42:00", "23:50:10"]])
    # e.grid(row=0, column=0, sticky=tk.S)
    #
    # f = UpDownButton(root, nickname='RoomWindow', ip_out='192.168.2.115', \
    #     hw_out=[5, 7], hw_in=[13, 21], sched_vector=[[[1], "22:24:30", \
    #     "23:12:10"], [[4,5], "12:56:00", "23:50:10"]],
    #     sched_vector2=[[[3], "1:24:30","23:12:10"]])
    # f.grid(row=0, column=1, sticky=tk.S)
    #
    # g = MainsButton(root, nickname='WaterBoiler', ip_out='192.168.2.114', \
    #     hw_out=[7, 5], hw_in=[13], sched_vector=[[[3, 2], \
    #     "02:24:30", "23:55:10"],[[4,5], "13:47:20", "23:50:10"]])
    # g.grid(row=0, column=2, sticky=tk.S)
    a=TimeOutCounter()
    a.grid()
    root.mainloop()
