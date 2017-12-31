import tkinter as tk
import gpiozero
from time import sleep
from gpiozero import OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import datetime
from tkinter import ttk
import Schedule
import csv
import os


class ScheduledEvents:
    
    def __init__(self, master= None, tasks=[]):

        self.master = master
        self.tasks = tasks
        self.result_vector, self.future_on = [0] * len(self.tasks), [0] * len(self.tasks)

        if self.check_integrity_time_table() == 0:
            self.run_schedule()
        else:
            print("Errors in TimeTable")

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

        for i in range(len(self.tasks)):
            self.result_vector[i] = [2]*len(self.tasks[i][0])
            self.future_on[i] = [2]*len(self.tasks[i][0])
            
        for i in range(len(self.tasks)): #Total tasks
            for m,day_in_task in enumerate(self.tasks[i][0]): #days in same task
                day_diff = day_in_task - datetime.datetime.today().isoweekday()

                #Today
                if day_in_task == datetime.date.today().isoweekday():
                    start_time = datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time()
                    stop_time = datetime.datetime.strptime(self.tasks[i][2], '%H:%M:%S').time()

                    #Before Time
                    if start_time > datetime.datetime.now().time():
                        self.result_vector[i][m] = -1
                        
                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(day_diff), datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())
                        #print("b4")


                    #In Time
                    elif start_time  < (datetime.datetime.now()-datetime.timedelta(seconds=1)).time() and (datetime.datetime.now() + datetime.timedelta(seconds=1)).time() < stop_time:
                        self.result_vector[i][m] = 1
                        
                        new_date = datetime.datetime.combine(datetime.date.today() , datetime.datetime.strptime(self.tasks[i][2], '%H:%M:%S').time())
                        #print("innnn")

                    #Time to Off
                    elif (datetime.datetime.now()+datetime.timedelta(seconds=2)).time() >stop_time and datetime.datetime.now().time() < stop_time  :
                        self.result_vector[i][m] = 0
                        #print("offff")

                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7) , datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())

                    # Byond Command Times
                    else :
                        self.result_vector[i][m] = -1
                        
                        new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7) , datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())



                #Day in Future
                elif day_in_task > datetime.date.today().isoweekday():
                    self.result_vector[i][m] = -1
                    
                    new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta
                    (day_diff), datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())
                    

                #Day in Past, Next in Future
                elif day_in_task < datetime.date.today().isoweekday():
                    self.result_vector[i][m] = -1
                    
                    new_date = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(7+day_diff), datetime.datetime.strptime(self.tasks[i][1], '%H:%M:%S').time())

                self.future_on[i][m] = chop_microseconds(new_date - datetime.datetime.now())

    def get_status(self):
        ans = [-1, -1]
        min_time=[]
        
        for x,res_vec in enumerate(self.result_vector):
            min_time.append(min(self.future_on[x]))
            for op in res_vec:
                if op in [0,1]:
                    ans= [op,x]#op state = on/off x= task number
       
        return [ans, min_time, min(min_time)]#, self.future_on] 


  
class Indicators:
    #This Calss displays output state of GPIO
    def __init__(self,master, frame,num_indic=2 ):
        self.master = master
        self.frame = frame
        self.t = num_indic #Amount of indicators needed
        self.indicators = ['indicator'+str(i) for i in range(self.t)]
        self.build_gui()
        self.update_indicators()
        
        
    def update_indicators(self):
        for i in range(self.t):
            if self.master.get_state()[i] == False:
                self.indicators[i].config(bg="red")
            elif self.master.get_state()[i] == True:
                self.indicators[i].config(bg="green")
                
        self.frame.after(500, self.update_indicators)

    def build_gui(self):
        #create indicators ( label changes color)
        ofset=2
        for i in range(self.t):
            self.indicators[i] = tk.Label(self.frame, width=1, height=1, text="", bg='blue',relief=tk.SUNKEN)
            self.indicators[i].grid(row=i, column=0, sticky=tk.NE,pady=ofset, padx=ofset)


