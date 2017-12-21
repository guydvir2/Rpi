import ButtonLib2
import tkinter as tk
from tkinter import ttk


#A=ButtonLib2.HWRemoteOutput(ip='192.168.2.114',output_pins=[5])
#print(A.get_state())
#A.set_state(0,1)
#print(A.get_state())
#A.set_state(0,0)
#print(A.get_state())
#A.close_device()
#print(A.get_state())


root = tk.Tk()
frame1= ttk.Frame(root)
frame1.grid()
But = ButtonLib2.ToggleButton(frame1,ip_out='192.168.2.114',hw_out=[5],sched_vector=[[[6], "08:37:30", "11:38:00"], [[2], "14:26:40", "22:03:10"]])
But.grid()
input("fgfgf")
But.close_all()

root.mainloop()
