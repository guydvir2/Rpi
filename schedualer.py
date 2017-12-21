import datetime
import time
import gmailmod
import csv
from sys import platform
from time import sleep
from gpiozero import Buzzer
from gpiozero import LED
from tkinter import *
from tkinter import ttk
import os.path
import signal
import getip
import pigpio





class sched_entry:
    def __init__(self,master,r1,c1,offr,offc,bg1=["yellow"],text1=[],wid=[17],pdx1=[0],pdy1=[0]):
        self.status=[]
        self.configur=[]
        for r in range(r1):
            newrow=[]
            entry_row=[]
            for c in range(c1):
                v=StringVar()
                z=Entry(master,relief=FLAT,width=wid,bg=bg1,textvariable=v,justify='center')
                z.grid(row=r+offr, column=c+offc,padx=pdx1, pady=pdy1)
                newrow.append(v)
                v.set(text1)
                entry_row.append(z)
            self.status.append(newrow)
            self.configur.append(entry_row)

    def get_stat():
        return self.status

    def update (self,bg1,r1,c1,text1=[None],fg1=["#4c4c4c"]):
        self.status[r1][c1].set(text1)
        self.configur[r1][c1].config(bg=bg1,fg=fg1)


class dev_buttons2(object):
    def __init__(self,master,buts_list):
        self.status=[]
        self.buts=[]
        self.leds=[]
        for i in range(len(buts_list)):
            var = StringVar()

            var1=IntVar()
            ent=Entry(master,textvariable=var1,width=4,justify="center")
            ent.grid(column=i,row=2)

            var2=StringVar()
            led=Label(master,textvariable=var2,width=4,bg="red",fg="white",
            relief="ridge")
            var2.set("off")
            led.grid(row=0,column=i)

            c = Checkbutton(master,text=buts_list[i], variable=var,
            indicatoron=0,command=lambda arg=[buts_list[i],var,var1]: self.cb(master,arg),width=10,height=2,onvalue="on",offvalue="off")
            c.grid(column=i, padx=30,pady=5,row = 1)
            var.set("off")

            mins=Label(master,text="min.",width=4,justify="center",fg="white",
            bg=bg_window)
            mins.grid(column=i,row=2,sticky=E,padx=15)

            self.status.append([var,var2,var1])
            self.buts.append(c)
            self.leds.append(led)


    def cb(self,master,but):
        a=""
        indx=devices_headers.index(but[0])
        if but[2].get()>0 and but[1].get()=="on" :
            a=", Auto shutdown in %d minutes."%self.status[indx][2].get()
        device_chage_state(indx,but[1].get(),text=a)
        if but[2].get()>0 and but[1].get()=="on" :
            self.cb_delayed(master,but,but[2].get())




    def cb_delayed(self, master, but, delay_ms_var):
        but[1].set("off")
        master.after(but[2].get()*1000*60, self.cb, master,but)


#class sched_label(object):
    #def __init__(self,master,r1,c1,offr,offc,bg1=["yellow"],text1=[None],wid=[17]):
        #self.status=[]
        #self.configur=[]
        #for r in range(r1):
            #newrow=[]
            #label_row=[]
            #for c in range(c1):
                #v=StringVar()
                #v.set(text1)
                #z=Label(master,relief=FLAT,width=wid,
                #bg=bg1, textvariable=v,justify='center')
                #z.grid(row=r+offr, column=c+offc)
                #newrow.append(v)
                #label_row.append(z)

            #self.status.append(newrow)
            #self.configur.append(label_row)
    #def update (self,bg1,r1,c1,text1=[None],fg1=["#4c4c4c"]):
        #self.status[r1][c1].set(text1)
        #self.configur[r1][c1].config(bg=bg1,fg=fg1)


class rpi_relay(pigpio.pi):

    def __init__(self,ip_addr,gpio=[4,5,6,12]):
        pigpio.pi.__init__(self)
        self.GPIO=gpio
        self.rpi=pigpio.pi(ip_addr)
        for t in range(len(self.GPIO)):
            self.rpi.write(self.GPIO[t],0)

    def switch_state(self,i,state):
        self.rpi.write(self.GPIO[i],state)

    def read_state(self,i):
        self.rpi.write(self.GPIO[i],state)




def init_parameters():
    global devices, sched_headers ,days, tol,device_state, start_time,bg_window,devices_headers,ip,rpi_1,rpi_2
    sched_headers=["Task #","Enable/Disable","Days","Start Hour","End Hour","Device",'Next On/Off']
    days=[2,3,4,5,6,7,1]
    tol = 0.4 # 2*tol = time tolerance for executing / periodical check
    devices=["dev1","dev2","dev3","dev4"]
    device_state = ['off' for y in range(len(devices))]
    devices_headers=["Device"+str(i) for i in range(1,len(devices)+1)]
    bg_window="DeepSkyBlue4"
    start_time=datetime.datetime.now()
    ip=getip.get_ip()
    rpi_1=rpi_relay('192.168.2.113')
    #rpi_2=rpi_relay('192.168.2.112')


