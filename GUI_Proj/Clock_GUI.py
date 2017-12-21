from tkinter import *
import datetime

root = Tk()

lab = Label(root)
lab.pack()


def clock():
    time = datetime.datetime.now().strftime("Date: %Y-%m-%d Time: %H:%M:%S")
    lab.config(text=time)
    root.after(500, clock) # run itself again after 1000 ms

    
# run first time
clock()

root.mainloop()
