import tkinter as tk
from tkinter import ttk
from time import sleep
import datetime
import gpiozero
from gpiozero import OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import time

class Com2Log:
    """ This class sends status logs to main GUI"""
    def __init__(self, master,nick):
        self.nick = nick
        self.master = master 

    def message(self, text1):
        try:
            self.master.master.master.master.master.master.write2log('[%s]: %s'%(self.nick,text1))
        except AttributeError:
            print(text1)
        

class ScheduledEvents(ttk.Frame):
    def __init__(self, master, tasks=[], sw=[0], **kwargs):

        ttk.Frame.__init__(self, master)
        #self.master = master
        self.tasks = tasks
        self.kwargs=kwargs
        #self.frame = frame

        #This loop is in case sched vector define in 3 place wich switch to pretate
        self.sw, self.run_id=[], None
        for i,current_task in enumerate(tasks):
            try:
                self.sw.append(current_task[3])
            except IndexError:
                self.sw.append(sw)
                
        self.ent_var = tk.StringVar()
        self.ent_var.set("No Schedule") # Varabile displays remaining time to SCHED
        self.remain_time_ent = ttk.Label(self,textvariable=self.ent_var, **kwargs)
        self.remain_time_ent.grid()

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
        
        self.tasks=tasks
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
                    start_time = datetime.datetime.strptime(current_task[1], '%H:%M:%S').time()
                    stop_time = datetime.datetime.strptime(current_task[2], '%H:%M:%S').time()

                    # Before Time
                    if start_time > datetime.datetime.now().time():
                        self.result_vector[i][m] = -1

                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(day_diff),datetime.datetime.strptime(current_task[1],'%H:%M:%S').time())

                    # In Time
                    elif start_time < (datetime.datetime.now() - datetime.timedelta(seconds=1)).time() and (datetime.datetime.now() + datetime.timedelta(seconds=1)).time() < stop_time:
                        self.result_vector[i][m] = 1

                        new_date = datetime.datetime.combine(datetime.date.today(),datetime.datetime.strptime(current_task[2],'%H:%M:%S').time())
                        # print("innnn")

                    # Time to Off
                    elif (datetime.datetime.now() + datetime.timedelta(
                            seconds=2)).time() > stop_time and datetime.datetime.now().time() < stop_time:
                        self.result_vector[i][m] = 0
                        # print("offff")

                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7),datetime.datetime.strptime(current_task[1],'%H:%M:%S').time())

                    # Byond Command Times
                    else:
                        self.result_vector[i][m] = -1
                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7),datetime.datetime.strptime(current_task[1],'%H:%M:%S').time())

                # Day in Future
                elif day_in_task > datetime.date.today().isoweekday():
                    self.result_vector[i][m] = -1
                    new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta
                    (day_diff), datetime.datetime.strptime(current_task[1], '%H:%M:%S').time())


                # Day in Past, Next in Future
                elif day_in_task < datetime.date.today().isoweekday():
                    self.result_vector[i][m] = -1
                    new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7 + day_diff),datetime.datetime.strptime(current_task[1],'%H:%M:%S').time())

                self.future_on[i][m] = chop_microseconds(new_date - datetime.datetime.now())

        return self.get_state()


    def get_state(self):
        ans = [-1, -1]
        min_time = []
        for x, res_vec in enumerate(self.result_vector):
            min_time.append(min(self.future_on[x]))
            for op in res_vec:
                if op in [0, 1]:
                    ans = [op, x]  # op state = on/off x= task number
                    
        return [ans, min_time, min(min_time)]  # , self.future_on]


    def switch_descision(self):
        #MainGui=self.master.master.master.master.master.master
        # Check what Sched vector are supplied:
        def check_state(sch_stat, sw):

            def update_label(txt, color='black'):
                self.remain_time_ent['foreground'] = color
                self.ent_var.set(txt)

            # sw  to pass to x_switch method
            # if task is on ---------** and task_state is On ----------_**
            if not sch_stat[0][0] == -1 and self.master.master.task_state[sch_stat[0][1]] == 1:
                if not bool(sch_stat[0][0]) == self.master.master.get_state()[sw[sch_stat[0][1]]]:
                    self.master.master.ext_press(sw[sch_stat[0][1]], sch_stat[0][0], "Schedule Switch")
                # Which button to switch--^^on or off ----^^

            # Reset task status after sched end ( in case it was cancelled )
            elif sch_stat[0][0] == 0 and self.master.master.task_state[sch_stat[0][1]] == 0:
                self.master.master.task_state[sch_stat[0][1]] = 1
                print("task:",sch_stat[0][1] , "Schedule restored")

            # if in "On" state : show time left to "On"
            if sch_stat[0][0] == 1 and self.master.master.task_state[sch_stat[0][1]] == 1:
                update_label(str(sch_stat[2]), 'green')
                #print("opt1", self.master.master.master.master.get_state())
            # if in "off state": time to next on, in all tasks
            elif sch_stat[0][0] == -1:
                update_label(str(sch_stat[2]), 'red')
            #Stop running sch when it is aready ON
            elif sch_stat[0][0] == 1 and self.master.master.task_state[sch_stat[0][1]] == 0:
                update_label("Task %s, cancelled" % str(sch_stat[0][1]), 'red')

            elif sch_stat[0][0] == -1 and self.master.master.task_state[sch_stat[0][1]] == 0:
                update_label("Task %s, cancelleddd" % str(sch_stat[0][1]), 'orange')
                
        a=self.run_schedule()
        #print(a)
        check_state(a, self.sw)
    
        self.run_id = self.after(500, self.switch_descision)


    def close_device(self):
        if self.run_id != None:
            self.after_cancel(self.run_id)


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
        #print(self.master.master.__doc__)

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
            self.button = ttk.Button(self.frame, textvariable=self.but_var, command=self.read_time)
            self.button.grid(row=0, column=1)
            self.button.bind('<Button-1>', self.press_but)
            self.button.bind('<ButtonRelease-1>', self.release_but)

            self.label = ttk.Label(self.frame, textvariable=self.lbl_var, relief=tk.RIDGE, anchor=tk.N)
            self.label.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)

        self.entry = ttk.Entry(self.frame, textvariable=self.ent_var, justify=tk.CENTER, width=10)
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

            if self.remote ==1 and not self.master.master.get_state()[self.sw] == self.on_off_status:
                self.master.master.ext_press(self.sw, self.on_off_status, "TimeOut Switch")

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
    def __init__(self, master, frame, num_indic=2,pdy=0, pdx=3,cols=[]):
        self.master = master
        self.frame = frame
        self.t = num_indic  # Amount of indicators needed
        self.indicators = ['indicator' + str(i) for i in range(self.t)]
        self.build_gui(pdx, pdy, cols)
        self.update_indicators()
        self.run_id= None

    def update_indicators(self):
        for i in range(self.t):
            if self.master.get_state()[i] == False:
                self.indicators[i].config(bg="red")
            elif self.master.get_state()[i] == True:
                self.indicators[i].config(bg="green")

        self.run_id = self.frame.after(500, self.update_indicators)

    def build_gui(self, pdx, pdy, cols):
        # create indicators ( label changes color)
        #Use cols to define specific columns to put indicators

        if cols ==[]:lens=list(range(self.t))
        else: lens=cols

        for i,val in enumerate(lens):
            self.indicators[i] = tk.Label(self.frame, width=1, height=1, text="", bg='blue', relief=tk.SUNKEN)
            self.indicators[i].grid(row=val, column=0, sticky=tk.E, pady=pdy, padx=pdx)

    def close_device(self):
        if self.run_id != None:
            #self.after_cancel(self.run_id)
            self.frame.after_cancel(self.run_id)


