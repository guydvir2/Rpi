import  Adafruit_DHT
import lcddriver
import time
import subprocess
import datetime
from  tkinter import *


##### pinout scheme ####
#1. GND to GND
#2. VCC to 3v
#3. DATA to GPIO04

#class table (object):
    #def __init__(self,text1):
        #self.text1=text1


def clock():
    time = datetime.datetime.now().strftime("Date: %Y-%m-%d Time: %H:%M:%S")
    clock_lab.config(text=time)
    uptime=datetime.datetime.now()-start_time
    uptime_lab.config(text="Uptime :" + str(uptime.seconds))
    root.after(500, clock) # run itself again after 1000 ms

def center_str(text_in): ## centers string to fit LCD display
    text_out=" "*round((16-len(text_in))/2)+text_in
    return text_out

def cel_fr():  ## convert C to F
    global c2f
    if c2f==0 :
        but1.config(text=states[1],fg="Blue")
        c2f=1
    elif c2f==1:
        but1.config(text=states[0],fg='#4c4c4c')
        c2f=0
        
        
def ht_data():
    global t, h
    h0,t0 = Adafruit_DHT.read(11,4)
    if h0 and t0:
        if h0 < 100 and t0 < 100 :
            h=h0
            if c2f==0:
                t=t0
            elif c2f==1:
                t=32+1.8*t0
        temp_var.set("%d"%t)
        hum_var.set("%d%%"%h)
        display.lcd_display_string(center_str('Temp: %dC' %(t)), 1)
        display.lcd_display_string(center_str('Humidity: %d%s' %(h,"%")), 2)
    root.after(2000, ht_data)



## Init parameters
labels=['Temperature','Humidity']
states=["Celsius","Ferhaite"]
c2f=0
start_time=datetime.datetime.now()


### Create GUI wid
root=Tk()
root.title("Temp&Humid Sensor")
#root.geometry("300x300")
frame1=Frame(root)
frame1.grid(pady=10)

label1=Label(frame1,text="Temperature",relief= RIDGE,width=12,anchor=W)
label1.grid(row=0,column=0,sticky=E)
temp_var=StringVar()

ent1=Label(frame1,bg="white",textvariable=temp_var,relief= RIDGE,width =8)
ent1.grid(row=0, column=1,sticky=W)

label2=Label(frame1,text="Humidity",justify=LEFT,relief= RIDGE,width=12)
label2.grid(row=1,column=0,sticky=W)
hum_var=StringVar()

ent2=Label(frame1,bg="white",textvariable=hum_var,width=8,relief= RIDGE)
ent2.grid(row=1,column=1)


but1=Button(frame1,text="Celcius",command=cel_fr)
but1.grid(row=2,column=0,sticky=N,pady=5)


but2=Button(frame1,text="Quit!",command="Quit")
but2.grid(row=2,column=1,sticky=N,pady=5)

clock_lab = Label(root,relief=RIDGE)
clock_lab.grid(row=3, column=0)

uptime_lab = Label(root,relief=RIDGE)
uptime_lab.grid(row=4, column=0,rowspan=3)


########

##### Initialize LCD display ###
display = lcddriver.lcd()
display.lcd_clear()
display.lcd_display_string(center_str("Let's Start !!"), 1)
time.sleep (2)
display.lcd_clear()
##########


### Run ###
clock()
ht_data()

root.mainloop()


   