class HWRemoteInput:
    #This class create a link between input_pins(HW buttons) to output pins
    def __init__(self, master, ip, input_pins):
        self.master = master
        factory = PiGPIOFactory(host=ip)
        
        self.input_pins= ["Pin_"+str(input_pins[i]) for i in range(len(input_pins))]
        for sw in range(len(self.input_pins)):
            self.input_pins[sw] = gpiozero.Button(input_pins[sw], pin_factory=factory)
            self.input_pins[sw].when_pressed = lambda arg=sw :self.pressed(arg)

        print("RemoteInput Init-%s, IP:%s, GPIO pins:%s"%(self.master.nick,ip, input_pins))


    #Detect press and make switch
    def pressed(self,i):
        self.master.switch_type = 'HWButton Switch'
        self.master.HW_Button(i, [1,0][self.master.HW_output.get_state()[i]])


    def get_state(self):
        stat=[]
        for sw in (self.input_pins):
            stat.append([sw.value])
        return stat

  
class HWRemoteOutput:
#This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
    def __init__(self, master, ip, output_pins):
        self.master = master
        factory = PiGPIOFactory(host=ip)
        self.output_pins= ["Pin_"+str(output_pins[i]) for i in range(len(output_pins))]
        for sw in range(len(self.output_pins)):
            self.output_pins[sw] = OutputDevice(output_pins[sw], pin_factory=factory,initial_value=False)
            
        print("RemoteOutput Init %s, IP:%s, GPIO pins:%s"%(self.master.nick, ip, output_pins))


    #Make the switch
    def set_state(self, sw, state):
        if state == 1:
            self.output_pins[sw].on()
        elif state == 0:
            self.output_pins[sw].off()

    #Inquiry
    def get_state(self):
        stat=[]
        for sw in range(len(self.output_pins)):
            stat.append(self.output_pins[sw].value)
        return stat



