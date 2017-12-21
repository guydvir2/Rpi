from tkinter import *
from time import sleep

# def update_clock():
#     x = time.strftime("%H:%M:%S")
#     entry1.delete(0, END)
#     entry1.insert(0, x)
#     entry1.pack()
colors=["blue","green","yellow"]
l=len(colors)
def shift_color():
    print("guy")

root = Tk()
root.title(string="BigBen")

frame = Frame(root, height=500, width=200)
frame.pack()

but1 = Button(frame, text='Press to Update',bg='blue',fg='yellow',command=shift_color())
but1.pack(side=LEFT)

txtvar=StringVar()
var_lab = Label(frame,bg='light green', justify=CENTER, width=10, height=1,textvariable=txtvar,relief=RAISED)

for x in range(0,5):
    txtvar.set(x)
    print(x)
    var_lab.pack()
    sleep(1)

root.mainloop()

#label1 = Label(frame, text=update_clock())
#label1.pack()



# while True:
#     update_clock()
#     frame.pack()
#     root.mainloop()




