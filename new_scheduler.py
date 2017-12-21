import datetime
import time
import csv
from sys import platform
from time import sleep
from tkinter import *
import tkinter.ttk
import os.path
import signal
import pigpio
import subprocess

# My Modules
import readfile_ssh
import getip
import password_window
#import RemoteRelSwitch


class sched_file:
    def __init__(self, master, ip, filename, path,local_ip):
        self.master = master
        self.filename = path + filename + '_' + (ip) + '.csv'
        self.loc_fname = path + filename + '.csv'
        self.ip = ip
        self.local_ip= local_ip
        self.load_csv()


    def save_csv(self, mat, exists=''):  # save sched table to CSV file

        if exists != 'new':
            non_empty_cells = 0
            for v in range(self.master.gui_rows):
                if self.master.row_vars[v][0].get() != "":
                    non_empty_cells += 1
                else:
                    break

            mat = []

            for r in range(non_empty_cells):
                newrow = []
                for c in range(len(self.master.headers) - 1):
                    if c == 0:
                        newrow.append(r)
                    else:
                        newrow.append(self.master.row_vars[r][c].get())
                mat.append(newrow)
            mat.insert(0, self.master.headers)
        else:
            pass

        outputfile = open(self.filename, 'w', newline="")
        outputwriter = csv.writer(outputfile)
        outputwriter.writerows(mat)
        outputfile.close()
        self.master.master.write2log("%s [saved OK]" % self.filename)

        self.reload1(mat)


    def reload1(self, mat):
        self.load_csv()
        self.master.tasks_total = self.tasks_total
        self.master.sch_file = mat
        self.master.continue_task = self.continue_task


    def load_csv(self):

        def read_csv(file_in):
            # check file exist
            if os.path.isfile(file_in) == True:
                with open(file_in, 'r') as f:
                    reader = csv.reader(f)
                    your_list = list(reader)
                    self.sch_file = your_list
            else:
                self.master.master.write2log(self.filename + " [does not exist]")

                mat = []
                mat.append(self.master.headers)
                mat.append(["1", "on", [6], "23:07:00", "01:08:00", "1"])
                self.tasks_total = 1
                self.save_csv(mat, 'new')
                read_csv(self.filename)

        if self.ip == self.local_ip:
            subprocess.run('cp %s %s'%(self.loc_fname,self.filename),shell=True)

        read_csv(self.filename)
        self.tasks_total = (len(self.sch_file)) - 1
        self.continue_task = ['on' for y in range(self.tasks_total)]
        self.master.master.write2log("%s [loaded OK]" % self.filename)


class SwitchButtons:
    def __init__(self, master, frame, num_of_buttons):
        self.master = master
        self.status = []
        self.buts = []
        self.leds = []
        bg_window = "DeepSkyBlue4"
        self.framein = Frame(frame)
        self.framein.grid(padx=5, pady=5)

        #Create Widgets of buttons
        for i in range(num_of_buttons):
            button_var = StringVar()
            entry_var = IntVar()
            led_var = StringVar()
            t = 35
            ent = Entry(self.framein, textvariable=entry_var, width=4, justify="center")
            ent.grid(column=i, row=2, sticky=W, padx=t)

            led = Label(self.framein, textvariable=led_var, width=4, bg="red", fg="white", relief="ridge")
            led_var.set("off")
            led.grid(row=0, column=i, pady=0)

            c = Checkbutton(self.framein, text="Switch " + str(i), variable=button_var, indicatoron=0,
                            width=10, height=2, onvalue="on", offvalue="off",
                            command=lambda arg=[i, button_var, entry_var]: self.cb(arg))
            c.grid(column=i, padx=30, pady=5, row=1)
            button_var.set("off")

            mins = Label(self.framein, text="min.", width=4, justify="center", fg="black")
            mins.grid(column=i, row=2, sticky=E, padx=t)

            self.status.append([button_var, led_var, entry_var])
            self.buts.append(c)
            self.leds.append(led)
            ###

    def cb(self, but, state='', a=''):
        # but = [ switch#, switch state, delay] ## explanatory

        ##In use only in CB_DELAYED
        if state != '':
            but[1].set(state)

        def switch_onoff():
            if but[1].get() == "on":
                self.leds[but[0]].config(bg="green")
                self.status[but[0]][1].set("on")
            elif but[1].get() == "off":
                self.leds[but[0]].config(bg="red")
                self.status[but[0]][1].set("off")

        if but[2].get() > 0 and but[1].get() == "on":
            a = ", Auto shutdown in %s minutes." % (but[2].get())
            switch_onoff()
            print("Delayed", but[1].get())
            self.cb_delayed(but)
        else:
            switch_onoff()

        self.master.loop.device_chage_state(but[0], but[1].get(), text=a)

    def cb_delayed(self, but):
        self.framein.after(but[2].get() * 1000, self.cb, but, "off")


