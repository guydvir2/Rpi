from tkinter import *

class Java2sButton(Frame):
    def __init__(self):              
        Frame.__init__(self)
        self.pack()
        stopper = Button(self, text='Text', command=self.quit)
        stopper.pack()
        stopper.config(bg='navy', fg='white', bd=2) 

if __name__ == '__main__': 
    Java2sButton().mainloop()

from tkinter import *

root = Tk()
root.title('Buttons')
f = Frame(root, width=300, height=310)
xf = Frame(f, relief=GROOVE, borderwidth=1)
Label(xf, text="AAA").pack(pady=15)
Button(xf, text="bbb", state=DISABLED).pack(side=LEFT, padx=5, pady=8)
Button(xf, text="ccc rrr rrr rrr rrr", command=root.quit).pack(side=RIGHT, padx=5, pady=8)
xf.place(relx=0.01, rely=0.125, anchor=NW)
Label(f, text='Titled Border').place(relx=.06, rely=0.125,anchor=W)
f.pack()
root.mainloop()
