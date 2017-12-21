import tkinter
from tkinter import *
root = Tk()
root.title('GUI 1')
root.geometry('500x600')
frame1 = LabelFrame(root, bg='light green')
frame1.pack(side=BOTTOM)
but1 = Button(frame1, text='shit', fg="blue", bg='green')
but1.pack()



root.mainloop()