class schedule_GUI():
    def __init__(self, master, tab_frame, ip, num_switches, filename, path, local_ip):
        self.ip = ip
        self.master = master
        self.num_switches = num_switches
        self.headers = ["Task#", "On/off", "Days", "Start", "End", "Switch", "Next On/Off"]
        self.load_sched_file(ip, filename, path, local_ip)
        self.build_table_gui(tab_frame, num_switches)
        self.create_buttons_gui()

        ## Run Schedualer
        self.loop = run_schedule(self)


    def build_table_gui(self, tab_frame, num_switches):
        style_ent = tkinter.ttk.Style()
        style_ent.configure('G.TEntry', foreground="blue", background=[("active", "black"), ("disabled", "red")],font=("Helvetica", 20))

        style_frame = tkinter.ttk.Style()
        style_frame.configure('TLabelFrame', background=[("active", "black"), ("disabled", "red")],
                              font=("Helvetica", 12))

        # Schedule LabelFrame
        sched_LabelFrame = tkinter.ttk.LabelFrame(tab_frame, text="Weekly Schedule")
        sched_LabelFrame.grid(row=0, column=0, sticky=NW, pady=20, padx=10)

        sched_frame = tkinter.ttk.Frame(sched_LabelFrame)
        sched_frame.grid(row=0, column=0, padx=15)
        dropdown_vals = [[], ["on", "off"], [], [], [], [num for num in range(num_switches)], [], []]
        cell_w = [8, 8, 15, 15, 15, 8, 15]

        # Create Table with initial Values
        self.row_vars = []
        self.ents = []

        self.gui_rows = self.tasks_total + 1

        for i in range(self.gui_rows):
            var1, var2, var3, var4, var5, var6, var7 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
            self.row_vars.append([var1, var2, var3, var4, var5, var6, var7])

            temp = []

            # Create Columns With Headers
            for t in range(len(self.headers)):
                l = tkinter.ttk.Label(sched_frame, text=self.headers[t], width=cell_w[t], anchor=CENTER)
                l.grid(row=0, column=t)

                if t == 1 or t == 5:
                    onoff_comb = tkinter.ttk.Combobox(sched_frame, width=cell_w[t], textvariable=self.row_vars[i][t], values=dropdown_vals[t], justify=CENTER)
                    onoff_comb.grid(row=i + 1, column=t)
                    temp.append(onoff_comb)

                else:
                    task_ent = Entry(sched_frame, width=cell_w[t], textvariable=self.row_vars[i][t], justify=CENTER,bg='white')
                    task_ent.grid(row=i + 1, column=t)
                    temp.append(task_ent)

                if t < len(self.headers) - 1 and i < self.tasks_total:
                    self.row_vars[i][t].set(self.sch_file[i + 1][t])
                elif t == len(self.headers) - 1 and i < self.tasks_total:
                    self.row_vars[i][t].set("Wait for Task")  ## Column 7

            self.ents.append(temp)
        ###
    def create_buttons_gui(self):
        ## Create update Button
        save_button = tkinter.ttk.Button(sched_frame, text="Update", command=self.save_cb)
        save_button.grid(row=i + 2, column=t, pady=5)
        ##

        ## Create Manual Buttons
        manualbut_frame = tkinter.ttk.LabelFrame(tab_frame, text="Manual Buttons")
        manualbut_frame.grid(row=1, column=0, padx=10, sticky=W + E)
        self.switch_button = SwitchButtons(self, manualbut_frame, num_switches)
        ##

        ## Create Main Buttons
        mainbut_frame = tkinter.ttk.LabelFrame(tab_frame, text="Main Buttons")
        mainbut_frame.grid(row=0, column=1, pady=20, sticky=N, padx=10)

        self.exit_button = Button(mainbut_frame, text="Exit", command=root.quit)
        self.exit_button.grid(row=0, column=0, pady=5, padx=10, sticky=W + E, columnspan=2)

        ##Create MainSW
        self.mainsw_txt = StringVar()
        self.mainsw_state = StringVar()
        self.mainswitch = Checkbutton(mainbut_frame, textvariable=self.mainsw_txt, variable=self.mainsw_state,indicatoron=0, height=2, width=15, onvalue="on", offvalue="off",command=self.mainsw)
        self.mainswitch.grid(row=1, column=0, pady=5, padx=10, columnspan=2)
        self.mainsw_state.set("on")
        self.mainsw("on")
        ###
        
    def load_sched_file(self,ip, filename, path, local_ip):
        self.file_handler = sched_file(self, self.ip, filename, path, local_ip)
        self.sch_file = self.file_handler.sch_file
        self.tasks_total = self.file_handler.tasks_total
        self.continue_task = self.file_handler.continue_task


    ## CallBack Press Save&Update
    def save_cb(self):
        self.file_handler.save_csv(self.row_vars)

    ##Control MainSwitch
    def mainsw(self, stat=[]):

        # if self.loop.device_chage_state=="on":                           #for code switch
        # self.mainsw_state.set("on")
        # elif stat=="off":
        # self.mainsw_state.set("off")

        if self.mainsw_state.get() == "on":  # execute when on
            self.mainsw_txt.set("MainSwitch ON")
            self.mainswitch.config(background="red", fg='#4c4c4c')
            self.master.write2log("[" + self.ip + "]" + "[MainSwitch ON]")
            for n in range(self.num_switches):
                self.switch_button.buts[n].config(state="normal")

        if self.mainsw_state.get() == "off":  # execute when off
            self.mainsw_txt.set("MainSwitch OFF")
            self.mainswitch.config(background="red", fg="white")
            self.master.write2log("[" + self.ip + "]" + "[MainSwitch OFF]")
            for n in range(self.num_switches):
                self.loop.device_chage_state(n, "off")
                self.switch_button.buts[n].config(state="disabled")

    ##Update Entries & Dropdown of Schedule
    def update(self, r, c, text, bg1='white', fg1='black'):
        self.row_vars[r][c].set(text)
        self.ents[r][c].config(fg=fg1, bg=bg1)
        ###