class HWRemoteInput:
    # This class create a link between input_pins(HW buttons) to output pins
    def __init__(self, master=None, ip='', input_pins=[]):
        self.master = master
        factory = PiGPIOFactory(host=ip)
        
        
        
        if self.master is None:
            nick='RemoteInput Device'
        else:
            nick=self.master.nick

        self.input_pins = ["Pin_" + str(input_pins[i]) for i in range(len(input_pins))]
        for sw in range(len(self.input_pins)):
            self.input_pins[sw] = gpiozero.Button(input_pins[sw], pin_factory=factory)
            self.input_pins[sw].when_pressed = lambda arg=[sw,1]: self.pressed(arg)
            # Line below is used when button switched off - setting the command to off
            self.input_pins[sw].when_released = lambda arg=[sw,0]: self.pressed(arg)

        self.com = Com2Log(self.master, nick)
        self.com.message("[Remote-Intput][IP:%s][GPIO pins:%s]" % (ip, input_pins))

    # Detect press and make switch
    def pressed(self, arg):
        self.master.switch_type = 'HWButton Switch'
        sw, state = arg[0], arg[1] #
        self.master.ext_press(sw, state,self.master.switch_type)

    def get_state(self):
        stat = []
        for sw in (self.input_pins):
            stat.append([sw.value])
        return stat

    #Close device
    def close_device(self):
        for sw in self.output_pins:
            sw.close()
        print("Device shut done")


class HWRemoteOutput:
    # This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
    def __init__(self, master=None, ip='', output_pins=[]):
        self.master = master
        
        
        if self.master is None:
            nick='RemoteOutput Device'
        else:
            nick=self.master.nick
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

    #Close device
    def close_device(self):
        for sw in self.output_pins:
            sw.close()
        self.output_pins[0].close()
        self.com.message("Device shut done")





