##from tkinter import *
##from tkinter.ttk import *
###mport tkinter
###import tkinter.ttk
##
##root=Tk()
##frame1=Frame(root)
##l1=Label(frame1,text="guy")
##l1.pack()
##root.mainloop()

##from tkinter import *
##
##master = Tk()
##
##w = Scale(master, from_=0, to=100)
##w.pack()
##
##w = Scale(master, from_=0, to=200, orient=HORIZONTAL)
##w.pack()
##
##mainloop()
###To query the widget, call the get method:
##
####w = Scale(master, from_=0, to=100)
####w.pack()
####
####print (w.get())

####from tkinter import *
##root = Tk()
##

##
### create a toplevel menu
### display the menu


from tkinter import *
from tkinter.ttk import *

def hello():
    print ("hello!")

root = Tk()
#scheduledimage=PhotoImage(...)

menubar = Menu(root)
menubar.add_command(label="Hello!", command=hello)
menubar.add_command(label="Quit!", command=root.quit)

note = Notebook(root)

tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
but=Button(tab1, text='Exit', command=root.destroy)
but.pack(padx=100, pady=100)
v5=StringVar()
ent1=Combobox(tab1,values=('On','Off'),textvariable=v5)
v5.set('On')
ent1.pack()


note.add(tab1, text = "Tab One", compound=BOTTOM)
note.add(tab2, text = "Tab Two")
note.add(tab3, text = "Tab Three")
note.pack()
root.config(menu=menubar)
root.mainloop()
exit()