#class rpi_relay(pigpio.pi):

    #def __init__(self,ip_addr,gpio=[4,22,6,26]):
        #pigpio.pi.__init__(self)
        #self.GPIO=gpio
        #self.rpi=pigpio.pi(ip_addr)
        #for t in range(len(self.GPIO)):
            #self.rpi.write(self.GPIO[t],0)

    #def switch_state(self,i,state):
        #self.rpi.write(self.GPIO[i],state)

    #def read_state(self,i):
        #self.rpi.write(self.GPIO[i],state)


class run_schedule():
    def __init__(self, master):
        self.master = master
        self.switches_flag = []
        # self.switches_flag = ['off' for y in range(master.num_switches)]

        ##Switch Off at init
        for n in range(master.num_switches):
            self.switches_flag.append("off")
            self.device_chage_state(n, "off")

        ## Start Main Schedule function
        self.loop()

    def time_diff(self, t1):
        t2 = datetime.datetime.now().time()
        today = datetime.date.today()
        return datetime.datetime.combine(today, t1) - datetime.datetime.combine(today, t2)

    ##Sched Loop _ Check if inside time interval
    def is_in(self, target, low_tol, high_tol, i):
        t = self.time_diff(datetime.datetime.strptime(target, "%H:%M:%S").time()).total_seconds()
        h = (int(abs(t) / 3600))
        m = (int((abs(t) - h * 3600) / 60))
        s = (abs(t) - h * 3600 - m * 60)
        return ["%02d:%02d:%02d" % (h, m, s), (round(t))]

    def device_chage_state(self, dev, stat, task="", text=""):
        task1 = ""

        # print(dev,stat,task)

        ##Switch Functions
        def switch(stat):
            self.switches_flag[dev] = stat
            if stat == "on":
                color = "green"
                #rpi_1.switch_state(dev, 1)
            elif stat == "off":
                color = "red"
                #rpi_1.switch_state(dev, 0)

            ##Item to EXECUTE on switch 
            self.master.switch_button.status[dev][1].set(stat)
            self.master.switch_button.leds[dev].config(bg=color)

        ###

        # Mainswtich is ON and Switch stat changes due schedule
        if stat != self.switches_flag[dev] and self.master.mainsw_state.get() == "on":
            switch(stat)

            # Switch from Sched_loop
            if task != "" and self.master.switch_button.status[dev][0].get() == "off":
                task1 = "task#" + str(int(task))

            ##Swtich caused by GUI button
            if task == "":
                task1 = "Manual Switch"
                if text != "0": task1 = task1 + text
            txt1 = "[%s] [Switch %s] [%03s] %s" % (str(self.master.ip), str(dev), str(stat), str(task1))
            self.master.master.write2log(txt1)

        ###

        # Shutdown process due to MainSw OFF
        if self.switches_flag[dev] == "on" and self.master.mainsw_state.get() == "off":
            task1 = "MainSwitch Shutdown"
            switch("off")
            self.master.switch_button.status[dev][0].set("off")
            txt1 = "[%s] [Switch %s] [%03s] %s" % (str(self.master.ip), str(dev), str(stat), str(task1))
            self.master.master.write2log(txt1)

    ## Schedualer Engine
    def loop(self):

        days = [2, 3, 4, 5, 6, 7, 1]
        tol = 0.4

        def label_def_onoff(r):
            self.master.update(r - 1, 6, "Wait for Task", 'white', '#4c4c4c')

        now = datetime.datetime.now().time()  ##update  loop time
        today = datetime.datetime.now().weekday()  ##get day of week
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  ##time stamp str f

        for i in range(1, self.master.tasks_total + 1):  # is task off ?
            if self.master.sch_file[i][1] == "off":
                label_def_onoff(i)

            if str(days[today]) in self.master.sch_file[i][2] and "on" in self.master.sch_file[i][
                1]:  # day of week & task enable
                isin_start = self.is_in(self.master.sch_file[i][3], -tol, tol, i)
                isin_stop = (self.is_in(self.master.sch_file[i][4], -tol, tol, i))

                if isin_start[1] > 0:
                    # print(i,"wait")                                           ##wait to ON
                    self.master.update(i - 1, 6, "Off (%s)" % str(isin_start[0]), "white", "red")
                    self.master.continue_task[i - 1] = 'on'

                if isin_stop[1] > 0 and isin_start[1] < 0:  ## inside On interval
                    # print(i,"run")
                    if self.master.switch_button.status[int(self.master.sch_file[i][5])][0].get() == "on" or \
                                    self.master.continue_task[i - 1] == 'off':
                        label_def_onoff(i)
                        self.master.continue_task[i - 1] = 'off'
                    if self.master.switch_button.status[int(self.master.sch_file[i][5])][0].get() == "off" and \
                                    self.master.continue_task[i - 1] != "off":
                        self.master.update(i - 1, 6, "On (%s)" % str(isin_stop[0]), "white", "green")
                        self.device_chage_state(int(self.master.sch_file[i][5]), "on", self.master.sch_file[i][0])
                        self.master.continue_task[i - 1] = 'on'

                #Stop Ending task or MainSwitch Shutdown
                if isin_start[1] < 0 and isin_stop[1] <= 0 and isin_stop[
                    1] >= -2 * tol or self.master.mainsw_state.get() == "off":
                    print(i, "stop")
                    self.device_chage_state(int(self.master.sch_file[i][5]), "off", self.master.sch_file[i][0])
                    label_def_onoff(i)
                    self.master.continue_task[i - 1] = 'off'
        root.after(int(2 * tol * 1000), self.loop)