class CoreButton(ttk.Frame):
    
    def __init__(self, master,nickname='CoreBut.inc', hw_in=[], hw_out=[],ip_in='', ip_out='', sched_vector=[], num_buts=1):
        
        ttk.Frame.__init__(self, master)
        # Buttons&Indicators
        self.buttons_frame = ttk.Frame(self, relief=tk.SUNKEN, border=2)
        self.buttons_frame.grid(row=0, column=0)
        # Counters
        self.timers_frame = ttk.Frame(self)
        self.timers_frame.grid(row=1, column=0)
        # Extra GUI
        self.switches_frame = ttk.Frame(self)
        self.switches_frame.grid(row=2, column=0)

        #self.master = master
        if ip_in == '': ip_in = ip_out  # in case remote input is not defined
        self.HW_input = None
        self.task_state,self.switch_type= [1] * len(sched_vector),''
        self.nick = nickname

        self.label_var = tk.StringVar()
        self.on_off_var = tk.IntVar() # Enables/Disables All button's GUI
        self.enable_disable_sched_var=tk.IntVar() # Enables/ Disables Sched ( task_state)
        self.but_stat ,self.buts= [tk.IntVar() for i in range(num_buts)], []
        self.on_off_var.set(1)

        
        #create log
        self.com = Com2Log(self, self.nick)

        self.build_gui()

        #run HW I/O
        self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
        self.Indicators = Indicators(self.HW_output, self.buttons_frame,num_indic=num_buts, pdx=8)
        if not hw_in == []: self.HW_input = HWRemoteInput(self, ip_in, hw_in)


        # run Sch module
        if not sched_vector == []:
            self.SchRun = ScheduledEvents(self.timers_frame,tasks=sched_vector, sw=0)
            #self.SchRun.grid(row=0, column=0)
        else:
            self.SchRun = ScheduledEvents(self.timers_frame)

        self.SchRun.grid(row=0, column=0, pady=3)

        # run Counter module
        self.Counter = TimeOutCounter(self.timers_frame, remote=1)
        self.Counter.grid(row=1, column=0)

        self.extras_gui()

    def build_gui(self):
        raise NotImplementedError('You have to override method build_gui()')

        
    def extras_gui(self):

        ttk.Separator(self.switches_frame, orient=tk.HORIZONTAL).\
        grid(row=5, column=0, columnspan=2, sticky=tk.E + tk.W, pady=5)

        tk.Checkbutton(self.switches_frame, text='On/Off',variable=self.on_off_var,\
        indicatoron=1, command=self.disable_but).grid(row=6, column=0, sticky=tk.N)
        
        tk.Checkbutton(self.switches_frame, text='Schedule',variable=self.enable_disable_sched_var,\
        indicatoron=1, command=lambda : self.disable_sched_task(s=self.enable_disable_sched_var.get())).grid(row=7, column=0)

        # to mark checkbot on/ off according active task
        task_number = self.SchRun.get_state()[0][1]
        self.enable_disable_sched_var.set(self.task_state[task_number])

        #ttk.Button(self.switches_frame, text='Update Schedule', command=self.update_schedule).\
        #grid(row=8, column=0)


    def switch_logic(self, sw):
        # Overwritten By Button's method
        pass


    def sf_button_press(self, sw=0):
        self.switch_type = 'SFButton Switch'
        self.Counter.on = self.but_stat[sw].get()
        self.Counter.read_time()
        self.switch_logic(sw)
        if self.SchRun.get_state()[0][0]==1 and self.but_stat[sw].get()==0:
            self.disable_sched_task()


    def sf_buttonAUX_press(self, sw=1):
        self.switch_type = 'SFButton Switch'
        self.Counter.on = self.but_stat[sw].get()
        self.Counter.read_time()
        self.switch_logic(sw)
        if self.SchRun.get_state()[0][0]==1 and self.but_stat[sw].get()==0:
            self.disable_sched_task()
        

    def ext_press(self, sw, state, type_s):
        
        self.switch_type = type_s
        self.but_stat[sw].set(state)
        self.switch_logic(sw)
        if not type_s == "Schedule Switch":
            self.disable_sched_task(state)


    def disable_sched_task(self,s=0, task_num=None):
        
        state = ['Cancelled','Enabled' ]
        current_state=None
        try:  # if there is a schedule
            # if schedule in ON- disable it for next run            
            if task_num == None:
                if not self.SchRun.get_state()[0][0] == -1:
                    task_num = self.SchRun.get_state()[0][1]
                    self.ext_press(sw=0,state=s,type_s='Schedule Switch')
                    current_state=self.task_state[task_num]
                else:
                    task_num = self.SchRun.get_state()[1].index(min(self.SchRun.get_state()[1]))
                    self.task_state[task_num] = self.task_state[task_num]
                
            self.task_state[task_num] = s

            # Checkbox On/off if sched is active or not
            self.enable_disable_sched_var.set(self.task_state[task_num])
            if current_state != self.task_state[task_num]:
                self.com.message(str(self.nick)+" Task %s: %s"%(task_num,state[s]))
        
        except AttributeError:
            # No schedule to stop
            pass


    def execute_command(self, sw, stat, add_txt=''):
        if not self.HW_output.get_state()[sw]==stat:
            self.HW_output.set_state(sw, stat)
            self.but_stat[sw].set(stat)
            #self.com.message([self.switch_type, 'Main is:' + str(self.HW_output.get_state()[0]),'Switch is: ' + str(self.HW_output.get_state()[1]), add_txt])


    def get_state(self):
        return self.HW_output.get_state()


    def update_schedule(self, new_sched=[]):
        self.SchRun.update_sched(new_sched)


    def close_all(self):
        self.SchRun.close_device()
        self.Indicators.close_device()
        self.HW_output.close_device()
        try:
            if self.HW_input !=[]:
                self.HW_input.close_device()
        except AttributeError:
            print(self.nick, "No input to close")
        self.Counter.close_device()
        self.destroy()
        self.com.message(self.nick, 'Closed')


    def disable_but(self):
        state=[tk.DISABLED,tk.NORMAL]
        # set gui to on/off
        for but in self.buts:
            but.config(state=state[self.on_off_var.get()])
        #self.main_but.config(state=state[self.on_off_var.get()])
        # set run_schedule on/ off
        self.disable_sched_task()
        self.enable_disable_sched_var.set(self.on_off_var.get())








    
