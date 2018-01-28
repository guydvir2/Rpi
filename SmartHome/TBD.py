import tkinter as tk
import sys
import platform
print("Hello World!")

a=sys.path
for i in a:
    print(i)
A=[2,4,6,8,10]

for i,a in enumerate(A):
    if a%10 : A[i]=a%10
    if a == 2: A[i]='two'
print(A)
# print(platform.
print(sys.platform)

def make_button():
    tk.Button(frame1,text="But_"+str(butCounter)).grid()
    butCounter +=1

root = tk.Tk()
globals
butCounter = 0

frame1 = tk.Frame(root)
frame1.grid()
but1 = tk.Button(frame1,text="GUY",command=make_button)
but1.grid(row=0,column=0)

root.mainloop()
