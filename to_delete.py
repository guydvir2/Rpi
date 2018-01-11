# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 23:51:51 2018

@author: guy
"""

import tkinter as tk

def ck1_event(event,val):
    var1.set('Ck1 is:'+ str(val))
    v2.set(v1.get())

def ck2_event(event,val):
    var2.set('Ck1 is:'+ str(val))    
root = tk.Tk()

v1=tk.IntVar()
ck1=tk.Checkbutton(root,variable=v1)
ck1.grid(row=0, column=0)

var1=tk.StringVar()
var1.set('CK1')
lbl1=tk.Label(root, textvariable=var1)
lbl1.grid(row=0, column=1)
ck1.bind('<Button-1>',lambda event: ck1_event(event,val=v1.get()))

v2=tk.IntVar()
ck2=tk.Checkbutton(root, variable=v2)
ck2.grid(row=1, column=0)

var2=tk.StringVar()
var2.set('CK2')
lbl2=tk.Label(root, textvariable=var2)
lbl2.grid(row=1, column=1)

ck2.bind('<Button-1>',lambda event: ck2_event(event,val=v2.get()))
#ck2.bind('<Button-1>',lambda a=v2.get() :v1.set(a))




root.mainloop()