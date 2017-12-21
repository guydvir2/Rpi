#import guizero
import time
import ctypes
from tkinter import *
##################

root = Tk()
root.title('Guy')
label_1 = Label (root, text="UserName")
label_1.grid(row=0, sticky=E)
label_2 = Label (root, text="Password")
label_2.grid(row=1, sticky=E)

entry_1 = Entry (root)
entry_1.grid(column=1, row=0)
entry_2 = Entry (root)
entry_2.grid(column=1, row=1)


ckbox = Checkbutton (root, text='Tick to keep me signed in')
ckbox.grid (columnspan = 2)


root.mainloop()
