# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 23:51:51 2018

@author: guy
"""

import tkinter as tk


def ck_cb(txt, v):
    v1.set(v)
    v2.set(v)
    print(txt + " pressed")


root = tk.Tk()

v1 = tk.BooleanVar()
txt1 = "CheckButton1"
ck1 = tk.Checkbutton(root, variable=v1, text=txt1, command=lambda: ck_cb(txt=txt1, v=v1.get()))
ck1.grid(row=0, column=0)

var1 = tk.StringVar()
var1.set('Not pressed')
lbl1 = tk.Label(root, textvariable=var1)
lbl1.grid(row=0, column=1)

v2 = tk.BooleanVar()
txt2 = "CheckButton2"
ck2 = tk.Checkbutton(root, variable=v2, text=txt2, command=lambda: ck_cb(txt=txt2, v=v2.get()))
ck2.grid(row=1, column=0)

var2 = tk.StringVar()
var2.set('Not pressed')
lbl2 = tk.Label(root, textvariable=var2)
lbl2.grid(row=1, column=1)


root.mainloop()
