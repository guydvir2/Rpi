import datetime
import time
import csv
from sys import platform
from time import sleep
##from gpiozero import Buzzer
##from gpiozero import LED
from tkinter import *
import tkinter.ttk
import os.path
import signal
# import pigpio

# My Modules
import readfile_ssh
import getip
import read_n_write_csv


class SwitchButtons:
    def __init__(self, master, frame, num_of_buttons):
        self.master = master
        self.status = []
        self.buts = []
        self.leds = []
        bg_window = "DeepSkyBlue4"
        frame.config(text="Switch Pannel", font=('Helvetica', 12))
        self.framein = Frame(frame)
        self.framein.grid(padx=5, pady=5)

        ##Create Widgets of buttons
        for i in range(num_of_buttons):
            button_var = StringVar()
            entry_var = IntVar()
            led_var = StringVar()
            t = 35
            ent = Entry(self.framein, textvariable=entry_var, width=4, justify="center")
            ent.grid(column=i, row=2, sticky=W, padx=t)

            led = Label(self.framein, textvariable=led_var, width=4, bg="red", fg="white", relief="ridge")
            led_var.set("off")
            led.grid(row=0, column=i, pady=10)

            c = Checkbutton(self.framein, text="Switch " + str(i), variable=button_var, indicatoron=0,
                            width=10, height=2, onvalue="on", offvalue="off",
                            command=lambda arg=[i, button_var, entry_var]: self.cb(arg))
            c.grid(column=i, padx=30, pady=5, row=1)
            button_var.set("off")

            mins = Label(self.framein, text="min.", width=4, justify="center", fg="black")  # ,bg=bg_window)
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

        ##Update in accordance with Master
        self.master.loop.device_chage_state(but[0], but[1].get(), text=a)
        # print("Switch %d is %s" % (but[0], but[1].get()))

        ##

    def cb_delayed(self, but):
        self.framein.after(but[2].get() * 1000, self.cb, but, "off")