class UpDownButton(tk.Frame):

    
    #class HWRemoteOutput:
    ##This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
        #def __init__(self, master, ip, output_pins):
            #self.master = master
            #factory = PiGPIOFactory(host=ip)
            #self.output_pins= ["Pin_"+str(output_pins[i]) for i in range(len(output_pins))]
            #for sw in range(len(self.output_pins)):
                #self.output_pins[sw] = OutputDevice(output_pins[sw], pin_factory=factory,initial_value=False)
                
            #print("RemoteOutput Init %s, IP:%s, GPIO pins:%s"%(self.master.nick, ip, output_pins))


        ##Make the switch
        #def set_state(self, sw, state):
            #if state == 1:
                #self.output_pins[sw].on()
            #elif state == 0:
                #self.output_pins[sw].off()

        ##Inquiry
        #def get_state(self):
            #stat=[]
            #for sw in range(len(self.output_pins)):
                #stat.append(self.output_pins[sw].value)
            #return stat

    
    #class Indicators:
        ##This Calss displays output state of GPIO
        #def __init__(self,master, frame ):
            #self.master = master
            #self.frame = frame
            #self.t = 2 #Amount of indicators (up and down)
            #self.indicators = ['indicator'+str(i) for i in range(self.t)]
            #self.build_gui()
            #self.update_indicators()
            
            
        #def update_indicators(self):
            #for i in range(self.t):
                #if self.master.get_state()[i] == False:
                    #self.indicators[i].config(bg="red")
                #elif self.master.get_state()[i] == True:
                    #self.indicators[i].config(bg="green")
                    
            #self.frame.after(500, self.update_indicators)

        #def build_gui(self):
            ##create indicators ( label changes color)
            #ofset=8
            #for i in range(self.t):
                #self.indicators[i] = tk.Label(self.frame, width=1, height=1, text="", bg='blue',relief=tk.SUNKEN)
                #self.indicators[i].grid(row=i, column=0, sticky=tk.NE,pady=ofset, padx=ofset)


    #class HWRemoteInput:
        ##This class create a link between input_pins(HW buttons) to output pins
        #def __init__(self, master, ip, input_pins):
            #self.master = master
            #factory = PiGPIOFactory(host=ip)
            
            #self.input_pins= ["Pin_"+str(input_pins[i]) for i in range(len(input_pins))]
            #for sw in range(len(self.input_pins)):
                #self.input_pins[sw] = gpiozero.Button(input_pins[sw], pin_factory=factory)
                #self.input_pins[sw].when_pressed = lambda arg=sw :self.pressed(arg)

            #print("RemoteInput Init-%s, IP:%s, GPIO pins:%s"%(self.master.nick,ip, input_pins))


        ##Detect press and make switch
        #def pressed(self,i):
            #self.master.switch_type = 'HWButton, '
            #self.master.HW_Button(i, [1,0][self.master.HW_output.get_state()[i]])


        #def get_state(self):
            #stat=[]
            #for sw in range(len(self.input_pins)):
                #stat.append([self.input_pins[sw].value])
            #return stat


    def __init__(self, master, nickname='', text_up='UP', text_down='DOWN', width=15, height=3, hw_in=[], hw_out=[], ip_in='', ip_out='', sched_vector=[], sched_vector_down=[]):
        
        tk.Frame.__init__(self, master)
        self.nick = nickname
        self.master = master
        self.text_up = text_up
        self.text_down = text_down
        self.but_stat = []

        if ip_in =='': ip_in = ip_out
        
        self.build_buttons(text_up, text_down, width, height)
        
        self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
        Indicators(self.HW_output, self)
        if not hw_in == []: self.HW_input = HWRemoteInput(self, ip_in, hw_in)

        self.switch_type=''
        self.up,self.down=0,0

        sched_vector_up=sched_vector # to keep comm with other buttons ( for now )
        if not sched_vector_up ==[]:
            #sched_vector = [[1,"22:00:40","23:24:10"]]
            self.task_state_up = [1]*len(sched_vector_up)
            self.SchRun_Up =  ScheduledEvents(tasks=sched_vector_up)
            self.up = 1

        if not sched_vector_down ==[]:
            self.task_state_down = [1]*len(sched_vector_down)
            self.SchRun_Down =  ScheduledEvents(tasks=sched_vector_down)
            self.down = 1

        if self.up or self.down >0 :self.run_schedule()


    def run_schedule(self):

        if self.up:

            #Run Schedule
            self.SchRun_Up.run_schedule()
            sched_status_up = self.SchRun_Up.get_status()

            #Switch On/Off -------** **-----in task no.     relative task_state is On -------_**
            if not sched_status_up[0][0] == -1 and self.task_state_up[sched_status_up[0][1]]== 1:
                if not bool(sched_status_up[0][0]) == self.get_state()[0] :
                    self.sched_switch_command(0, sched_status_up[0][0])
                    #Which button to switch--^^   on or off ----^^
                
            #Reset task status after sched end ( in case it was cancelled )
            elif sched_status_up[0][0] == -1 and self.task_state_up[sched_status_up[0][1]]== 0:
                self.task_state_up[sched_status_up[0][1]]== 1

            #if in "On" state : show time left to "On"
            if sched_status_up[0][0] == 1:
                print("Off in: ",sched_status_up[1][sched_status_up[0][1]])
            #if in "off state": time to next on, in all tasks
            elif sched_status_up[0][0] == -1:
                print("Next On in: ",sched_status_up[1][sched_status_up[0][1]])
                

        if self.down:
            #Run Schedule
            self.SchRun_Down.run_schedule()
            sched_status_down = self.SchRun_Down.get_status()

            #sched_status[0][0] is switch on/off sched_status[0][1] is task number
            #if status equal to On or Off and task state wasn't disabled

            #Make Switch
            if not sched_status_down[0][0] == -1 and self.task_state_down[sched_status_down[0][1]]== 1:
                if not bool(sched_status_down[0][0]) == self.get_state()[1] :
                    self.sched_switch_command(1, sched_status_down[0][0])
                
            #Reset task status after sched end ( in case it was cancelled )
            elif sched_status_down[0][0] == -1 and self.task_state_down[sched_status_down[0][1]]== 0:
                self.task_state_down[sched_status_down[0][1]]== 1

            #if in "On" state : show time left to "On"
            if sched_status_down[0][0] == 1:
                print("Off in: ",sched_status_down[1][sched_status_down[0][1]])
            #if in "off state": time to next on, in all tasks
            elif sched_status_down[0][0] == -1:
                print("Next On in: ",sched_status_down[1][sched_status_down[0][1]])
                
        self.master.after(1000, self.run_schedule)
                

    def build_buttons(self, text_up, text_down, width, height):

        but1_var = tk.IntVar()
        but1 = tk.Checkbutton(self, text=text_up, width=width, height=height, indicatoron=0, variable=but1_var,command=self.com_up)
        but1.grid(row=0, column=0, pady=5)

        but2_var = tk.IntVar()
        but2 = tk.Checkbutton(self, text=text_down, width=width, height=height, indicatoron=0, variable=but2_var,command=self.com_down)
        but2.grid(row=1, column=0)

        label = tk.Label(self, text=self.nick)
        label.grid(row=2, column=0)

        self.but_stat = [but1_var, but2_var]


    def com_up(self, nick=''):

        if nick == '':
            self.switch_type = 'SFButton Switch'

        if not self.switch_type == 'Schedule Switch': self.disable_sched_task()

        if self.but_stat[0].get() == 1:
            if self.but_stat[1].get() == 1:
                self.but_stat[1].set(0)
                self.execute_command(0, self.but_stat[1].get())
                sleep(1)
                self.execute_command(self.but_stat[0].get(), self.but_stat[1].get())
                
            elif self.but_stat[1].get() == 0:
                self.execute_command(self.but_stat[0].get(), self.but_stat[1].get())
                
        elif self.but_stat[0].get() == 0:
            self.execute_command(self.but_stat[0].get(), self.but_stat[1].get())


    def com_down(self, nick=''):
        
        if nick == '':
            self.switch_type = 'SFButton Switch'

        if not self.switch_type == 'Schedule Switch': self.disable_sched_task()
            
        if self.but_stat[1].get() == 1:
            if self.but_stat[0].get() == 1:
                self.but_stat[0].set(0)
                self.execute_command(self.but_stat[0].get(), 0)
                sleep(1)
                self.execute_command(self.but_stat[0].get(), self.but_stat[1].get())
            elif self.but_stat[0].get() == 0:
                self.execute_command(self.but_stat[0].get(), self.but_stat[1].get())
        elif self.but_stat[1].get() == 0:
            self.execute_command(self.but_stat[0].get(), self.but_stat[1].get())


    def HW_Button(self, sw, state):

        self.switch_type = "HWButton Switch"
        self.but_stat[sw].set(state)
                
        if sw == 0:
            self.com_up(nick = self.switch_type)
        elif sw == 1:
            self.com_down(nick = self.switch_type)


    def sched_switch_command(self,sw,state):

        self.switch_type = 'Schedule Switch'
        self.but_stat[sw].set(state)
                
        if sw == 0:
            self.com_up(nick = self.switch_type)
        elif sw == 1:
            self.com_down(nick = self.switch_type)


    def disable_sched_task(self):
        # Stop Schedule run if it was defined at start

        try: # if there is a schedule
            #if schedule in ON- disable it for next run
            if not self.SchRun_Up.get_status()[0][0] == -1 :
                self.task_state_up[self.SchRun_Up.get_status()[0][1]] = 0
                print("Disabled task")                        #   ^^------toggle button
        except AttributeError:
            pass


    def execute_command(self, up_stat, down_stat):

        self.HW_output.set_state(0,up_stat)
        self.HW_output.set_state(1, down_stat)

        print([self.nick, self.switch_type, self.HW_output.get_state()])


    def get_state(self):
        return self.HW_output.get_state()



