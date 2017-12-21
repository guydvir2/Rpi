#import guizero
import time
from time import sleep
import ctypes
from tkinter import *
##################

def mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)


def time_stamp():
    x={'Time is: ': time.strftime("%H:%M:%S"), 'Date is: ': time.strftime("%d/%m/%Y")}
    #print('Date is: ', time.strftime("%d/%m/%Y"))
    return str(x)

time_stamp()
root=Tk()
#mbox('Pop-up Messages', time_stamp(),0)
count=0
ent=Entry(root)
ent.insert(0,"guy")
ent.pack()
var=StringVar()

while (count<100):
    label= ("Time is:", time.strftime("%H:%M:%S"),"Date is: ",time.strftime("%d/%m/%Y"))
    time.sleep(.1)
    count +=1
    print (label[0], label[1])
    var.set(label[0])

print ("\n\nrun", count, " times")
root.mainloop()