class UpDownButton(ttk.Frame):
    """UpDownButton Class"""
    
    def __init__(self, master, nickname='', text_up='UP', text_down='DOWN', width=15, height=3, hw_in=[], hw_out=[],ip_in='', ip_out='', sched_vector=[], sched_vector_down=[]):

        ttk.Frame.__init__(self, master)
        self.nick = nickname
        self.master = master
        self.text_up, self.text_down = text_up, text_down
        if ip_in == '': ip_in = ip_out  # in case remote input is not defined
        self.HW_input = None
        
        self.task_state,self.switch_type = [1] * len(sched_vector),''
        self.but1_var ,self.but2_var = tk.IntVar(), tk.IntVar()
        self.on_off_var = tk.IntVar() # Enables/Disables All button's GUI
        self.enable_disable_sched_var=tk.IntVar() # Enables/ Disables Sched ( task_state)
        self.but_stat = [self.but1_var, self.but2_var]
        
        self.com = Com2Log(self, self.nick)
    
        self.build_gui(text_up, text_down, width, height)

        self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
        self.Indicators = Indicators(self.HW_output, self, cols=[1,2], pdx=5)
        if not hw_in == []: self.HW_input = HWRemoteInput(self, ip_in, hw_in)

        self.check_sched_vectors(sched_vector)
        
        if not sched_vector == []:
            self.SchRun = ScheduledEvents(self, tasks=sched_vector, sw=1)
            self.SchRun.grid(row=3, column=0)
        else:
            self.SchRun = ScheduledEvents(self)
            self.SchRun.grid(row=3, column=0)

        #self.extras_gui()


    def check_sched_vectors(self,v):
        for i,current_vector in enumerate(v):
            # '*' in sched _vector for up scedule
            if '*' in current_vector[1]:
                current_vector[1] = current_vector[1].split('*')[-1].split(' ')[-1]

                try:
                    current_vector[3] = 0
                except IndexError:
                    current_vector.append(0)
            else:
                try:
                    current_vector[3] = 1
                except IndexError:
                    current_vector.append(1)


    def build_gui(self, text_up, text_down, width, height):

        self.but1 = tk.Checkbutton(self, text=text_up+'\n'+self.nick, width=width, height=height, indicatoron=0, variable=self.but1_var, command=lambda: self.sf_button_press(0))
        self.but1.grid(row=1, column=0, pady=5)

        self.but2 = tk.Checkbutton(self, text=text_down+'\n'+self.nick, width=width, height=height, indicatoron=0, variable=self.but2_var,command=lambda: self.sf_button_press(1))
        self.but2.grid(row=2, column=0)


    def extras_gui(self):

        ttk.Separator(self, orient=tk.HORIZONTAL).\
        grid(row=5, column=0, columnspan=2, sticky=tk.E + tk.W, pady=5)

        tk.Checkbutton(self, text='Enable Device',variable=self.on_off_var,\
        indicatoron=1, command=self.disable_but).grid(row=6, column=0, sticky=tk.N)
        
        tk.Checkbutton(self, text='Active Schedule',variable=self.enable_disable_sched_var,\
        indicatoron=1, command=lambda : self.disable_sched_task(s=self.enable_disable_sched_var.get())).grid(row=7, column=0)

        # to mark checkbot on/ off according active task
        task_number = self.SchRun.get_state()[0][1]
        self.enable_disable_sched_var.set(self.task_state[task_number])

        #ttk.Button(self, text='Update Schedule', command=self.update_schedule).\
        #grid(row=8, column=0)


    def switch_logic(self, sw):
        
        sw_i = [0, 1]
        if self.but_stat[sw_i[sw]].get() == 1:  # Pressed to turn on
            if self.but_stat[sw_i[sw - 1]].get() == 1:  # check if pther is on
                self.but_stat[sw_i[sw - 1]].set(0)  # turn other off
                self.execute_command(sw_i[sw - 1], 0, 'Logic Switch')  # turn other off
                sleep(0.2)
                self.execute_command(sw_i[sw], 1)  # turn on
            elif self.but_stat[sw_i[sw - 1]].get() == 0:  # if other is off
                sleep(0.2)
                self.execute_command(sw_i[sw], 1)  # turn on

        elif self.but_stat[sw_i[sw]].get() == 0:  # if pressed to turn off
            self.execute_command(sw_i[sw], 0)  # turn off
            ##Both lines below are in case of HW switch and sched_swhith together
            self.execute_command(sw_i[sw-1], 0)
            self.but_stat[sw_i[sw-1]].set(0)


    def sf_button_press(self, sw):
        self.switch_type = 'SFButton Switch'
        self.switch_logic(sw)
        if self.SchRun.get_state()[0][0]==1 and self.but_stat[sw].get()==0:
            self.disable_sched_task()
        #self.disable_sched_task()


    def ext_press(self, sw, state, type_s):
        self.switch_type = type_s
        if not type_s == "Schedule Switch":
            self.disable_sched_task()
        self.but_stat[sw].set(state)
        self.switch_logic(sw)


    def disable_sched_task(self,s=0, task_num=None):
        #task_num=0
        # Stop Schedule run if it was defined at start
        state = ['Cancelled','Enabled' ]
        current_state=None
        try:  # if there is a schedule
            # if schedule in ON- disable it for next run            
            if task_num == None:
                if not self.SchRun.get_state()[0][0] == -1:
                    task_num = self.SchRun.get_state()[0][1]
                    self.ext_press(sw=0,state=s,type_s='Schedule Switch')
                    current_state=self.task_state[task_num]
                else:
                    task_num = self.SchRun.get_state()[1].index(min(self.SchRun.get_state()[1]))
                    self.task_state[task_num] = self.task_state[task_num]
                
            self.task_state[task_num] = s
            # Checkbox On/off if sched is active or not
            self.enable_disable_sched_var.set(self.task_state[task_num])
            if current_state != self.task_state[task_num]:
                self.com.message(str(self.nick)+" Task %s: %s"%(task_num,state[s]))
        
        except AttributeError:
            # No schedule to stop
            pass
            
    #def disable_sched_task(self,sw=1):
        ## Stop Active Schedule run if
        #try:  # if there is a schedule
            ## if schedule in ON- disable it for next run
            #if not self.SchRun.get_state()[0][0] == -1:
                #active_task = self.SchRun.get_state()[0][1]
                #self.task_state[active_task] = 0
                #self.com.message("Task %s: Cancelled"%active_task) 
        #except AttributeError:
            ## No schedule to stop
            #pass

    def execute_command(self, sw, stat, add_txt=''):
        if not self.HW_output.get_state()[sw]==stat:
            self.HW_output.set_state(sw, stat)
            self.com.message([self.switch_type, 'Up is:' + str(self.HW_output.get_state()[0]),
               'Down is: ' + str(self.HW_output.get_state()[1]), add_txt])

    def get_state(self):
        return self.HW_output.get_state()

    def close_all(self):
        if self.SchRun.run_id != None:
            self.SchRun.close_device()
        if self.Indicators.run_id != None:
            self.Indicators.close_device()
        self.HW_output.close_device()
        #if self.HW_input ==[]: self.HW_input.close_device()
        self.destroy()
        self.com.message('closed')

    def disable_but(self):
        self.but1.config(state=tk.DISABLED)
        self.but2.config(state=tk.DISABLED)


