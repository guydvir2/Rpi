from tkinter import *

main=Tk()
main.geometry('500x100')
main.title(string='Test Diagram')

frame1=Frame(main)
frame1.pack(side = LEFT)

ent=Entry(frame1, width=5)
ent.pack(side = LEFT)
but1=Button(frame1, text='Button1',fg='blue')
but1.pack(side =  RIGHT)

but2=Button(frame1, text='Button2',fg='cyan')
but2.pack(side =  BOTTOM )
#text1=Label(frame1,text='guuuuuy',fg='darkgreen',bg='yellow', relief=RIDGE,width=30).pack(side = BOTTOM )
#text1.pack()
main.mainloop()
