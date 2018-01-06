import os
import tkinter as tk
from tkinter import ttk
import datetime
import socket
import time

from random import randint


class MainApp(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=0, column=0)
        master.title("Where's my Internet ?")

        self.but_frame = ttk.LabelFrame(self, text="Select:", padding=5)
        self.but_frame.grid(row=0, column=1, sticky=tk.E + tk.W + tk.S, padx=5)
        self.statistics_frame = ttk.LabelFrame(self, text="Connection OverView", padding=5)
        self.statistics_frame.grid(row=1, column=0, columnspan=2, sticky=tk.E + tk.W + tk.N, padx=5, pady=5)

        self.txtvar, self.ping_counter_var = tk.StringVar(), tk.StringVar()
        self.status_label_var, self.butvar = tk.StringVar(), tk.StringVar()
        self.max_con_label_var, self.max_discon_label_var = tk.StringVar(), tk.StringVar()
        self.cur_con_var = tk.StringVar()
        self.reset_parameters()

        self.local_ip = socket.gethostbyname(socket.gethostname())

        self.build_gui()
        self.update_ping_counter()
        self.get_time()  ### Runs Clock
        self.update_log('App Start')

    def reset_parameters(self):
        self.ping_counter_good, self.ping_counter_bad = 0, 0
        self.time_good, self.time_bad = datetime.timedelta(0), datetime.timedelta(0)
        self.add_elapsed_time = datetime.timedelta(0)
        self.time_good_current, self.time_bad_current = 0, 0
        self.state, self.elapsed_time = 0, '0'
        self.max_times = [datetime.timedelta(0)] * 2
        self.last_ping = -1
        self.add_time_good, self.add_time_bad = datetime.timedelta(0), datetime.timedelta(0)

    def build_gui(self):
        style = ttk.Style()
        style.theme_use('clam')
        label1 = ttk.Label(self.frame1, text="Ping destination IP/URL:")
        label1.grid(row=0, column=0, sticky=tk.W, padx=5)

        comb_vals = ['www.google.com', 'www.yahoo.com', '127.0.0.1']
        ip_combo = ttk.Combobox(self.frame1, textvariable=self.txtvar, width=18, values=comb_vals)
        ip_combo.grid(row=0, column=1, pady=5)  # , sticky=tk.E)
        ip_combo.current(0)
        ip_combo.bind('<Return>', self.ping)
        ip_combo.bind('<Return>', self.ping)

        self.butvar.set("Start")
        button1 = ttk.Button(self.but_frame, textvariable=self.butvar, command=lambda arg='<>': self.ping(arg))
        button1.grid(row=0, column=0, sticky=tk.W + tk.E, columnspan=2, padx=5)

        self.save_but = ttk.Button(self.but_frame, text="Save")
        self.save_but.grid(row=2, column=0, padx=5)

        self.clear_but = ttk.Button(self.but_frame, text="Reset", command=self.reset_callback)
        self.clear_but.grid(row=2, column=1, padx=5)

        self.exit_button = ttk.Button(self.but_frame, text="Quit", command=root.destroy)
        self.exit_button.grid(row=1, column=0, columnspan=2, sticky=tk.E + tk.W, padx=5, pady=5)

        self.textbox1 = tk.Text(self.frame1, height=10, font=(ip_combo.cget('font'), 8), width=45)
        self.textbox1.grid(row=1, column=0, columnspan=2, padx=5)

        self.status_label = ttk.Label(self, textvariable=self.status_label_var, relief=tk.FLAT, anchor=tk.CENTER,
                                      justify=tk.CENTER)
        self.status_label.grid(row=5, column=0, columnspan=5, sticky=tk.W + tk.E, padx=5)

        self.ping_count_label = ttk.Label(self.statistics_frame, textvariable=self.ping_counter_var, justify=tk.LEFT)
        self.ping_count_label.grid(row=3, column=0, columnspan=3, sticky=tk.E + tk.W)
        self.update_ping_counter()

        ttk.Label(self.statistics_frame, text="Current state. time: ").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.statistics_frame, text="Max Conn. time: ").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self.statistics_frame, text="Max DisConn. time: ").grid(row=2, column=0, sticky=tk.W)

        self.cur_con_label = ttk.Label(self.statistics_frame, textvariable=self.cur_con_var)
        self.cur_con_label.grid(row=0, column=1, sticky=tk.W)
        self.max_con_label = ttk.Label(self.statistics_frame, textvariable=self.max_con_label_var)
        self.max_con_label.grid(row=1, column=1, sticky=tk.W)
        self.max_discon_label = ttk.Label(self.statistics_frame, textvariable=self.max_discon_label_var)
        self.max_discon_label.grid(row=2, column=1, sticky=tk.W)

    def get_time(self):
        clock = datetime.datetime.now()
        if self.state == 1:
            self.elapsed_time = str(clock - self.now + self.add_elapsed_time).split('.')[0]
        self.status_label_var.set(
            str(clock).split('.')[0] + ", Elapsed: " + self.elapsed_time + ', Local IP: ' + str(self.local_ip))

        self.after(1000, self.get_time)

    def update_log(self, input):
        self.textbox1.insert(tk.END, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + input + '\n')

    def ping(self, event, address=''):

        def recur():
            ping_result = os.system('ping %s -c 1 >NULL' % address)

            if ping_result == 0:
                self.ping_counter_good += 1
                if self.time_good == datetime.timedelta(0):
                    self.time_good = datetime.datetime.now()  # Gong for Good time

                if self.time_bad != datetime.timedelta(0):
                    self.max_times[1] = max(self.max_times[1], (datetime.datetime.now() - self.time_bad))
                    self.time_bad = datetime.timedelta(0)
                    self.max_discon_label_var.set(str(self.max_times[1]).split('.')[0])  # print("Max",self.max_times)

                self.time_good_current = datetime.datetime.now() - self.time_good+self.add_time_good
                self.cur_con_var.set("Connected: " + str(self.time_good_current).split('.')[0])
                self.cur_con_label["foreground"] = 'green'

                if self.time_good_current > self.max_times[0]:
                    self.max_times[0] = self.time_good_current
                    self.max_con_label_var.set(str(self.max_times[0]).split('.')[0])

            else:
                self.ping_counter_bad += 1
                # if time is lo longer good
                if self.time_bad == datetime.timedelta(0):
                    self.time_bad = datetime.datetime.now()

                if self.time_good != datetime.timedelta(0):
                    self.max_times[0] = max(self.max_times[0], (datetime.datetime.now() - self.time_good))
                    self.time_good = datetime.timedelta(0)
                    self.max_con_label_var.set(str(self.max_times[0]).split('.')[0])

                self.time_bad_current = datetime.datetime.now() - self.time_bad+self.add_time_bad
                self.cur_con_var.set("DisConnected: " + str(self.time_bad_current).split('.')[0])
                self.cur_con_label["foreground"] = 'red'

                if self.time_bad_current > self.max_times[1]:
                    self.max_times[1] = self.time_bad_current
                    self.max_discon_label_var.set(str(self.max_times[1]).split('.')[0])

            if self.last_ping != ping_result:
                if ping_result == 0:
                    self.update_log("%s Reachable" % address)  # successful
                else:
                    self.update_log("%s not Reachable" % address)

            self.last_ping = ping_result

            self.update_ping_counter(color='green')
            self.root_id = root.after(2000, recur)

        if address == '':
            address = self.txtvar.get()
        if self.state == 0:
            self.now = datetime.datetime.now()
            self.butvar.set("Stop")
            self.update_log("Start pinging %s" % address)
            self.status_label.focus()
            recur()
            self.state = 1

        elif self.state == 1:
            self.add_elapsed_time = self.add_elapsed_time + (datetime.datetime.now() - self.now)
            # self.time_good ,self.time_bad= datetime.timedelta(0), datetime.timedelta(0)
            # self.add_time_good = self.time_good_current
            # self.add_time_bad = self.time_bad_current
            self.stop_ping()

    def stop_ping(self):
        self.butvar.set("Start")
        root.after_cancel(self.root_id)
        self.update_log("Stopped by User")
        self.update_ping_counter('red')
        self.state = 0

    def reset_callback(self):
        if self.state == 0:
            self.textbox1.delete(1.0, tk.END)
            self.reset_parameters()
            self.update_ping_counter()
            self.cur_con_var.set("")
            self.cur_con_label["foreground"] = 'black'
            self.max_con_label_var.set("")
            self.max_discon_label_var.set("")

    def update_ping_counter(self, color=''):
        self.ping_counter_var.set('Ping Counter (Total\Conn\DisConn) : %d\ %d\ %d' % (
            self.ping_counter_bad + self.ping_counter_good, self.ping_counter_good, self.ping_counter_bad))
        if color != '':
            self.ping_count_label['foreground'] = color
        else:
            self.ping_count_label['foreground'] = '#4c4c4c'


root = tk.Tk()
app = MainApp(root)
app.grid()
root.mainloop()
# from platform import system as system_name # Returns the system/OS name
# from os import system as system_call       # Execute a shell command
#
# def ping(host):
#     """
#     Returns True if host (str) responds to a ping request.
#     Remember that some hosts may not respond to a ping request even if the host name is valid.
#     """
#
#     # Ping parameters as function of OS
#     parameters = "-n 1" if system_name().lower()=="windows" else "-c 1"
#
#     # Pinging
#     return system_call("ping " + parameters + " " + host) == 0
#
# ping('127.0.0.1')