class ToggleButton(tk.Frame):

    
    class HWRemoteOutput:
    #This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
        def __init__(self,master, ip, output_pins):
            factory = PiGPIOFactory(host=ip)
            self.master = master
            self.output_pins= ["Pin_"+str(output_pins[i]) for i in range(len(output_pins))]
            for sw in range(len(self.output_pins)):
                self.output_pins[sw] = OutputDevice(output_pins[sw], pin_factory=factory,initial_value=False)
                
            print("RemoteOutput Init %s, IP:%s, GPIO pins:%s"%(self.master.nick, ip, output_pins))


        #Make the switch
        def set_state(self, sw, state):
            if state == 1:
                self.output_pins[sw].on()
            elif state == 0:
                self.output_pins[sw].off()

        #Inquiry
        def get_state(self):
            stat=[]
            for sw in range(len(self.output_pins)):
                stat.append(self.output_pins[sw].value)
            return stat

    
    class Indicators:
        
        def __init__(self,master, frame ):
            self.master = master
            self.frame = frame
            self.t = 1
            self.indicators = ['indicator'+str(i) for i in range(self.t)]
            self.build_gui()
            self.update_indicators()
            
            
        def update_indicators(self):
            for i in range(self.t):
                if str(self.master.get_state()[i]) == "False":
                    self.indicators[i].config(bg="red")
                elif str(self.master.get_state()[i]) == "True":
                    self.indicators[i].config(bg="green")
            self.frame.after(500, self.update_indicators)


        def build_gui(self):
            ofset=8
            for i in range(self.t):
                self.indicators[i] = tk.Label(self.frame, width=1, height=1, text="", bg='blue',relief=tk.SUNKEN)
                self.indicators[i].grid(row=i, column=0, sticky=tk.NE, pady=ofset, padx=ofset)


    class HWRemoteInput:
        #This class create a link between input_pins(HW buttons) to output pins
        def __init__(self, master, ip, input_pins):
            self.master = master
            factory = PiGPIOFactory(host=ip)
            
            self.input_pins= ["Pin_"+str(input_pins[i]) for i in range(len(input_pins))]
            for sw in range(len(self.input_pins)):
                self.input_pins[sw] = gpiozero.Button(input_pins[sw], pin_factory=factory)
                self.input_pins[sw].when_pressed = lambda arg=sw :self.pressed(arg)

            print("RemoteInput Init-%s, IP:%s, GPIO pins:%s"%(self.master.nick,ip, input_pins))

        #Detect press and make switch
        def pressed(self,i):
            
            self.master.switch_type = 'HWButton Switch'
            self.master.HWbutton_pressed(i,[1,0][self.master.HW_output.get_state()[i]])

        def get_state(self):
            stat=[]
            for sw in range(len(self.input_pins)):
                stat.append([self.input_pins[sw].value])
            return stat

    
    def __init__(self, master, nickname='ToggleButton', height=3, width=15, ip_in='', hw_in=[], ip_out='', hw_out=[], sched_vector=[]):
        
        tk.Frame.__init__(self, master)
        
        if ip_in == '':ip_in = ip_out
    
        self.nick = nickname
        self.master = master
        self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
        if not hw_in == [] : self.HW_input = HWRemoteInput(self, ip_in, hw_in)
        self.build_gui(self, nickname, height, width)
        self.switch_type=''
        self.last_exec=''
        self.task_state = [1]*len(sched_vector)

        if not sched_vector ==[]:
                    #sched_vector = [[1,"22:00:40","23:24:10"]]
                    self.SchRun =  ScheduledEvents(self,tasks=sched_vector)
                    self.run_schedule()


    def run_schedule(self):

        #Run Schedule
        self.SchRun.run_schedule()
        sched_status = self.SchRun.get_status()

        #sched_status[0][0] is switch on/off sched_status[0][1] is task number
        #if status equal to On or Off and task state wasn't disabled
        
        if not sched_status[0][0] == -1 and self.task_state[sched_status[0][1]]== 1:
            if not bool(sched_status[0][0]) == self.get_state() :self.sched_switch_command(0, sched_status[0][0])
   
        self.master.after(1000, self.run_schedule)


    def build_gui(self, master, nickname, height, width):
        
        def restore_timeout(event):
            if not self.txtvar.get() == self.init_var:
                try:
                    int(self.txtvar.get())
                except ValueError:
                    self.txtvar.set(self.init_var)


        def clear_timeout(event):
            self.txtvar.set("")


        self.init_var = "TimeOut [min]"
        self.but_vat = tk.IntVar()
        button = tk.Checkbutton(self, text = nickname, variable=self.but_vat, indicatoron=0, height=height, width= width, command=self.SFbutton_pressed)
        button.grid(row=0, column=0, padx=3)

        self.txtvar = tk.StringVar()
        self.txtvar.set(self.init_var)
        timeout_entry = tk.Entry(self, textvariable=self.txtvar, width=12, bg="white", fg='#4c4c4c', justify=tk.CENTER)
        timeout_entry.grid(row=2, column=0, padx=6)
        timeout_entry.bind("<Button-1>", clear_timeout)
        timeout_entry.bind("<FocusOut>", restore_timeout)

        self.Indicators(self.HW_output, self)


    def execute_command(self,state,txt=''):

         if not bool(state) == self.HW_output.get_state()[0]:
            self.but_vat.set(state)
            self.HW_output.set_state(0,state)

            print([self.nick, self.switch_type, state, txt])


    def sched_switch_command(self,i,state):
        #i irrelvant
        self.switch_type = 'Schedule Switch'
        self.execute_command(state)


    def disable_sched_task(self):
        try: # if there is a schedule
            #if schedule in ON- disable it for next run
            if not self.SchRun.get_status()[0][0] == -1 :
                self.task_state[self.SchRun.get_status()[0][0]] = 0
                                                        #   ^^------toggle button
        except AttributeError:
            pass


    def SFbutton_pressed(self):
                  
        self.switch_type = 'SFButton'
        if not self.task_state==[] : self.disable_sched_task()

        try:
            if float(self.txtvar.get()) >0:
                if self.but_vat.get() == 1 :  
                    self.execute_command(1, 'AutoOff %s minutes'%self.txtvar.get())
                    self.after(int(round(float(self.txtvar.get())*1000)), self.execute_command, 0)
                    self.counter(datetime.datetime.now()+datetime.timedelta(seconds=int(float(self.txtvar.get()))))
            
            elif self.but_vat.get() == 0 :
                self.txtvar.set(self.init_var)
                self.execute_command(0)

        except ValueError:
            self.txtvar.set(self.init_var)
            self.execute_command(self.but_vat.get())


    def counter(self,time):
        
        def chop_microseconds(delta):
            return delta - datetime.timedelta(microseconds=delta.microseconds)
            
        remain_time = chop_microseconds(time-datetime.datetime.now())
        
        if remain_time.total_seconds() >0 and self.but_vat.get() == 1: 
            self.txtvar.set(str(remain_time))
            self.after(1000,self.counter,time)
            
        elif remain_time.total_seconds()<=0:
            self.txtvar.set(self.init_var)


    def HWbutton_pressed(self,i,state):
        #i irrelvant
        if not self.task_state == [] : self.disable_sched_task()
        self.execute_command(state)


    def get_state(self):
        return self.HW_output.get_state()