def save_csv(): # save sched table to CSV file
    file_out=sched_csv_file

    mat=[]
    mat.append(sched_headers)

    non_empty_cells=0
    for v in range(1,tasks_total+2):
        #print(sched_entries.status[v][0].get())
        if sched_entries.status[v][0].get() !="" :#or sched_entries.status[v][0].get() !='None' :
            #print(sched_entries.status[v][0].get())
            non_empty_cells +=1
        else:
            break
        #print(non_empty_cells)
    for r in range(1,non_empty_cells+1):
        newrow=[]
        for c in range(len(sched_headers)-1):
            if c==0:
                newrow.append(r)
            else:
                newrow.append(sched_entries.status[r][c].get())
        mat.append(newrow)
    outputfile=open(file_out,'w')
    outputwriter = csv.writer(outputfile)
    outputwriter.writerows(mat)
    outputfile.close()


def load_csv():
    global sch_file, tasks_total, continue_task, sched_csv_file

    if platform == 'linux':
        sched_csv_file = "/home/guy/PythonProjects/schedule.csv"
    elif platform == 'darwin':
        sched_csv_file = "~/PythonProjects/guy.csv"
    elif platform == 'win32':
        sched_csv_file = "d:\\guy.csv"

    sch_file=(read_csv(sched_csv_file))
    #print(sch_file)
    tasks_total=(len(sch_file))-1
    continue_task= ['on' for y in range(tasks_total)]
    print("[%s] %s loaded into memory"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    sched_csv_file))


def read_csv(file_in):

    if os.path.isfile(file_in) == True:                                 #Check if file exists
        with open(file_in, 'r') as f:
            reader = csv.reader(f)
            your_list = list(reader)
            return your_list
    else:
        file_out=sched_csv_file
        mat=[]
        mat.append(sched_headers)
        mat.append(["1","on",[6],"23:07:00","01:08:00","1"])
        outputfile=open(file_in,'w')
        outputwriter = csv.writer(outputfile)
        outputwriter.writerows(mat)
        outputfile.close()


def label_def_onoff(r,c,):
    sched_entries.update("lightgreen",r,6,"Wait for Task")


def device_chage_state(dev,stat,task="",text=[""]):
    task1=""
    #print(dev,stat,task)
    #print(type(task))
    def switch(stat):
        device_state[dev]=stat
        if stat=="on":
            color="green"
            rpi_2.switch_state(dev,1)
        elif stat=="off":
            color="red"
            rpi_2.switch_state(dev,0)
        buts.status[dev][1].set(stat)
        buts.leds[dev].config(bg=color)


    if mainsw_state.get()=="on" and stat != device_state[dev]:          #Mainswtich is ON
        switch(stat)                                                    # and change state
        if task !="" and buts.status[dev][0].get() == "off" :
            task1="task#"+str(int(task))
            if stat=="off": label_def_onoff(int(task)-1,0)

        if task =="":
            task1="Manual Switch"
            if text !="0":
                task1=task1+text
        print("[%s] %s, %s, %s"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        devices_headers[dev],stat,task1))


    if mainsw_state.get()=="off" and device_state[dev]== "on":         #MainSwitch shutdown
        task1="MainSwitch Shutdown"
        switch("off")
        buts.status[dev][0].set("off")

        print("[%s] %s, %s, %s"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        devices_headers[dev],stat,task1))


