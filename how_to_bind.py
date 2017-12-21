#bind example
import tkinter as tk

def res(event):
    var.set('')

def restore(event):
    if var.get()=="":
        var.set(value0)    
    
root = tk.Tk()
var = tk.StringVar()
value0 = "ComeBack Here you chicken Shit!!!"
var.set(value0)
label = tk.Entry(root, textvariable=var)
label.bind("<Button-1>", res)
label.bind("<Leave>",restore)
label.grid()


root.mainloop()
