from tkinter import *

root=Tk()
root.title('IPcam Control Pane')
#root.geometry('800x200')
root.config()
root.resizable(0,0)

title1 = Label(root,text="IP Camera Display GUI",relief=RIDGE, bd=2)\
    .grid(row=0, columnspan=10)
frame1 = Frame(root,relief=RIDGE, bd=2, bg="lightgreen")\
    .grid(row=1, column=1, sticky=W)

label1=Label(frame1,text="Select Camera:",font=("Courier",10))
label1.grid(row=1, column=0, sticky=E)


cams=[('CAM 1', 1), ('CAM 2', 2), ('CAM 3', 3),
       ('CAM 4', 4), ('CAM 5', 5), ('CAM 6', 6),
      ('CAM 7', 7) ,('CAM 8', 8)]
var = IntVar()
for text, value in cams:
    Radiobutton(frame1, text=text, value=value, variable=var).\
        grid(row=2, column=value, sticky=W)#, indicatoron=0).\
    #Radiobutton(root, text=text, value=value, variable=var).pack(anchor=W)
var.set(1)

label2=Label(frame1,text="Buffer (ms):",font=("Courier",10)).\
    grid(row=3,column=0, columnspan=1, sticky=E)
ent1=Entry(frame1,width=10).grid(row=3,column=1,sticky=W)

label3=Label(frame1,text="Size [0-1]:",font=("Courier",10)).\
    grid(row=4,column=0, columnspan=1, sticky=E)
ent2=Entry(frame1,width=10).grid(row=4,column=1,sticky=W)







root.mainloop()