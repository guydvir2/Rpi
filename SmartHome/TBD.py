# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 22:51:04 2017

@author: guy
"""

import ButtonLib2
import tkinter as tk
from tkinter import ttk


root=tk.Tk()
select_button='ToggleBut2'
a=getattr(ButtonLib2,select_button)(root, nickname='LivingRoom Lights', ip_out='192.168.2.113', \
        hw_out=[22,6],hw_in=[13],sched_vector=[[[4], "02:24:30", "23:12:10"], \
        [[2], "19:42:00", "23:50:10"]])
a.grid()
print(ButtonLib2.button_list)
root.mainloop()