class ToggleButton(ttk.Frame):
    """ToggleButton Class"""
    def __init__(self, master, nickname='ToggleButton', height=3, width=15, ip_in='', hw_in=[], ip_out='', hw_out=[],sched_vector=[]):

        ttk.Frame.__init__(self, master)
        if ip_in == '': ip_in = ip_out
        self.HW_input = None
        self.nick = nickname
        self.master = master
        
        self.but_var = tk.IntVar()
        self.on_off_var = tk.IntVar() # Enables/Disables All button's GUI
        self.enable_disable_sched_var=tk.IntVar() # Enables/ Disables Sched ( task_state)
        self.on_off_var.set(1)
        self.but_stat = [self.but_var]
        self.task_state ,self.switch_type= [1] * len(sched_vector), ''

        self.com = Com2Log(self, self.nick)
        self.enable_disable_sched_var.set(self.task_state)
        #self.on_off_var.set(1)

        self.build_gui(nickname, height, width)
        
        self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
        self.Indicators = Indicators(self.HW_output, self, num_indic=1)
        if not hw_in == []: self.HW_input = HWRemoteInput(self, ip_in, hw_in)

        self.Counter = TimeOutCounter(self, remote=1)
        self.Counter.grid(row=2, column=0)

        if not sched_vector == []:
            self.SchRun = ScheduledEvents(self, tasks=sched_vector,sw=0)
            self.SchRun.grid(row=3, column=0)
        else:
            self.SchRun = ScheduledEvents(self)
            self.SchRun.grid(row=3, column=0)


        self.extras_gui()


    def build_gui(self, nickname, height, width):
        
        self.button = tk.Checkbutton(self, text=nickname, variable=self.but_var, indicatoron=0, height=height, width=width, command=self.sf_button_press)
        self.button.grid(row=0, column=0)
        
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky=tk.E + tk.W, pady=5)
        


    def extras_gui(self):

        ttk.Separator(self, orient=tk.HORIZONTAL).\
        grid(row=5, column=0, columnspan=2, sticky=tk.E + tk.W, pady=5)

        tk.Checkbutton(self, text='Enable Device',variable=self.on_off_var,\
        indicatoron=1, command=self.disable_but).grid(row=6, column=0, sticky=tk.N)
        
        tk.Checkbutton(self, text='Active Schedule',variable=self.enable_disable_sched_var,\
        indicatoron=1, command=lambda : self.disable_sched_task(s=self.enable_disable_sched_var.get())).grid(row=7, column=0)

        # to mark checkbot on/ off according active task
        task_number = self.SchRun.get_state()[0][1]
        self.enable_disable_sched_var.set(self.task_state[task_number])

        ttk.Button(self, text='Update Schedule', command=self.update_schedule).\
        grid(row=8, column=0)

    


    def switch_logic(self, sw):
        self.execute_command(sw,self.but_stat[sw].get())
        if self.but_stat[sw].get() == 0: # Abourt Conter
            self.Counter.succ_end()
    
    def sf_button_press(self, sw=0):
        #sw=0 - 1 button only
        self.switch_type = 'SFButton Switch'
        self.Counter.on = self.but_stat[sw].get()
        self.Counter.read_time()
        self.switch_logic(sw)
        if self.SchRun.get_state()[0][0]==1 and self.but_stat[sw].get()==0:
            self.disable_sched_task()
        #self.disable_sched_task()

    def ext_press(self, sw, state, type_s):
        self.switch_type = type_s
        self.but_stat[sw].set(state)
        self.switch_logic(sw)
        if not type_s == "Schedule Switch":
            self.disable_sched_task()

            
    def disable_sched_task(self,s=0, task_num=None):
        #task_num=0
        # Stop Schedule run if it was defined at start
        state = ['Cancelled','Enabled' ]
        current_state=None
        try:  # if there is a schedule
            # if schedule in ON- disable it for next run            
            if task_num == None:
                if not self.SchRun.get_state()[0][0] == -1:
                    task_num = self.SchRun.get_state()[0][1]
                    self.ext_press(sw=0,state=s,type_s='Schedule Switch')
                    current_state=self.task_state[task_num]
                else:
                    task_num = self.SchRun.get_state()[1].index(min(self.SchRun.get_state()[1]))
                    self.task_state[task_num] = self.task_state[task_num]
                
            self.task_state[task_num] = s
            # Checkbox On/off if sched is active or not
            self.enable_disable_sched_var.set(self.task_state[task_num])
            if current_state != self.task_state[task_num]:
                self.com.message(str(self.nick)+" Task %s: %s"%(task_num,state[s]))
        
        except AttributeError:
            # No schedule to stop
            pass

    #def disable_sched_task(self,s=0):
        ## Stop Schedule run if it was defined at start
        #state = ['Cancelled','Enabled' ] 
        #try:  # if there is a schedule
            ## if schedule in ON- disable it for next run
            #if not self.SchRun.get_state()[0][0] == -1:
                #if not self.task_state[self.SchRun.get_state()[0][1]] == 0:
                    #active_task = self.SchRun.get_state()[0][1]
                    #self.task_state[active_task] = s
                    #self.com.message("Task %s: %s"%(active_task,state[s])) 
                    
        #except AttributeError:
            ## No schedule to stop
            #pass

    #def abort_restore_task(self, state):
        ## This method is to enable/ disable task_state on and off.
        #if state==0:
            #self.ext_press(sw=0,state=state,type_s='StateSwitch')
        #elif state == 1:
            #self.disable_sched_task(s=state)

                
    def execute_command(self, sw, stat, add_txt=''):
        if not self.HW_output.get_state()[sw]==stat:
            self.HW_output.set_state(sw, stat)
            self.com.message([self.switch_type, str(self.HW_output.get_state()), add_txt])

    def get_state(self):
        return self.HW_output.get_state()

    def update_schedule(self, new_sched):
        self.SchRun.update_sched(new_sched)
        print(self.nick, "Updating Schedule...")

    def close_all(self):
        self.SchRun.close_device()
        self.Indicators.close_device()
        self.HW_output.close_device()
        self.Counter.close_device()
        #if self.HW_input ==[]: self.HW_input.close_device()
        self.destroy()
        self.com.message('closed')

    def disable_but(self):
        state=[tk.DISABLED,tk.NORMAL]
        # set gui to on/off
        self.button.config(state=state[self.on_off_var.get()])
        #self.main_but.config(state=state[self.on_off_var.get()])
        # set run_schedule on/ off
        self.disable_sched_task()
        self.enable_disable_sched_var.set(self.on_off_var.get())




