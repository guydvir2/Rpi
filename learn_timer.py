import time
import tkinter as tk
from tkinter import ttk
import datetime


########################
#######################

class LongPressButton(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.but_var = tk.StringVar()
        self.ent_var = tk.StringVar()
        self.lbl_var = tk.StringVar()
        self.on = False
        self.build_gui()
        self.restart()

    def restart(self):
        self.update_ent("Enter", 'blue')
        # time.sleep(8)
        print("restart")
        self.tic, self.toc = 0, 0
        self.on_off_status = 0
        self.but_var.set("Start")
        self.lbl_var.set('End time: ')

    def build_gui(self):
        self.style = ttk.Style()
        self.button = ttk.Button(self, textvariable=self.but_var, command=self.read_time)
        self.button.grid(row=0, column=1)
        self.button.bind('<Button-1>', self.press_but)
        self.button.bind('<ButtonRelease-1>', self.release_but)

        self.entry = ttk.Entry(self, textvariable=self.ent_var, justify=tk.CENTER, width=15)
        self.entry.bind('<Button-1>', self.clear_ent)
        self.entry.grid(row=0, column=0)

        self.label = ttk.Label(self, textvariable=self.lbl_var, relief=tk.RIDGE, anchor=tk.N)
        self.label.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)

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
            print('Valid time format')
            return b
        except ValueError:
            print("invalid time format")
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
                        self.update_ent("Wrong format", 'red')
                        time.sleep(2)
                        self.restart()

    def time_out(self, days=0, seconds=0):

        def update_clock():
            time_left = future - datetime.datetime.now()
            if time_left.total_seconds() > 0:
                time_str = str(time_left).split('.')[0]
                self.ent_var.set(time_str)
                self.on_off_status = 1

                self.a = self.after(500, update_clock)

            else:
                # self.update_ent('Count Over','blue')
                # time.sleep(3)
                self.on_off_status = 0
                self.succ_end()

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
        except AttributeError:
            pass
        self.on = False
        self.restart()


root = tk.Tk()
a = LongPressButton(root)
a.grid()
root.mainloop()