class schedule_GUI():
    def __init__(self, master, tab_frame, ip, num_switches):

        self.master = master
        self.num_switches = num_switches
        self.file_handler = read_n_write_csv.sched_file(ip)
        self.sch_file = self.file_handler.sch_file
        self.tasks_total = self.file_handler.tasks_total
        self.continue_task = self.file_handler.continue_task
        #self.master.uptime("12312312", "192.168.2.113")
        print(master.__str__)

        style_ent = tkinter.ttk.Style()
        style_ent.configure('G.TEntry', foreground="blue", background=[("active", "black"), ("disabled", "red")],
                            font=("Helvetica", 20))

        style_frame = tkinter.ttk.Style()
        style_frame.configure('TLabelFrame', background=[("active", "black"),
                                                         ("disabled", "red")], font=("Helvetica", 12))

        sched_frame = tkinter.ttk.LabelFrame(tab_frame, text="Weekly Schedule")
        sched_frame.grid(row=0, column=0, pady=20, padx=20, ipadx=20, columnspan=1)
        dropdown_vals = [[], ["on", "off"], [], [], [], [num for num in range(num_switches)], [], []]
        self.headers = ["Task#", "On/off", "Days", "Start", "End", "Switch", "Next On/Off"]
        cell_w = [5, 5, 12, 12, 12, 5, 12]

        # Create Table with initial Values
        self.row_vars = []
        self.ents = []
        for i in range(self.tasks_total):
            var1, var2, var3, var4, var5, var6, var7 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
            self.row_vars.append([var1, var2, var3, var4, var5, var6, var7])
            temp = []

            # Create Columns With Headers
            for t in range(len(self.headers)):
                l = tkinter.ttk.Label(sched_frame, text=self.headers[t], width=cell_w[t],
                                      anchor=CENTER)
                l.grid(row=0, column=t)

                if t == 1 or t == 5:
                    onoff_comb = tkinter.ttk.Combobox(sched_frame, width=cell_w[t],
                                                      textvariable=self.row_vars[i][t], values=dropdown_vals[t],
                                                      justify=CENTER)
                    onoff_comb.grid(row=i + 1, column=t)
                    temp.append(onoff_comb)

                else:
                    task_ent = Entry(sched_frame, width=cell_w[t],
                                     textvariable=self.row_vars[i][t], justify=CENTER, bg='white')  # ,style='G.TEntry'
                    task_ent.grid(row=i + 1, column=t)
                    temp.append(task_ent)

                if t < len(self.headers) - 1:
                    self.row_vars[i][t].set(self.sch_file[i + 1][t])
                else:
                    self.row_vars[i][t].set("Wait for Task")  ## Column 7

            self.ents.append(temp)
        ###

        ## Create SAVE Button
        save_button = tkinter.ttk.Button(sched_frame, text="Update", command=self.save_cb)  # self.save_csv)
        save_button.grid(row=i + 2, column=t, pady=5)
        ##

        ## Create Manual Buttons
        manualbut_frame = LabelFrame(tab_frame, text="Manual Buttons")
        manualbut_frame.grid(row=1, column=0, padx=0)
        self.switch_button = SwitchButtons(self, manualbut_frame, num_switches)
        ##

        ## Create Main Buttons
        mainbut_frame = tkinter.ttk.LabelFrame(tab_frame, text="Main Buttons")
        mainbut_frame.grid(row=0, column=1, padx=10)

        self.exit_button = Button(mainbut_frame, text="Exit", command=root.quit)
        self.exit_button.grid(row=0, column=0, pady=5, padx=5, sticky=W + E, columnspan=2)

        ##Create MainSW
        self.mainsw_txt = StringVar()
        self.mainsw_state = StringVar()
        self.mainswitch = Checkbutton(mainbut_frame, textvariable=self.mainsw_txt,
                                      variable=self.mainsw_state, indicatoron=0, height=2, width=20, onvalue="on",
                                      offvalue="off", command=self.mainsw)
        self.mainswitch.grid(row=1, column=0, pady=5, padx=5, columnspan=2)
        self.mainsw_state.set("on")
        self.mainsw("on")
        ###

        ## Run Schedualer
        self.loop = run_schedule(self)

    ## CallBack Press Save&Update
    def save_cb(self):
        self.file_handler.save_csv(self)

    ##Control MainSwitch
    def mainsw(self, stat=[]):
        # if self.loop.device_chage_state=="on":                           #for code switch
        # self.mainsw_state.set("on")
        # elif stat=="off":
        # self.mainsw_state.set("off")

        if self.mainsw_state.get() == "on":  # execute when on
            self.mainsw_txt.set("MainSwitch ON")
            self.mainswitch.config(background="red", fg='#4c4c4c')
            for n in range(self.num_switches):
                self.switch_button.buts[n].config(state="normal")

        if self.mainsw_state.get() == "off":  # execute when off
            self.mainsw_txt.set("MainSwitch OFF")
            self.mainswitch.config(background="red", fg="white")
            for n in range(self.num_switches):
                self.loop.device_chage_state(n, "off")
                self.switch_button.buts[n].config(state="disabled")

    ##Update Entries & Dropdown of Schedule
    def update(self, r, c, text, bg1='white', fg1='black'):
        self.row_vars[r][c].set(text)
        self.ents[r][c].config(fg=fg1, bg=bg1)
        ###


##class rpi_relay(pigpio.pi):
##
##    def __init__(self,ip_addr,gpio=[4,5,6,12]):
##        pigpio.pi.__init__(self)
##        self.GPIO=gpio
##        self.rpi=pigpio.pi(ip_addr)
##        for t in range(len(self.GPIO)):
##            self.rpi.write(self.GPIO[t],0)
##
##    def switch_state(self,i,state):
##        self.rpi.write(self.GPIO[i],state)
##
##    def read_state(self,i):
##        self.rpi.write(self.GPIO[i],state)