class MainsButton(ttk.Frame):
    """MainButton Class"""
    def __init__(self, master, nickname='MainsBut', ip_out='', hw_out=[], hw_in=[],
                 ip_in='', sched_vector=[], height=3, width=15):

        ttk.Frame.__init__(self, master)
        self.mainframe = ttk.Frame(self)
        self.master = master
        self.nick = nickname
        
        self.main_but_var = tk.IntVar()
        self.tog_but_var = tk.IntVar()
        self.label_var = tk.StringVar()
        self.on_off_var = tk.IntVar() # Enables/Disables All button's GUI
        self.enable_disable_sched_var=tk.IntVar() # Enables/ Disables Sched ( task_state)
        self.but_stat = [self.main_but_var, self.tog_but_var]
        
        self.com = Com2Log(self, self.nick)

        self.task_state ,self.switch_type = [1] * len(sched_vector), ''
        self.on_off_var.set(1)
        self.build_gui(width, height)
        
        
        self.HW_input = None

        #Using GIO HW classes
        self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
        self.Indicators = Indicators(self.HW_output, self)
        if not hw_in == []: self.HW_input = HWRemoteInput(self, ip_in, hw_in)

        self.Counter = TimeOutCounter(self, remote=1, sw=1)  # sw=1 is toggle
        self.Counter.grid(row=3, column=0)

        if not sched_vector == []:
            self.SchRun = ScheduledEvents(self, tasks=sched_vector, sw=1)
            self.SchRun.grid(row=4, column=0)
        else:
            self.SchRun = ScheduledEvents(self)
            self.SchRun.grid(row=3, column=0)

        self.extras_gui()

  
    def build_gui(self, width, height):

        self.main_but = tk.Checkbutton(self, text='Main Power', width=10, height=1, indicatoron=0,variable=self.main_but_var,fg='red', command=self.sf_button_main_press)
        self.main_but.grid(row=0, column=0, pady=5)

        self.tog_but = tk.Checkbutton(self, text=self.nick, width=width, height=height, indicatoron=0,variable=self.tog_but_var,command=self.sf_button_press)
        self.tog_but.grid(row=1, column=0)

        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        sep.grid(row=2, column=0, columnspan=2, sticky=tk.E + tk.W, pady=5)


    def extras_gui(self):

        ttk.Separator(self, orient=tk.HORIZONTAL).\
        grid(row=5, column=0, columnspan=2, sticky=tk.E + tk.W, pady=5)

        tk.Checkbutton(self, text='Enable Device',variable=self.on_off_var,\
        indicatoron=1, command=self.disable_but).grid(row=6, column=0, sticky=tk.N)
        
        tk.Checkbutton(self, text='Active Schedule',variable=self.enable_disable_sched_var,\
        indicatoron=1, command=lambda : self.disable_sched_task(s=self.enable_disable_sched_var.get())).grid(row=7, column=0)

        # to mark checkbot on/ off according active task
        task_number = self.SchRun.get_state()[0][1]
        self.enable_disable_sched_var.set(self.task_state[task_number])

        #ttk.Button(self, text='Update Schedule', command=self.update_schedule).\
        #grid(row=8, column=0)


    def switch_logic(self, sw):
        if self.but_stat[0].get() == 1 and self.but_stat[1].get() == 1:  # Toggle on when Mains is on
            self.execute_command(1, 1)
        elif self.but_stat[0].get() == 0 and self.but_stat[1].get() == 1:  # Toggle off after Mains is off
            self.execute_command(1, 0)
            self.Counter.succ_end()
            self.but_stat[1].set(0) 
        elif self.but_stat[1].get() == 0:  # Stop Counter when toggle is pressed off
            self.execute_command(1, 0)
            self.Counter.succ_end()


    def sf_button_press(self, sw=1):
        self.switch_type = 'SFButton Switch'
        self.Counter.on = self.but_stat[sw].get()
        self.Counter.read_time()
        self.switch_logic(sw)
        if self.SchRun.get_state()[0][0]==1 and self.but_stat[sw].get()==0:
            self.disable_sched_task()


    def sf_button_main_press(self, sw=0):
        self.switch_type = "MainsButton Switch"
        self.execute_command(sw, self.but_stat[sw].get())  # set HWoutput on/ off
        self.switch_logic(sw)
        if self.but_stat[sw].get()==0: #cancel only when mainswitch is set to off
            self.disable_sched_task()


    def ext_press(self, sw, state, type_s):
        self.switch_type = type_s
        self.but_stat[sw].set(state)
        self.switch_logic(sw)
        if not type_s == "Schedule Switch":
            self.disable_sched_task(state)


    def disable_sched_task(self,s=0, task_num=None):
        #task_num=0
        # Stop Schedule run if it was defined at start
        state = ['Cancelled','Enabled' ]
        current_state=None
        try:  # if there is a schedule
            # if schedule in ON- disable it for next run            
            if task_num == None:
                if not self.SchRun.get_state()[0][0] == -1:
                    task_num = self.SchRun.get_state()[0][1]
                    self.ext_press(sw=1,state=s,type_s='Schedule Switch')
                    current_state=self.task_state[task_num]
                else:
                    task_num = self.SchRun.get_state()[1].index(min(self.SchRun.get_state()[1]))
                    self.task_state[task_num] = self.task_state[task_num]
                
            self.task_state[task_num] = s

            # Checkbox On/off if sched is active or not
            self.enable_disable_sched_var.set(self.task_state[task_num])
            if current_state != self.task_state[task_num]:
                self.com.message(str(self.nick)+" Task %s: %s"%(task_num,state[s]))
        
        except AttributeError:
            # No schedule to stop
            pass


    def execute_command(self, sw, stat, add_txt=''):
        if not self.HW_output.get_state()[sw]==stat:
            self.HW_output.set_state(sw, stat)
            self.but_stat[sw].set(stat)
            self.com.message([self.switch_type, 'Main is:' + str(self.HW_output.get_state()[0]),'Switch is: ' + str(self.HW_output.get_state()[1]), add_txt])


    def get_state(self):
        return self.HW_output.get_state()


    def update_schedule(self, new_sched=[]):
        self.SchRun.update_sched(new_sched)


    def close_all(self):
        self.SchRun.close_device()
        self.Indicators.close_device()
        self.HW_output.close_device()
        try:
            if self.HW_input !=[]:
                self.HW_input.close_device()
        except AttributeError:
            print(self.nick, "No input to close")
        self.Counter.close_device()
        self.destroy()
        self.com.message(self.nick, 'Closed')


    def disable_but(self):
        state=[tk.DISABLED,tk.NORMAL]
        # set gui to on/off
        self.tog_but.config(state=state[self.on_off_var.get()])
        self.main_but.config(state=state[self.on_off_var.get()])
        # set run_schedule on/ off
        self.disable_sched_task()
        self.enable_disable_sched_var.set(self.on_off_var.get())

        

