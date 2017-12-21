import datetime
import time
#import gmailmod
import csv
from sys import platform
from time import sleep
from gpiozero import Buzzer
from gpiozero import LED
from tkinter import *
import tkinter.ttk

import readfile_ssh

import os.path
import signal
import getip
import pigpio
   


class schedule_GUI(Frame):
    
        
    class dev_buttons2:
        counter=0
        def __init__(self, master, frame1, buts_list):
            #Frame.__init__(self,master)
            #print("but",buts_list)
            self.frame1=frame1
            self.status=[]
            self.buts=[]
            self.leds=[]
            bg_window="DeepSkyBlue4"
            self.master=master

            ##Create Widgets of buttons
            for i in range(len(buts_list)):
                var = StringVar()
                var1=IntVar()
                
                ent=Entry(frame1,textvariable=var1,width=4,justify="center")
                ent.grid(column=i,row=2)

                var2=StringVar()
                led=Label(frame1,textvariable=var2,width=4,bg="red",fg="white",relief="ridge")
                var2.set("off")
                led.grid(row=0,column=i)

                c = Checkbutton(frame1,text="Switch "+ str(buts_list[i]), variable=var,
                indicatoron=0,width=10,height=2,onvalue="on",offvalue="off",command=lambda arg=[buts_list[i],var,var1]: self.cb(frame1,arg))
                c.grid(column=i, padx=30,pady=5,row = 1)
                var.set("off")

                mins=Label(frame1,text="min.",width=4,justify="center",fg="white",bg=bg_window)
                mins.grid(column=i,row=2,sticky=E,padx=15)

                self.status.append([var,var2,var1])
                self.buts.append(c)
                self.leds.append(led)
                #self.dev_buttons2.counter +=1
            ###

        def cb(self,frame1,but):
            #but = [ switch#, switch state, delay] ## explanatory
            a=""
            if but[2].get()>0 and but[1].get()=="on" :
                a=", Auto shutdown in %s minutes."%(but[2].get())
            self.master.loop.device_chage_state(but[0],but[1].get(),text=a)
            if but[2].get()>0 and but[1].get()=="on" :
                self.cb_delayed(frame1,but,but[2].get())

        def cb_delayed(self, frame1, but, delay_ms_var):
            but[1].set("off")
            frame1.after(but[2].get()*1000*60, self.cb, frame1,but)
            

    def save_csv(self): # save sched table to CSV file
        file_out=sched_csv_file

        mat=[]
        mat.append(self.headers)
        non_empty_cells=0
        for v in range(self.tasks_total):
            if self.row_vars[v][0].get() !="" :#or sched_entries.status[v][0].get() !='None' :
                non_empty_cells +=1
            else:
                break

        for r in range(non_empty_cells):
            newrow=[]
            for c in range(len(self.headers)-1):
                if c==0:
                    newrow.append(r)
                else:
                    #print("r=",r,"c=",c, self.row_vars[r][c].get())
                    newrow.append(self.row_vars[r][c].get())
            mat.append(newrow)
        outputfile=open(file_out,'w')
        outputwriter = csv.writer(outputfile)
        outputwriter.writerows(mat)
        outputfile.close()
        self.load_csv()
        self.loop.sch_file=self.sch_file

    def load_csv(self,file1):
        global continue_task, sched_csv_file

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


        if platform == 'linux':
            sched_csv_file = "/home/guy/PythonProjects/schedule.csv"
        elif platform == 'darwin':
            sched_csv_file = "~/PythonProjects/guy.csv"
        elif platform == 'win32':
            sched_csv_file = "d:\\guy.csv"

        self.sch_file=(read_csv(sched_csv_file))
        self.tasks_total=(len(self.sch_file))-1
        self.continue_task= ['on' for y in range(self.tasks_total)]
        print("[%s] %s loaded into memory"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        sched_csv_file))

    def __init__(self,master,switch=4):
        
        self.load_csv()        
        self.master = master

        style_ent=tkinter.ttk.Style()
        style_ent.configure('G.TEntry',foreground="blue",background=[("active", "black"), ("disabled", "red")],font=("Helvetica",20))
        
        style_frame=tkinter.ttk.Style()
        style_frame.configure('TLabelFrame',background=[("active", "black"),
        ("disabled", "red")],font=("Helvetica",12))
        
        sched_frame=tkinter.ttk.LabelFrame(master,text="Weekly Schedule")
        sched_frame.grid(row=0, column=0,pady=20, padx=20,ipadx=20, columnspan=1)
        switch_num=[num for num in range(switch)]
        dropdown_vals=[[],["on","off"],[],[],[],switch_num,[],[]]
        self.headers=["Task#","On/off","Days","Start","End","Switch","Next On/Off"]
        cell_w=[5,5,12,12,12,5,12]
        
        ## Create Table with initial Values
        self.row_vars=[]
        self.ents=[]
        for i in range(self.tasks_total):
            var1,var2,var3,var4,var5,var6,var7=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
            self.row_vars.append([var1,var2,var3,var4,var5,var6,var7])
            temp=[]

            ## Create Columns With Headers
            for t in range(len(self.headers)):
                l=tkinter.ttk.Label(sched_frame,text=self.headers[t],width=cell_w[t],
                anchor=CENTER)
                l.grid(row=0,column=t)
                
                if t==1 or t==5 :
                    onoff_comb=tkinter.ttk.Combobox(sched_frame,width=cell_w[t],
                    textvariable=self.row_vars[i][t], values=dropdown_vals[t],justify=CENTER)
                    onoff_comb.grid(row=i+1,column=t)
                    temp.append(onoff_comb)
                
                else :
                    task_ent=Entry(sched_frame,width=cell_w[t],
                    textvariable=self.row_vars[i][t],justify=CENTER,bg='white')#,style='G.TEntry'
                    task_ent.grid(row=i+1,column=t)
                    temp.append(task_ent)
                    
                if t<len(self.headers)-1:
                    self.row_vars[i][t].set(self.sch_file[i+1][t])
                else:
                    self.row_vars[i][t].set("Wait for Task") ## Column 7
                    
            self.ents.append(temp)
        ###
        
        ## Create SAVE Button
        save_button=tkinter.ttk.Button(sched_frame,text="Update", command=self.save_csv)
        save_button.grid(row=i+2, column=t,pady=5)
        ##

        ## Create Manual Buttons
        manualbut_frame=tkinter.ttk.LabelFrame(master,text="Manual Buttons")
        manualbut_frame.grid(row=1, column=0,padx=0)
        self.switch_button=self.dev_buttons2(self,manualbut_frame,switch_num)
        ##

        ## Create Main Buttons
        mainbut_frame=tkinter.ttk.LabelFrame(master,text="Main Buttons")
        mainbut_frame.grid(row=0, column=1,padx=10)

        self.exit_button=tkinter.ttk.Button(mainbut_frame,text="Exit",command=root.quit)
        self.exit_button.grid(row=0,column=1,pady=5,padx=5)
        ###

        ##Create MainSW
        self.mainsw_txt=StringVar()
        self.mainsw_state=StringVar()
        self.mainswitch = Checkbutton(mainbut_frame,textvariable=self.mainsw_txt,
        variable=self.mainsw_state, indicatoron=0,height=2,width=20,onvalue="on",offvalue="off",command=self.mainsw)
        self.mainswitch.grid(row=1,column=0,pady=5,padx=5, columnspan=2)
        self.mainsw_state.set("on")
        self.mainsw("on")
        print(self.mainswitch)
        ###

        ## Create  Task Bar
        self.statusbar_label=Label(root)
        self.statusbar_label.grid()
        self.update_statusbar()
        #schedule_GUI.GUIs_counter +=1

        ## Run Schedualer
        self.loop=run_schedule(self)

    ##Control MainSwitch
    def mainsw(self,stat=[]):
        #if self.loop.device_chage_state=="on":                           #for code switch
            #self.mainsw_state.set("on")
        #elif stat=="off":
            #self.mainsw_state.set("off")
            
        if self.mainsw_state.get()=="on":                               #execute when on
            self.mainsw_txt.set("MainSwitch ON")
            self.mainswitch.config(background="red", fg='#4c4c4c')
            for n in range(self.switch_button.counter):
                self.switch_button.buts[n].config(state="normal")

        if self.mainsw_state.get()=="off":                              #execute when off
            self.mainsw_txt.set("MainSwitch OFF")
            self.mainswitch.config(background="red", fg="white")
            for n in range(self.switch_button.counter):
                self.loop.device_chage_state(n,"off")
                self.switch_button.buts[n].config(state="disabled")
    ###

    ##Update Entries & Dropdown of Schedule
    def update(self,r,c,text,bg1='white',fg1='black'):
        self.row_vars[r][c].set(text)
        self.ents[r][c].config(fg=fg1,bg=bg1)
    ###

    #def update_statusbar(self):
        
        #def uptime(start):
            #now=datetime.datetime.now()
            #del_time=now-start
            #hours=int(del_time.seconds/3600)
            #minutes=int((del_time.seconds-hours*3600)/60)
            #seconds=del_time.seconds-hours*3600-minutes*60
            #return str('%d days, %02d:%02d:%02d'%(del_time.days, hours, minutes, seconds))
            
        #time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #self.statusbar_label.config(text=time+" Uptime: "+uptime(start_time)+" Local IP:%s , External IP:%s"%(ip))
        #root.after(500, self.update_statusbar) # run itself again after 1000 ms


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