def create_GUI():
    global sched_entries,led_dev, timeouts_ents, root, buts,mainsw_state

    root=Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry("+0+%d"%(screen_height))
    root.configure(background=bg_window)
    root.title("Schedualer to Raspberry Pi")


    ### Week Schedule GUI ###

    sched_frame=LabelFrame(root,text="Weekly Schedule",padx=10,bg=bg_window,
    fg="white",font=("Helvetica",14))
    sched_frame.grid(row=0, column=0 , sticky=W, padx=20,pady=10)
    sched_entries=sched_entry(sched_frame,tasks_total+1+1,len(sched_headers),1,0) #Create Entries

    for r in range(tasks_total+1):   #update table with schdule.csv data
        for c in range (len(sched_headers)):
            if r== 0:
                sched_entries.update("lightgreen",r,c,sched_headers[c])
            if c == (len(sched_headers)-1) and r>0:
                sched_entries.update("lightgreen",r,c,"wait for Task")
            if c != (len(sched_headers)-1) and r!=0:
                sched_entries.status[r][c].set(sch_file[r][c])



    ##### Manual Pannel Buttons & LEDs
    frame_leds=LabelFrame(root, text="Manual Switch Pannel",bg=bg_window,
    fg="white",font=("Helvetica",14),padx=15,pady=15)
    frame_leds.grid(row=1, column=0 , padx=20, pady=10, sticky=W)
    buts=dev_buttons2(frame_leds,devices_headers)

    ##############


    #### create Exit, Reload, Save Buttons
    frame_mainbuttons=LabelFrame(root, text="Buttons",bg=bg_window,
    fg="white",font=("Helvetica",14),padx=35,pady=22)
    frame_mainbuttons.grid(row=1,column=0,padx=20,sticky=E)

    exit_but=Button(frame_mainbuttons,text="Exit",width=10, command=sys.exit)
    exit_but.grid(row=0, column=0, sticky=E,padx=1)

    reload_but=Button(frame_mainbuttons,text="Reload",command=load_csv,width=10)#,bg="")
    reload_but.grid(row=0,column=1,pady=5)


    save_but=Button(sched_frame,text="Save",command=save_csv,width=10,bg="lawn green")
    save_but.grid(row=tasks_total+3,column=6,pady=15)

    mainsw_txt=StringVar()
    mainsw_state=StringVar()

    def mainsw(stat=[]):

        if stat=="on":                                                  #for code switch
            mainsw_state.set("on")
        elif stat=="off":
            mainsw_state.set("off")

        if mainsw_state.get()=="on":                                    #execute when on
            mainsw_txt.set("MainSwitch ON")
            mainswitch.config(background="red", fg='#4c4c4c')
            for n in range(len(devices_headers)):
                buts.buts[n].config(state="active")

        if mainsw_state.get()=="off":                                   #execute when off
            mainsw_txt.set("MainSwitch OFF")
            mainswitch.config(background="red", fg="white")
            for n in range(len(devices_headers)):
                device_chage_state(n,"off")
                buts.buts[n].config(state="disabled")

    mainswitch=Checkbutton(frame_mainbuttons,textvariable=mainsw_txt,
    width=20, height=2,command=mainsw,onvalue="on",offvalue="off",indicatoron=0,variable=mainsw_state)
    mainswitch.grid(row=1, column=0,columnspan=2)
    mainsw("on")

    ############

    frame_statusbar=Frame(root)
    frame_statusbar.grid(sticky=S)

    def uptime(start):
        now=datetime.datetime.now()
        del_time=now-start
        hours=int(del_time.seconds/3600)
        minutes=int((del_time.seconds-hours*3600)/60)
        seconds=del_time.seconds-hours*3600-minutes*60
        return str('%d days, %02d:%02d:%02d'%(del_time.days, hours, minutes, seconds))


    def clock():
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clock_label.config(text=time+" Uptime: "+uptime(start_time)+" Local IP:%s , External IP:%s"%(ip)  )
        root.after(500, clock) # run itself again after 1000 ms

    clock_label=Label(frame_statusbar,relief="sunken")
    clock_label.grid(row=0,column=1,ipadx=root.winfo_width()/3)
    clock()
    root.update()


def schedule_loop():
    
    def time_diff(t1):
        t2 = datetime.datetime.now().time()
        today = datetime.date.today()
        return datetime.datetime.combine(today, t1)-datetime.datetime.combine(today, t2)

    
    def is_in(target,low_tol,high_tol,i):
        t=time_diff(datetime.datetime.strptime(target,"%H:%M:%S").time()).total_seconds()
        h=(int(abs(t)/3600))
        m=(int((abs(t)-h*3600)/60))
        s=(abs(t)-h*3600-m*60)
        t_left=0
        t_left=round(t)
        return ["%02d:%02d:%02d"%(h,m,s),(t_left)]



    now = datetime.datetime.now().time()                                ##update current loop time
    today= datetime.datetime.now().weekday()                            ##get day of week
    time_stamp= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")   ##time stamp str for log

    for i in range(1,tasks_total+1):                                     # is task off ?
        if sch_file[i][1]=="off":
            label_def_onoff(i,0)

        if str(days[today]) in sch_file[i][2] and "on" in sch_file[i][1]: #day of week & task enable
            isin_start=(is_in(sch_file[i][3],-tol,tol,i))
            isin_stop=(is_in(sch_file[i][4],-tol,tol,i))

            if isin_start[1] >0 :
                #print(i,"wait")                                           ##wait to ON
                sched_entries.update("red",i,6,"Off %s"%str(isin_start[0]),"white")
                continue_task[i-1] = 'on'

            if isin_stop[1] >0 and isin_start[1] < 0  :                 ## inside On interval
                if buts.status[int(sch_file [i][5])-1][0].get()=="on"  or  continue_task[i-1] == 'off':
                    label_def_onoff(i,0)
                    continue_task[i-1] = 'off'
                if buts.status[int(sch_file [i][5])-1][0].get() == "off" and continue_task[i-1] !="off":
                    sched_entries.update("green",i,6,"On (%s)"%str(isin_stop[0]),"white")
                    device_chage_state(int(sch_file [i][5])-1,"on",sch_file[i][0])
                    continue_task[i-1] = 'on'

            if isin_start[1] < 0 and isin_stop[1] <= 0  and isin_stop[1] >= -tol or mainsw_state.get()=="off":
                #print(i,"stop")
                device_chage_state(int(sch_file [i][5])-1,"off",sch_file[i][0])
                label_def_onoff(i,0)
                continue_task[i-1] = 'off'


    root.after(int(2*tol*1000),schedule_loop)


init_parameters()
load_csv()
create_GUI()
schedule_loop()
root.mainloop()



