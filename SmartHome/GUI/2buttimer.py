import tkinter as tk
import datetime
import time


class TwoButsTimer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.mainframe = tk.Frame(master, borderwidth=2, relief=tk.RIDGE)
        self.mainframe.grid()
        self.butframe = tk.Frame(self.mainframe, relief=tk.RIDGE)
        self.butframe.grid(row=0, column=0)
        self.labelframe = tk.Frame(self.mainframe, borderwidth=2, relief=tk.RIDGE)
        self.labelframe.grid(row=1, column=0, sticky=tk.E + tk.W)
        self.labelframe.grid_columnconfigure(0, weight=1)
        self.clockframe = tk.Frame(self.mainframe, borderwidth=2, relief=tk.RIDGE)
        self.clockframe.grid(row=2, column=0, sticky=tk.W + tk.E)
        self.clockframe.grid_columnconfigure(0, weight=1)

        self.on_off_state = False
        self.start_time, self.end_time, self.press_counter = None, None, 0
        self.but1, self.but2 = None, None
        self.label1, self.lb1_value = None, tk.StringVar()
        self.label2, self.lb2_value = None, tk.StringVar()
        self.label3, self.lb3_value = None, tk.StringVar()

        self.create_buttons()
        self.zeroing_variables()
        self.tick_clock()

    def create_buttons(self):
        px = 12
        py = 5
        self.but1 = tk.Button(self.butframe, text='On/Off', command=self.on_off_cb)
        self.but1.grid(row=0, column=0, padx=px, pady=py)

        self.but2 = tk.Button(self.butframe, text='Timer', command=self.timer_cb)
        self.but2.grid(row=0, column=1, padx=px, pady=py)

        self.label1 = tk.Label(self.labelframe, textvariable=self.lb1_value)
        self.label1.grid(row=0, column=0, sticky=tk.E + tk.W)
        self.lb1_value.set("Wait for 1st command")

        self.label2 = tk.Label(self.labelframe, textvariable=self.lb2_value)
        self.label2.grid(row=1, column=0, sticky=tk.E + tk.W)
        self.lb2_value.set("Wait for 1st command")

        self.label3 = tk.Label(self.clockframe, textvariable=self.lb3_value)
        self.label3.grid(row=0, column=0, sticky=tk.E + tk.W, columnspan=2)
        self.lb3_value.set("it's time")

    def zeroing_variables(self):
        self.press_counter = 0
        self.start_time, self.end_time = None, None
        self.on_off_state = False
        self.but1['bg'] = 'red'
        self.but2['bg'] = 'orange'
        self.lb1_value.set("Status: Off")
        self.lb2_value.set("End Time: Not Set")

    def on_off_cb(self):
        if self.on_off_state is False:
            self.on_off_state = True
            self.but1['bg'] = 'green'
            self.lb1_value.set("Status: On")
            self.lb2_value.set("On: %s" % (str(datetime.datetime.now())[:-7]))
            self.action_on()
        elif self.on_off_state is True:
            self.on_off_state = False
            self.but1['bg'] = 'red'
            self.action_off()

            self.zeroing_variables()

    @staticmethod
    def action_on():
        print("action_on")

    @staticmethod
    def action_off():
        print("action_off")

    def timer_cb(self):
        # cond to start timer:
        if self.on_off_state is True:
            self.but2['bg'] = 'green'
            self.lb1_value.set("Status: Timer")
            if self.press_counter == 0:
                self.start_time = datetime.datetime.now()
            self.press_counter += 1
            self.end_time = self.start_time + datetime.timedelta(seconds=10 * self.press_counter)
        else:
            self.lb2_value.set("Err: Switch On before Timer")
            #time.sleep(3)
            #self.zeroing_variables()

    def tick_clock(self):
        time_now = datetime.datetime.now()
        # Check timer
        if self.end_time is not None:
            if self.end_time > time_now:
                time_left = self.end_time - datetime.datetime.now()
                self.lb2_value.set('Left: %s' % (str(time_left)[:-7]))
            else:
                self.zeroing_variables()

        # Update clock label
        self.lb3_value.set(str(time_now)[:-7])
        self.after(500, self.tick_clock)


if __name__ == "__main__":
    root = tk.Tk()
    a = TwoButsTimer(root)
    root.mainloop()