class run_schedule():

    def __init__(self,master):
        self.master=master
        #self.sch_file=master.sch_file
        #self.continue_task=master.continue_task
        self.tasks_total=master.tasks_total
        
        ##Switch Off  all
        for n in range(master.switch_button.counter):
            self.device_chage_state(n,"off")
        self.loop()

    
    def time_diff(self,t1):
        t2 = datetime.datetime.now().time()
        today = datetime.date.today()
        return datetime.datetime.combine(today, t1)-datetime.datetime.combine(today, t2)

    ##Sched Loop _ Check if inside time interval
    def is_in(self,target,low_tol,high_tol,i):
        t=self.time_diff(datetime.datetime.strptime(target,"%H:%M:%S").time()).total_seconds()
        h=(int(abs(t)/3600))
        m=(int((abs(t)-h*3600)/60))
        s=(abs(t)-h*3600-m*60)
        t_left=0
        t_left=round(t)
        return ["%02d:%02d:%02d"%(h,m,s),(t_left)]


    def device_chage_state(self,dev,stat,task="",text=[""]):
        task1=""
        #print(dev,stat,task)

        ##Switch Functions
        def switch(stat):
            switches_flag[dev]=stat
            if stat=="on":
                color="green"
                rpi_1.switch_state(dev,1)
            elif stat=="off":
                color="red"
                rpi_1.switch_state(dev,0)
                
            ##Item to EXECUTE on switch 
            self.master.switch_button.status[dev][1].set(stat)
            self.master.switch_button.leds[dev].config(bg=color)
        ###

        #Mainswtich is ON and Switch stat changes due schedule
        #print(dev)
        if  stat != switches_flag[dev] and self.master.mainsw_state.get()=="on":  
            switch(stat)
            
            #Switch from Sched_loop                                                         
            if task !="" and self.master.switch_button.status[dev][0].get() == "off" :
                task1="task#"+str(int(task))

            ##Swtich caused by sofware button
            if task =="":
                task1="Manual Switch"
                if text !="0":task1=task1+text
                
            print("[%s] Switch%s, %s, %s"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            str(dev),stat,task1))
        ###
        
        #Shutdown process due to MainSw OFF
        if  switches_flag[dev]== "on" and self.master.mainsw_state.get()=="off" :
            task1="MainSwitch Shutdown"
            switch("off")
            self.master.switch_button.status[dev][0].set("off")
            print("[%s] %s, %s, %s"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            str(dev),stat,task1))
        ###

    ## Schedualer Engine   
    def loop(self):

        def label_def_onoff(r):
            self.master.update(r-1,6,"Wait for Task",'white','#4c4c4c')
        
        now = datetime.datetime.now().time()                            ##update  loop time
        today= datetime.datetime.now().weekday()                        ##get day of week
        time_stamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")##time stamp str f

        for i in range(1,self.tasks_total+1):                           # is task off ?
            if self.master.sch_file[i][1]=="off":
                label_def_onoff(i)

            if str(days[today]) in self.master.sch_file[i][2] and "on" in self.master.sch_file[i][1]: #day of week & task enable
                isin_start=self.is_in(self.master.sch_file[i][3],-tol,tol,i)
                isin_stop=(self.is_in(self.master.sch_file[i][4],-tol,tol,i))

                if isin_start[1] >0 :
                    #print(i,"wait")                                           ##wait to ON
                    self.master.update(i-1,6,"Off (%s)"%str(isin_start[0]),"white","red")
                    self.master.continue_task[i-1] = 'on'

                if isin_stop[1] >0 and isin_start[1] < 0  :                 ## inside On interval
                    if self.master.switch_button.status[int(self.master.sch_file [i][5])][0].get()=="on"  or  self.master.continue_task[i-1] == 'off':
                        label_def_onoff(i)
                        self.master.continue_task[i-1] = 'off'
                    if self.master.switch_button.status[int(self.master.sch_file [i][5])][0].get() == "off" and self.master.continue_task[i-1] !="off":
                        self.master.update(i-1,6,"On (%s)"%str(isin_stop[0]),"white","green")
                        self.device_chage_state(int(self.master.sch_file [i][5]),"on",self.master.sch_file[i][0])
                        self.master.continue_task[i-1] = 'on'
                        
                ##Stop Ending task or MainSwitch Shutdown
                if isin_start[1] < 0 and isin_stop[1] <= 0  and isin_stop[1] >= -2*tol or self.master.mainsw_state.get()=="off":
                    #print(i,"stop")
                    self.device_chage_state(int(self.master.sch_file [i][5]),"off",self.master.sch_file[i][0])
                    label_def_onoff(i)
                    self.master.continue_task[i-1] = 'off'
        root.after(int(2*tol*1000),self.loop)


