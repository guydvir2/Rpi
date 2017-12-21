from tkinter import *
import subprocess

def run_cmd():
    valid_1=validity(v1.get(),7,1)
    valid_2=validity(v2.get(),1,0.01)
    valid_3=validity(v3.get(),20000,1000)
    print (valid_1, valid_2, valid_3)
    if (valid_1+valid_2+valid_3==0):
        subprocess.call(['play_ipcam.sh' ,str(v1.get()),str(v2.get()),str(v3.get())])
    elif valid_1 != 0:
        print ('Select no between 1-7 only')
    elif valid_2 != 0:
        print ('Window size beween 0.01-1 only')
    elif valid_3 != 0:
        print ('buffer size between 1,000-20,000')
            
def kill_cmd():
    subprocess.call(['killall' ,'vlc'])
    
def validity(val, upper_lim,lower_lim):
    if float(upper_lim)>float(lower_lim):
        if ( float(val) <=float(upper_lim) ) and ( float(val)>=float(lower_lim) ):
            return 0
        else:
            return 1
    else:
        return 2

def quit_cmd():
    kill_cmd()
    root.quit()

root=Tk()
#root.geometry('150x100')
root.title(string='IP Camera GUI')
frame1=Frame(root,bg='yellow').grid(row=0,column=0)

#def Vars
v1=StringVar()
v1.set('1')
v2=StringVar()
v2.set('0.4')
v3=StringVar()
v3.set('4000')
##########

text1=Label (frame1,text="select cam:").grid(row=0,column=0, sticky=NW)
ent1= Entry (frame1,width=5,bg='white', textvariable=v1).grid(row=0,column=1, sticky=NW)

text2=Label (frame1,text="windows size:").grid(row=1,column=0, sticky=NW)
ent2= Entry (frame1,width=5,bg='white', textvariable=v2).grid(row=1,column=1, sticky=NW)

text3=Label (frame1,text="buffer").grid(row=2,column=0, sticky=NW)
ent3= Entry (frame1,width=5,bg='white', textvariable=v3).grid(row=2,column=1, sticky=NW)


start_but=Button(frame1,text='Play',command=run_cmd).grid(row=3,sticky=W,columnspan=1)
stop_button=Button(frame1,text='Stop',fg='red',command=kill_cmd).grid(row=3,column=1,sticky=W,columnspan=1)
exit_button=Button(frame1,text='Exit',fg='Blue',command=quit_cmd).grid(row=3,column=2,sticky=W,columnspan=2)

root.mainloop()
