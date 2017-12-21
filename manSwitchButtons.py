from tkinter import *
import tkinter.ttk

class dev_buttons2:
    
    def __init__(self, master, num_of_buttons):
        #Frame.__init__(self,master)
        self.master=master
        self.status=[]
        self.buts=[]
        self.leds=[]
        bg_window="DeepSkyBlue4"
        self.master.config(text="Switch Pannel",font=('Helvetica',12))
        self.framein=Frame(self.master)
        self.framein.grid(padx=20,pady=50)

        ##Create Widgets of buttons
        for i in range(num_of_buttons):
            button_var = StringVar()
            entry_var = IntVar()
            led_var = StringVar()
            t=35
            ent = Entry(self.framein,textvariable=entry_var,width=4,justify="center")
            ent.grid(column=i,row=2,sticky=W,padx=t)

            led = Label(self.framein,textvariable=led_var,width=4,bg="red",fg="white",relief="ridge")
            led_var.set("off")
            led.grid(row=0,column=i,pady=10)

            c = Checkbutton(self.framein,text="Switch "+ str(i), variable=button_var,indicatoron=0,
            width = 10,height=2,onvalue="on",offvalue="off",command=lambda arg=[i,button_var,entry_var]: self.cb(arg))
            c.grid(column=i, padx=30,pady=5,row = 1)
            button_var.set("off")

            mins = Label(self.framein,text="min.",width=4,justify="center",fg="black")#,bg=bg_window)
            mins.grid(column=i,row=2,sticky=E,padx=t)

            self.status.append([button_var,led_var,entry_var])
            self.buts.append(c)
            self.leds.append(led)
        ###
    
        
    def cb(self,but,state='',a=''):
        #but = [ switch#, switch state, delay] ## explanatory
        
        ##In use only in CB_DELAYED
        if state !='':
            but[1].set(state)
            
        def switch_on_off():
            if but[1].get()=="on":
                self.leds[but[0]].config(bg="green")
                self.status[but[0]][1].set("on")
            elif but[1].get()=="off":
                self.leds[but[0]].config(bg="red")
                self.status[but[0]][1].set("off")

        if but[2].get()>0 and but[1].get()=="on" :
            a=", Auto shutdown in %s minutes."%(but[2].get())
            switch_on_off()
            print("Delayed",but[1].get())
            self.cb_delayed(but)
        else :
            switch_on_off()   
        ##Update in accordance with Master
        #self.master.loop.device_chage_state(but[0],but[1].get(),text=a)
            
        print("Switch %d is %s"%(but[0],but[1].get()))
        
        ##
    def cb_delayed(self,but):
        self.framein.after(but[2].get()*1000 ,self.cb,but,"off")


#root=Tk()
#frame=LabelFrame(root)
#frame.grid(padx=10,pady=10)
#sample_switches=dev_buttons2(frame,8)
#root.mainloop()