class ErrBut(ttk.Frame):
    def __init__(self,master,name=''):
        ttk.Frame.__init__(self,master)
        self.mainframe = ttk.Frame(self)
        self.mainframe.grid()

        self.create_but(name)


    def create_but(self,name):
        if name=='': name='ErrBut'
        ttk.Label(self.mainframe,text="%s\nNOT loaded"%name,font=12,\
         justify=tk.CENTER, relief=tk.SUNKEN, border=1, width=12).grid(sticky=tk.E)


    def get_state(self):
        pass

    def close_all(self):
        self.destroy()




class ToggleBut2(CoreButton):
    """ToggleBut2 Class"""
    def __init__(self, master, nickname="Gen.ToggleButton", hw_in=[], hw_out=[],ip_in='', ip_out='', sched_vector=[]):
        CoreButton.__init__(self, master, nickname=nickname, hw_in=hw_in, hw_out=hw_out, ip_in=ip_in, ip_out=ip_out, sched_vector=sched_vector, num_buts=1)
        self.master = master
        self.nick = nickname

    def build_gui(self, height=3, width=13):
        
        self.button_0 = tk.Checkbutton(self.buttons_frame, text=self.nick, variable=self.but_stat[0], indicatoron=0, height=height, width=width, command=self.sf_button_press)
        self.button_0.grid(row=0, column=0, pady=2,padx=5)
        self.buts.append(self.button_0)

        #self.button_1 = tk.Checkbutton(self.buttons_frame, text="MainSwitch", variable=self.but_stat[1], indicatoron=0, height=1, width=width)
        #self.button_1.grid(row=1, column=0, pady=2)
        #self.buts.append(self.button_1)
        
        #ttk.Separator(self.timers_frame,orient=tk.HORIZONTAL).grid(row=0, column=0, columnspan=2, sticky=tk.E + tk.W, pady=5)

    
    def switch_logic(self, sw):
        self.execute_command(sw,self.but_stat[sw].get())
        if self.but_stat[sw].get() == 0: # Abourt Conter
            self.Counter.succ_end()





