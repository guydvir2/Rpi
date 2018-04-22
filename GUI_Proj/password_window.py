import tkinter
from tkinter import ttk
import subprocess

import tkinter
from tkinter import ttk
import subprocess


class XWin:
    def __init__(self, master, exec_command,SF_name='', pwd=''):
        self.pwd = pwd
        self.bg = 'light slate gray'
        self.SF_name = SF_name
        self.master = master
        self.toplevel1 = tkinter.Toplevel(self.master, bg=self.bg)
        self.toplevel1.grid()
        self.exec_comm = exec_command
        self.dialog_run_gui(exec_command)
        style = ttk.Style()
        style.configure('.', background=self.bg)
        style.configure('bold.TLabel', foreground='white', font='Times 12 ')
        style.configure('header.TLabel', foreground='white', font='Times 14 underline')

    def dialog_run_gui(self, exec_command):
        ypad = 5
        self.shitme = tkinter.StringVar()
        if not self.pwd =='':
            self.shitme.set(self.pwd)

        def key_cb(event):
            self.exec_command()

        self.toplevel1.title(self.SF_name+"Enter Passsword")
        frame2 = ttk.Frame(self.toplevel1)
        frame2.grid(row=0, column=0, pady=ypad)

        header = ttk.Label(frame2, text="Confirm running Shell command", style='header.TLabel')
        header.grid()

        frame1 = ttk.Frame(self.toplevel1)
        frame1.grid(row=1, column=0, padx=10, pady=ypad)

        label1 = ttk.Label(frame1, text="program to execute: ")
        label1.grid(row=0, column=0, pady=ypad)

        label2 = ttk.Label(frame1, text=exec_command, style='bold.TLabel')  # , relief="ridge", padding=5)
        label2.grid(row=0, column=1, sticky=tkinter.W)

        label3 = ttk.Label(frame1, text="sudo's password: ")
        label3.grid(row=1, column=0, sticky=tkinter.E, pady=ypad)

        self.ent =ttk.Entry(frame1, width=30, textvariable=self.shitme, show="*")
        self.ent.grid(row=1, column=1)
        self.ent.bind("<Return>", key_cb)

        but_ok = ttk.Button(frame1, text="Continue", command=self.exec_command)
        but_ok.grid(row=2, column=1, sticky=tkinter.E, pady=ypad)

        but_cancel = ttk.Button(frame1, text="Cancel", command=self.toplevel1.quit)
        but_cancel.grid(row=2, column=1, sticky=tkinter.W)


    def exec_command(self):
        task = subprocess.call ("echo %s | sudo -S %s "%(self.ent.get(), self.exec_comm),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #output, error = task.communicate()
        #print(task)
        if task == 0:
            print("execute OK")
            self.toplevel1.destroy()
        else:
            self.msg_window('Wrong password, try again', 'Message')


    def msg_window(self,msg,title):
        ypad = 5
        width = '300'
        height = '80'

        frame = tkinter.Frame()
        self.toplevel2 = tkinter.Toplevel(frame, bg=self.bg)
        self.toplevel2.title(self.SF_name+ title)
        self.toplevel2.geometry('{}x{}'.format(width, height))

        frame = tkinter.Frame(self.toplevel2,bg = self.bg)
        frame.grid()

        text = ttk.Label(frame,text=msg)
        text.grid(pady= ypad, sticky=tkinter.W+tkinter.E)

        button = ttk.Button(frame,text="exit", command= self.toplevel2.destroy)
        button.grid(pady= ypad )

        frame.update()
        xcenter = int(width) / 2 - frame.winfo_width() / 2
        ycenter = int(height) / 2- frame.winfo_height() / 2
        frame.grid(row=0, column=1, pady=ycenter, padx=xcenter)
        


root = tkinter.Tk()
XWin(root, 'pigpiod', 'SchedualerPlus - ','kupelu9e')
root.mainloop()