class MainsButton(tk.Frame):

    
    #class HWRemoteOutput:
    ##This Class creates Hardware state of ""gpio_pins"" of RPi at "ip"
        #def __init__(self,master, ip, output_pins):
            #factory = PiGPIOFactory(host=ip)
            #self.master = master
            #self.output_pins= ["Pin_"+str(output_pins[i]) for i in range(len(output_pins))]
            #for sw in range(len(self.output_pins)):
                #self.output_pins[sw] = OutputDevice(output_pins[sw], pin_factory=factory,initial_value=False)
                
            #print("RemoteOutput Init %s, IP:%s, GPIO pins:%s"%(self.master.nick, ip, output_pins))


        ##Make the switch
        #def set_state(self, sw, state):
            #if state == 1:
                #self.output_pins[sw].on()
            #elif state == 0:
                #self.output_pins[sw].off()

        ##Inquiry
        #def get_state(self):
            #stat=[]
            #for sw in range(len(self.output_pins)):
                #stat.append(self.output_pins[sw].value)
            #return stat

    
    #class Indicators:
        
        #def __init__(self,master, frame ):
            #self.master = master
            #self.frame = frame
            #self.t = 2 # Amount of indicators/ switches
            #self.indicators = ['indicator'+str(i) for i in range(self.t)]
            #self.build_gui()
            #self.update_indicators()
            
            
        #def update_indicators(self):
            #for i in range(self.t):
                #if str(self.master.get_state()[i]) == "False":
                    #self.indicators[i].config(bg="red")
                #elif str(self.master.get_state()[i]) == "True":
                    #self.indicators[i].config(bg="green")
            #self.frame.after(500, self.update_indicators)


        #def build_gui(self):
            #ofset=8
            #for i in range(self.t):
                #self.indicators[i] = tk.Label(self.frame, width=1, height=1, text="", bg='blue',relief=tk.SUNKEN)
                #self.indicators[i].grid(row=i, column=0, sticky=tk.NE, pady=ofset, padx=ofset)


    #class HWRemoteInput:
        ##This class create a link between input_pins(HW buttons) to output pins
        #def __init__(self, master, ip, input_pins):
            #self.master = master
            #factory = PiGPIOFactory(host=ip)
            
            #self.input_pins= ["Pin_"+str(input_pins[i]) for i in range(len(input_pins))]
            #for sw in range(len(self.input_pins)):
                #self.input_pins[sw] = gpiozero.Button(input_pins[sw], pin_factory=factory)
                #self.input_pins[sw].when_pressed = lambda arg=sw :self.pressed(arg)

            #print("RemoteInput Init-%s, IP:%s, GPIO pins:%s"%(self.master.nick,ip, input_pins))

        ##Detect press and make switch
        #def pressed(self,i):
            #self.master.switch_type = 'HWButton Switch'
            #self.master.HWbutton_pressed(i,[1,0][self.master.HW_output.get_state()[i]])

        #def get_state(self):
            #stat=[]
            #for sw in range(len(self.input_pins)):
                #stat.append([self.input_pins[sw].value])
            #return stat


    def __init__(self, master, nickname='MainsBut', ip_out='192.168.2.113', hw_out=[4, 27], hw_in=[21,22], ip_in='192.168.2.113', sched_vector=[[[4,5,6],"06:00:40","23:24:10"]], height=3, width=15):
        
        tk.Frame.__init__(self, master)
        self.mainframe = ttk.Frame(self)
        self.master = master
        self.nick = nickname
        self.allow_to_switch = 0

        self.build_buttons(width,height)
        self.switch_type=''
        self.last_exec=''
        self.task_state = [1]*len(sched_vector)

        #Using GIO HW classes
        self.HW_output = HWRemoteOutput(self, ip_out, hw_out)
        Indicators(self.HW_output, self)
        if not hw_in == []: self.HW_input = HWRemoteInput(self, ip_in, hw_in)
        if not sched_vector ==[]:
            #sched_vector = [[1,"22:00:40","23:24:10"]]
            self.SchRun =  ScheduledEvents(tasks=sched_vector)
            self.run_schedule()



    def build_buttons(self, width, height):

        def restore_timeout(event):
            if not self.txtvar.get() == self.init_var:
                try:
                    int(self.txtvar.get())
                except ValueError:
                    self.txtvar.set(self.init_var)


        def clear_timeout(event):
            self.txtvar.set("")


        self.init_var = "TimeOut [min]"

        self.txtvar = tk.StringVar()
        self.txtvar.set(self.init_var)
        timeout_entry = tk.Entry(self, textvariable=self.txtvar, width=12, bg="white", fg='#4c4c4c', justify=tk.CENTER)
        timeout_entry.grid(row=2, column=0, padx=6)
        timeout_entry.bind("<Button-1>", clear_timeout)
        timeout_entry.bind("<FocusOut>", restore_timeout)

        main_but_var = tk.IntVar()
        main_but = tk.Checkbutton(self, text='Main Power', width=10, height=1, indicatoron=0, variable=main_but_var, fg='red', command=self.main_power)
        main_but.grid(row=0, column=0, pady=5)

        tog_but_var = tk.IntVar()
        tog_but = tk.Checkbutton(self, text=self.nick, width=width, height=height, indicatoron=0, variable=tog_but_var, command=self.SFbutton_pressed)
        tog_but.grid(row=1, column=0)

        #label = tk.Label(self, text=self.nick)
        #label.grid(row=3, column=0)

        self.but_stat = [main_but_var, tog_but_var]


    def main_power(self, txt='MainPower'):

        #power off
        if self.but_stat[0].get() == 0:
            self.allow_to_switch = 0
            self.HW_output.set_state(0,0)
            if bool(self.HW_output.get_state()[1]):
                self.execute_command(0,'MainSwitch ShutDown')

        #power on
        elif self.but_stat[0].get() == 1:
            self.allow_to_switch = 1
            self.HW_output.set_state(0,1)

        if self.switch_type == '' : self.switch_type='SFButton'
        print([self.nick, self.switch_type, txt, self.HW_output.get_state()[0]])


    def execute_command(self, state, txt=''):

        #On/Off
        if self.allow_to_switch == 1:
            if state == 1:#Switch on
                if not bool(self.HW_output.get_state()[1]):
                    self.HW_output.set_state(1,1)
                    self.but_stat[1].set(1)
            elif state == 0:#Swotch off
                if bool(self.HW_output.get_state()[1]):
                    self.HW_output.set_state(1,0)
                    self.but_stat[1].set(0)

        #State = Power Disable
        elif self.allow_to_switch == 0:
            if bool(self.HW_output.get_state()[1]): #Toggle button is On
                self.HW_output.set_state(1,0)
                self.but_stat[1].set(0)
            elif not bool(self.HW_output.get_state()[1]):
                self.but_stat[1].set(0)

        print([self.nick, self.switch_type,'ToggleButton', self.HW_output.get_state()[1],txt])


    def run_schedule(self):
        
        self.SchRun.run_schedule()
        sched_status = self.SchRun.get_status()

        #sched_status[0][0] is switch on/off sched_status[0][1] is task number
        #if status equal to On or Off and task state wasn't disabled
        
        if not sched_status[0][0] == -1 and self.task_state[sched_status[0][1]]== 1:
            if not bool(sched_status[0][0]) == self.get_state()[1] :
                self.sched_switch_command(0, sched_status[0][0])
   
        self.master.after(1000, self.run_schedule)


    def sched_switch_command(self,i,state):
        #i irrelvant
        self.switch_type = 'Schedule'
        self.execute_command(state)


    def disable_sched_task(self):
        try: # if there is a schedule
            #if schedule in ON- disable it for next run
            if not self.SchRun.get_status()[0][0] == -1 :
                self.task_state[self.SchRun.get_status()[0][1]] = 0
                                                        #   ^^------toggle button
        except AttributeError:
            pass


    def SFbutton_pressed(self):
                  
        self.switch_type = 'SFButton'
        if not self.task_state==[] : self.disable_sched_task()
       
        #if self.but_stat[1].get() == 1 :  
            #self.execute_command(1)#, 'AutoOff %s minutes'%self.txtvar.get())
            ##self.after(1000, self.execute_command, 0)
            ##self.counter(datetime.datetime.now()+datetime.timedelta(seconds=int(float(self.txtvar.get()))))
            
        #elif self.but_stat[1].get() == 0 :
            ##self.txtvar.set(self.init_var)
            #self.execute_command(0)

        try:
            if float(self.txtvar.get()) >0:
                if self.but_stat[1].get() == 1 :  
                    self.execute_command(1, 'AutoOff %s minutes'%self.txtvar.get())
                    self.after(int(round(float(self.txtvar.get())*1000)), self.execute_command, 0)
                    self.counter(datetime.datetime.now()+datetime.timedelta(seconds=int(float(self.txtvar.get()))))
            
            elif self.but_stat.get() == 0 :
                self.txtvar.set(self.init_var)
                self.execute_command(0)

        except ValueError:
            self.txtvar.set(self.init_var)
            self.execute_command(self.but_stat[1].get())


    def counter(self,time):
        
        def chop_microseconds(delta):
            return delta - datetime.timedelta(microseconds=delta.microseconds)
            
        remain_time = chop_microseconds(time-datetime.datetime.now())
        
        if remain_time.total_seconds() >0 and self.but_stat[1].get() == 1: 
            self.txtvar.set(str(remain_time))
            self.after(1000,self.counter,time)
            
        elif remain_time.total_seconds()<=0:
            self.txtvar.set(self.init_var)


    def HWbutton_pressed(self,sw,state):

        self.switch_type = "HWButton"
        self.but_stat[sw].set(state)
                
        if sw == 0: #MainsPower
            self.main_power('MainPower')
            
        elif sw == 1: #ToggleButton
            self.execute_command(state)

    def get_state(self):
        return self.HW_output.get_state()


root = tk.Tk()
a=MainsButton(root)
a.grid()
root.mainloop()

#root = tk.Tk()
#a=UpDownButton(root,hw_out=[4,27],ip_out='192.168.2.113',nickname="UpDown",hw_in=[21,22],sched_vector=[[[6],"14:34:00","19:54:00"], [[7],"07:00:40","14:33:10"]])
#a.grid()
#root.mainloop()

#root = tk.Tk()
#b = ToggleButton(root, ip_out="192.168.2.113",hw_out=[4], hw_in=[22],sched_vector=[[[6],"14:34:00","19:54:00"], [[7],"07:00:40","14:33:10"]])
#b.grid()
#root.mainloop()

button_list={1:'UpDownButton', 2:'ToggleButton', 3:'MainsButton'}

