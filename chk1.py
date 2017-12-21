#import subprocess

#output = subprocess.check_output(['ls', '-1'])
#print ('Have %d bytes in output' % len(output))
#print (output)
#import  pigpio

#pi1 = pigpio.pi('192.168.2.113')
#pi2= pigpio.pi('192.168.2.112')
#print(pi1.connected,pi2.connected)
##if not pi1.connected:
   #print("Couldn't connect to daemon")
   #exit()
#if not pi2.connected:
   #print("Couldn't connect to daemon")
   #exit()


import tkinter
import password_window

root=tkinter.Tk()
password_window.XWin(root,'sudo pigpiod')
root.mainloop()
