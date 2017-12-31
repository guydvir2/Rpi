import subprocess
from gpiozero import OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import  pigpio
#from gpiozero.Factory import release_all

import os
import csv
import password_window
import tkinter as tk
from tkinter import ttk

class SSHfile:
  
    def __init__(self,adress,path,fname,usr,pwd):
        self.usr = usr
        self.pwd = pwd
        self.adress = adress
        self.path = path
        self.fname = fname
        self.local_file = self.path + self.fname + '_'+self.adress+'.csv'
        self.remote_file = self.path+self.fname+'.csv'
        #self.import_remote_file()
        
    def import_remote_file(self):
        cmd='sshpass -p %s scp -r %s@%s:%s %s'%(self.pwd, self.usr, self.adress, self.remote_file, self.local_file)
        try:
            subprocess.call(cmd, shell=True)
            print("file %s from %s retreived OK"%(self.remote_file, self.adress))
        except:
            print("failed to retreive %s from %s"%(self.remote_file, self.ad))
        
            
        #result = subprocess.run('scp {}'.format('guy@%s'%self.adress+':'+self.remote_file,self.local_file),shell=True)
        #print(result.check_returncode())

    def update_remote_file(self):
        cmd='sshpass -p %s scp -r %s %s@%s:%s '%(self.pwd, self.local_file, self.usr, self.adress, self.remote_file)
        try:
            subprocess.run(cmd, shell=True)
            print("file %s saved at %s OK"%(self.remote_file, self.adress))
        except:
            print("failed to save %s at %s"%(self.remote_file, self.ad))
        
        #result = subprocess.run(['scp',self.local_file, 'guy@%s'%self.adress+':'+self.remote_file])
        #result.check_returncode()
    
class PigpiodManager:
    class RunSUCommand:
        def __init__(self,pwd,cmd, usr=''):
            self.usr = usr
            self.pwd = pwd
            self.cmd = cmd

            self.run_cmd()
            
        def run_cmd(self):
            try:
                subprocess.call('echo {} | sudo -S {}'.format(self.pwd, self.cmd), shell=True)
            except:
                print("failed to execute command")


    def __init__(self, master, adress, local_ip, pwd):
        self.master = master
        self.adress = adress
        self.local_ip = local_ip
        self.pwd = pwd
        self.successful=[[],[]]
        
        self.load_pigpiod()

    def load_pigpiod(self):
        if self.local_ip == self.adress:
            if pigpio.pi(self.adress).connected == True:
                print('%s - is local, pigpiod already loaded'%self.adress)
                self.load_status = 0
                self.successful[0]=self.adress
            else:
                #subprocess.run(['sudo','pigpiod'])
                self.RunSUCommand(self.pwd,'pigpiod')
                try:
                    subprocess.check_output(["pidof","pigpiod"])
                    self.load_status = 0
                    print('%s - is local, pigpiod loaded - OK'%self.adress)
                    self.successful[0]=self.adress

                except:
                    subprocess.CalledProcessError
                    self.load_status = 1
                    print('%s - is local, pigpiod load - fail'%self.adress)
                    self.successful[1]=self.adress

                    

        else:#Remote machine
        #try:
            #subprocess.run(['ssh','-t','guy@'+self.adress,'sudo pigpiod && pgrep -x pigpiod'])
            if pigpio.pi(self.adress).connected:
                self.load_status = 0
                print('%s - is remote, pigpiod loaded - ok'%self.adress)
                self.successful[0]=self.adress

            else:
                try:
                    #subprocess.CalledProcessError
                    subprocess.check_output(['ssh','-t','guy@'+self.adress,'sudo pigpiod && pgrep -x pigpiod'])
                    self.load_status = False
                    print('%s is remote, pigpiod loaded - OK'%self.adress)
                    self.successful[0]=self.adress

                except subprocess.CalledProcessError:
                    print('%s is remote, pigpiod load - fail'%self.adress)
                    self.successful[1]=self.adress
                    self.load_status = 1

        self.master.pig_res = self.load_status

    def get_state(self):
        return self.successful



class LoadFile:
    
    def __init__(self, master=None, filename='', path='', titles=[], defaults=[], ip=''):
        self.master = master
        self.titles= titles
        self.defaults = defaults
        self.data_from_file = []
        self.filename = path + filename
        #self.frame = ttk.Frame(master)
        #self.frame.grid()
        self.load_file()


    def create_def_row(self, titles=''):
        
        self.mat = []
        titles = self.titles
        
        self.mat.append(titles)
        self.mat.append(self.defaults)
        self.data_from_file = self.mat
        print(self.mat)
        
        self.save_to_file(mat=self.mat)
                
        #print("File created")


    def save_to_file(self,filename='', mat=[]):  # save sched table to CSV file

        if filename == '' : filename = self.filename
        if mat ==[]: mat = self.data_from_file
        if not self.titles in mat: mat.insert(0, self.titles)
        outputfile = open(filename, 'w', newline="")
        outputwriter = csv.writer(outputfile)
        outputwriter.writerows(mat)
        outputfile.close()

        #self.load_file()

        print(filename,"saved")


    def load_file(self, file_in=''):

        if file_in == '': file_in=self.filename

        if os.path.isfile(file_in) == True:
            with open(file_in, 'r') as f:
                reader = csv.reader(f)
                self.data_from_file = list(reader)[1:]

        else :
            print('file',self.filename,' not found. default was created')
            self.create_def_row()