class MainApp:
    def __init__(self,master,pis):
        #Frame.__init__(self,master)
        note=tkinter.ttk.Notebook(master)
        guis= ['gui'+str(i) for i in range(len(pis))]
        tabs = ['tab'+str(i) for i in range(len(pis))]
        for i in range(len(pis)):
            tabs[i] = tkinter.ttk.Frame(note)
            note.add(tabs[i], text = pis [i])
            note.grid()
            guis[i]=schedule_GUI(tabs[i])
        #print(guis)
        self.statusbar_label=Label(master)
        self.statusbar_label.grid()
        self.update_statusbar(master)
        
    def update_statusbar(self):
    
        def uptime(start):
            now=datetime.datetime.now()
            del_time=now-start
            hours=int(del_time.seconds/3600)
            minutes=int((del_time.seconds-hours*3600)/60)
            seconds=del_time.seconds-hours*3600-minutes*60
            return str('%d days, %02d:%02d:%02d'%(del_time.days, hours, minutes, seconds))
        
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.statusbar_label.config(text=time+" Uptime: "+uptime(start_time)+" Local IP:%s , External IP:%s"%(ip))
    root.after(500, self.update_statusbar) # run itself again after 1000 ms
        

def init_parameters():
    global days, tol, start_time,ip,rpi_1,rpi_2,num_switches,switches_flag,pis
    
    days=[2,3,4,5,6,7,1]
    num_switches=4
    tol = 0.4 # 2*tol = time tolerance for executing / periodical check
    switches_flag = ['off' for y in range(num_switches)]
    start_time=datetime.datetime.now()
    ip=getip.get_ip()
    pis=['192.168.2.112','192.168.2.113']


    #readfile_ssh.run_process('pigpiod')
    rpi_1=rpi_relay(pis[0])
    #rpi_2=rpi_relay(pis[1])
    #readfile_ssh.copyfile(pis[1],'/home/guy/PythonProjects/','schedule')




##Initialize GUI
init_parameters()


root=Tk()
root.title("Advanced Schedualer")

#note=tkinter.ttk.Notebook(root)
#tab1 = tkinter.ttk.Frame(note)
#tab2 = tkinter.ttk.Frame(note)

#note.add(tab1, text = pis[0], compound=TOP)
#note.add(tab2, text = pis[1])
#note.grid()


#App=MainApp(tab1)
App=MainApp(root,pis)

root.mainloop()