class run_schedule():
    def __init__(self, master):
        self.master = master
        self.switches_flag = []
        for t in range(master.num_switches):
            self.switches_flag.append(['off' for y in range(master.num_switches)])

        ##Switch Off at init
        for n in range(master.num_switches):
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
        t_left = 0
        t_left = round(t)
        return ["%02d:%02d:%02d" % (h, m, s), (t_left)]

    def device_chage_state(self, dev, stat, task="", text=""):
        task1 = ""

        # print(dev,stat,task)

        ##Switch Functions
        def switch(stat):
            self.switches_flag[dev] = stat
            if stat == "on":
                color = "green"
                # rpi_1.switch_state(dev, 1)
            elif stat == "off":
                color = "red"
                # rpi_1.switch_state(dev, 0)

            ##Item to EXECUTE on switch 
            self.master.switch_button.status[dev][1].set(stat)
            self.master.switch_button.leds[dev].config(bg=color)

        ###

        # Mainswtich is ON and Switch stat changes due schedule
        # print(dev)
        if stat != self.switches_flag[dev] and self.master.mainsw_state.get() == "on":
            switch(stat)

            # Switch from Sched_loop
            if task != "" and self.master.switch_button.status[dev][0].get() == "off":
                task1 = "task#" + str(int(task))

            ##Swtich caused by sofware button
            if task == "":
                task1 = "Manual Switch"
                if text != "0": task1 = task1 + text

            print("[%s] Switch%s, %s, %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                             str(dev), stat, task1))
        ###

        # Shutdown process due to MainSw OFF
        if self.switches_flag[dev] == "on" and self.master.mainsw_state.get() == "off":
            task1 = "MainSwitch Shutdown"
            switch("off")
            self.master.switch_button.status[dev][0].set("off")
            print("[%s] %s, %s, %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                       str(dev), stat, task1))
            ###

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

                ##Stop Ending task or MainSwitch Shutdown
                if isin_start[1] < 0 and isin_stop[1] <= 0 and isin_stop[
                    1] >= -2 * tol or self.master.mainsw_state.get() == "off":
                    print(i, "stop")
                    self.device_chage_state(int(self.master.sch_file[i][5]), "off", self.master.sch_file[i][0])
                    label_def_onoff(i)
                    self.master.continue_task[i - 1] = 'off'
        root.after(int(2 * tol * 1000), self.loop)


class MainApp:
    def __init__(self, master, pis, tab_names=[]):
        # Frame.__init__(self,master)
        start_time = datetime.datetime.now()
        ip = getip.get_ip()

        note = tkinter.ttk.Notebook(master)
        guis = ['gui' + str(i) for i in range(len(pis))]
        tabs = ['tab' + str(i) for i in range(len(pis) + 1)]

        if tab_names == [] or len(tab_names) < 3:
            tab_names = pis + ['Activity log']
        else:
            tab_names.append('Activity log')

        for i in range(len(pis) + 1):
            tabs[i] = tkinter.ttk.Frame(note)
            note.add(tabs[i], text=tab_names[i])
            note.grid()
            if i == len(pis):
                self.text_tab = Text(tabs[i], width=100, height=26)
                self.text_tab.grid(row=0, column=0)
                scrollbar = Scrollbar(tabs[i])
                scrollbar.grid(row=0, column=1)  # , sticky = W + E +N + S)
                scrollbar.config(command=self.text_tab.yview)
                self.text_tab.config(yscrollcommand=scrollbar.set)
            else:
                guis[i] = schedule_GUI(self, tabs[i], pis[i], num_switches[i])

##        self.write2log("Initialize: " + str(start_time))
##        self.write2log("Local IP: " + str(ip[0]))

        self.statusbar_label = Label(master)
        self.statusbar_label.grid()
        self.update_statusbar(start_time, ip)
        # readfile_ssh.run_process('pigpiod')
        # rpi_1=rpi_relay(pis[0])
        # rpi_2=rpi_relay(pis[1])
        # readfile_ssh.copyfile(pis[1],'/home/guy/PythonProjects/','schedule')

    def update_statusbar(self, start_time, ip):

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
        root.after(500, self.update_statusbar, start_time, ip)  # run itself again after 1000 ms

    def write2log (self):
        print("guy")
        #print(self.status_label)
        #self.text_tab.insert(END,text1+"\n")








############################################

root = Tk()
root.title("Advanced Schedualer")
pis = ['192.168.2.112', '192.168.2.113', '192.168.2.114']
pi_names = ['RaspBerryPi 1', 'RaspBerryPi 2', 'RaspBerryPi 3']
num_switches = [4, 4, 4]
App = MainApp(root, pis, pi_names)
root.mainloop()
