from tkinter import *
root = Tk(  )
root.geometry('300x200')
Label(root,text="Select Cam to display",borderwidth=1,relief=SUNKEN,height=2).\
    grid(row=0 , column=0, sticky=N)
Frame(root,bg="green", width=150, height =100,relief=SUNKEN, bd=2).grid(row=0, column=1)
# tkinter.Label(root,text="HO baby!",borderwidth=1).grid(row=0 , column=1)
# tkinter.Label(root,text="HO baby!",borderwidth=1).grid(row=1 , column=1)
# tkinter.Label(root,text="HO baby!",borderwidth=1).grid(row=3 , column=2)
# tkinter.Label(root,text="1345634563456345634563456",borderwidth=1).grid(row=3 , column=3)
# for r in range(3):
#     for c in range(4):
#         tkinter.Label(root, text='R%s/C%s'%(r,c),
#             borderwidth=1 ).grid(row=r,column=c)
root.mainloop(  )