class UpDownButton2(CoreButton):
    """UpDown2 Class"""
    def __init__(self, master, nickname="Gen.UpDownButton", hw_in=[], hw_out=[],ip_in='', ip_out='', sched_vector=[]):
        CoreButton.__init__(self, master, nickname=nickname, hw_in=hw_in, hw_out=hw_out, ip_in=ip_in, ip_out=ip_out, sched_vector=sched_vector, num_buts=2)
        self.master = master
        self.nick = nickname

    def build_gui(self, height=3, width=13):
        
        self.button_0 = tk.Checkbutton(self.buttons_frame, text=self.nick[0], variable=self.but_stat[0], indicatoron=0, height=height, width=width, command=self.sf_button_press)
        self.button_0.grid(row=1, column=0, pady=2,padx=5)
        self.buts.append(self.button_0)

        self.button_1 = tk.Checkbutton(self.buttons_frame, text=self.nick[1], variable=self.but_stat[1], indicatoron=0, height=3, width=width)
        self.button_1.grid(row=0, column=0, pady=2)
        self.buts.append(self.button_1)
        
        #ttk.Separator(self.timers_frame,orient=tk.HORIZONTAL).grid(row=0, column=0, columnspan=2, sticky=tk.E + tk.W, pady=5)

    

    

        
button_list = {1: 'UpDownButton', 2: 'ToggleButton', 3: 'MainsButton', 4:'ErrBut'}

if __name__ == "__main__" :
    
    root = tk.Tk()
    mainframe = ttk.Frame(root)
    mainframe.grid()
    frame1 = ttk.LabelFrame(mainframe, text="Main-Shutter", padding=5)
    frame1.grid(row=0, column=0, sticky=tk.N, padx=5)
    frame2 = ttk.LabelFrame(mainframe, text="UpnDown", padding=5)
    frame2.grid(row=0, column=1, sticky=tk.N, padx=5)
    frame3 = ttk.LabelFrame(mainframe, text="Toggle", padding=5)
    frame3.grid(row=0, column=2, sticky=tk.N, padx=5)
    frame4 = ttk.LabelFrame(mainframe, text="ErrorBut", padding=5)
    frame4.grid(row=0, column=3, sticky=tk.N, padx=5)

    #a = MainsButton(frame1, ip_out='192.168.2.114', hw_out=[5, 7], hw_in=[13, 21], height=3, width=15,ip_in='192.168.2.114', sched_vector=[[[5,3], "02:24:30", "23:12:10"], [[4], "1:42:00", "23:50:10"]])
    #a.grid(row=0, column=0)

    #c = UpDownButton(frame2, hw_out=[5,7], ip_out='192.168.2.113', nickname="UpDown", hw_in=[13, 21],sched_vector=[[[1], "*09:17:00", "20:42:10",1]])#,[[0], "*18:43:20", "21:05:30",1]])#,sched_vector_down=[[[1], "11:37:30", "11:38:00"], [[2], "14:26:40", "22:03:10"]])
    #c.grid(row=0, column=1)

    #b = ToggleButton(frame3, ip_out="192.168.2.113", hw_out=[5], hw_in=[19],sched_vector=[[[2], "23:30:00", "23:30:30"], [[6], "00:00:40", "23:59:00"]])
    #b.grid(row=0, column=2)

    #b.update_schedule(new_sched=[[[6], "03:30:00", "23:30:30"]])

    #d= ErrBut(frame4, ip_out='192.168.2.114', hw_out=[5, 7], hw_in=[13, 21], height=3, width=15,ip_in='192.168.2.114', sched_vector=[[[5,3], "02:24:30", "23:12:10"], [[4], "1:42:00", "23:50:10"]])
    #d.grid(row=0, column=3)

    e= ToggleBut2(frame4,nickname='NewToggle',ip_out='192.168.2.114', hw_out=[5, 7], hw_in=[13, 21], ip_in='192.168.2.114', sched_vector=[[[7,3], "02:24:30", "23:12:10"], [[4], "1:42:00", "23:50:10"]])
    e.grid()

    f= UpDownButton2(frame4,nickname=['Down','Up'],ip_out='192.168.2.115', hw_out=[5, 7], hw_in=[13, 21], ip_in='192.168.2.115', sched_vector=[[[7,3], "02:24:30", "23:12:10"], [[4], "1:42:00", "23:50:10"]])
    e.grid(row=0, column=1)
    

    root.mainloop()
