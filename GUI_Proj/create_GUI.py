from tkinter import *
import random
import csv

root = Tk()

ff = "/home/guy/write.csv"
height = 5
width = 5

delta = 0

entries = []
textrow = []
mat = []


def save_me():
    for c in range(height):
        textrow = []
        for r in range(width):
            a = entries[c][r]
            textrow.append(a['text'])
        mat.append(textrow)
        # print(mat)
    print(mat)
    outputfile = open(ff, 'w')
    outputwriter = csv.writer(outputfile)  # , dialect='excel')
    outputwriter.writerows(mat)
    outputfile.close()


for i in range(height):  # Rows
    newrow = []
    for j in range(width):  # Columns
        b = Label(root, width=20, text=str(j))
        b.grid(row=i, column=j)
        newrow.append(b)
    entries.append(newrow)
colors = ["pink", "green", "red", "brown", "yellow"]
for r in range(height):
    for c in range(width):
        entries[r][c].config(font=("Helvetica", 10), bg="white")

but1 = Button(root, text="save&Quit", command=save_me)

but1.grid()

v = StringVar
ent1 = Entry(root, textvariable=v)


def ddd():
    s = ent1.get()
    print(s)


but2 = Button(root, text="print Entry", command=ddd)
but2.grid()
ent1.bind("<Button-1>", ddd)
ent1.grid()
mainloop()