class MainApp:
    
    def __init__(self, master, pis, tab_names=[]):
        self.master = master
        ip = getip.get_ip()
        self.logger=[]
        self.constants()
        self.file_and_daemon_up(ip[0], pis)
        #self.build_gui(master, pis, tab_names)


    def constants(self):
        def platf():
            if platform == 'linux':
                path = "/home/guy/PythonProjects/"
            elif platform == 'darwin':
                path = "/home/guy/PythonProjects/"
            elif platform == 'win32':
                path = "d:\\PythonProjects\\"
            return path
            
        self.path = platf()
        self.filename = 'schedule'
        self.pwd = 'kupelu9e'
        self.SW_Name = "Advanced Schedualer"


    def file_and_daemon_up(self, local_ip, pis):
        
        #Ping desired Rpis, Load pigpiod, and SSH copy schedule from remote RPis
        self.connected_pis=[]
        local_indx=''
        self.logger.append("RPis set to connect :"+str(pis))
        
        # Check if Running Master is one of RPi's
        if local_ip in pis:
            local_indx = pis.index(local_ip)
            
        for i in range(len(pis)):
            self.pig_res=''
            #self.logger.append("checking RPi#%d - %s"%(i,pis[i]))
            exists_ip = subprocess.Popen('ping %s -c3'%pis[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = exists_ip.communicate()
            #ping OK ?
            if exists_ip.returncode == 0:
                self.logger.append('RPi#%d - %s ping OK'%(i, pis[i]))
                if i == local_indx: #Local machine
                    self.logger.append('RPi#%d - %s - is local/Master machine'%(i, pis[i]))
                    #Load pigpiod
                    readfile_ssh.PigpiodManager(self, pis[i], local_ip, self.pwd)                
                    
                else: #Remote Machine
                    self.logger.append('RPi#%d - %s - is Remote machine'%(i, pis[i]))
                    readfile_ssh.PigpiodManager(self, pis[i], local_ip, self.pwd)
                    #Copy file from remote
                    readfile_ssh.SSHfile(pis[i], self.path, self.filename,'guy',self.pwd)
                    
                if self.pig_res == 0:
                    self.logger.append('RPi#%d - %s pigpiod loaded'%(i, pis[i]))
                    self.connected_pis.append(i)
                else:
                    self.logger.append('RPi#%d - %s pigpiod failed'%(i, pis[i]))
        
            else:
                self.logger.append('RPi#%d - %s ping failed'%(i, pis[i]))



    def build_gui (self, master, pis, tab_names=[]):
        
        def update_statusbar(start_time, ip):

            def uptime(start):
                now = datetime.datetime.now()
                del_time = now - start
                hours = int(del_time.seconds / 3600)
                minutes = int((del_time.seconds - hours * 3600) / 60)
                seconds = del_time.seconds - hours * 3600 - minutes * 60
                return str('%d days, %02d:%02d:%02d' % (del_time.days, hours, minutes, seconds))

            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.statusbar_label.config(
                text=time + " Uptime: " + uptime(start_time) + " Local IP:%s , External IP:%s" % (ip))
            root.after(500, update_statusbar, start_time, ip)  # run itself again after 1000 ms

        ip = getip.get_ip()
        start_time = datetime.datetime.now()
        tabs_connected=[]

        #Create Tabs
        guis = ['gui' + str(i) for i in range(len(self.connected_pis))]
        tabs = ['tab' + str(i) for i in range(len(self.connected_pis) + 1)]

        if tab_names == [] or len(tab_names) < len (self.connected_pis):
            tab_names=['' for i in range (len(pis))]

        for i in range(len(self.connected_pis)):
            tabs_connected.append(tab_names[self.connected_pis[i]]+'-'+ str(pis[self.connected_pis[i]]))
        tabs_connected.append('Activity log')


        #Create Notes for Tabs
        note = tkinter.ttk.Notebook(master)
        for i in range(len(self.connected_pis) + 1):
            tabs[i] = tkinter.ttk.Frame(note)
            note.add(tabs[i], text=tabs_connected[i])
        note.grid(sticky=E + W + N + S)

        #Create log Tab
        self.text_tab = Text(tabs[-1], width=105, height=26)
        self.text_tab.grid(row=0, column=0, sticky= E+W)
        scrollbar = Scrollbar(tabs[-1])
        scrollbar.grid(row=0, column=1, sticky=N + S)
        scrollbar.config(command=self.text_tab.yview)
        self.text_tab.config(yscrollcommand=scrollbar.set)

        log_button = tkinter.ttk.Button(tabs[-1], text="Save log", command=self.save_log)
        log_button.grid(row=1, column=0, sticky=E, pady=10)

        for i in range(len(self.connected_pis)):
            guis[i] = schedule_GUI(self, tabs[i], pis[self.connected_pis[i]], num_switches[i], self.filename, self.path,ip[0])

        #self.write2log("Network Check:", "0.0")
        for m in range (len(self.logger)):
            self.write2log(str(self.logger[m]))
        #self.path = (guis[1].file_handler.platf())
        self.write2log("Initialize MainApp")
        self.write2log("Local IP: " + str(ip[0]))

        self.statusbar_label = Label(master)
        self.statusbar_label.grid()
        update_statusbar(start_time, ip)


    def write2log(self, text1, start=''):
        time2log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if start == "":
            start = END
        self.text_tab.insert(start, "[" + str(time2log) + "] " + text1 + "\n")


    def save_log(self):
        input1 = self.text_tab.get("1.0", 'end-1c')
        text_file = open(self.path + "Schduler.log", "w")
        text_file.write(input1)
        text_file.close()


############################################

root = Tk()
#root.title("Advanced Schedualer")
root.resizable(width = False, height = FALSE)
pis = ['192.168.2.114', '192.168.2.113', '192.168.2.112']
pi_names = ['RaspBerryPi 1', 'RaspBerryPi 2', 'RaspBerryPi 3']
#pi_names=[]
num_switches = [4, 4, 4]
App = MainApp(root, pis, pi_names)
root.mainloop()
