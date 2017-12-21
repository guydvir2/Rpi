#from tkinter import *
from subprocess import *

##
##master = Tk()
##
##Label(text="one").pack()
##
##separator = Frame(height=12, bd=5, relief=SUNKEN)
##separator.pack(fill=X, padx=5, pady=5)
##
##Label(text="two").pack()
##
##mainloop()

##check_output(["echo", "Hello World!"])
##a=run(["echo", "Hello World!"],shell=True)
##print(a.returncode)
###subprocess.getoutput

from subprocess import call
filename = input("What file would you like to display?\n")
call("cat " + filename, shell=True)
