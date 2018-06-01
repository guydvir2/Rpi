from tkinter import *


class buttons(object):
    counter_buttons = 0

    def __init__(self, frame1, text1, fg1, cmd1, side1):
        self = Button(frame1, text=text1, fg=fg1, command=self.but_press)
        self.pack(side=side1)
        # counter_buttons +=1

    def but_press(self):
        # self.config(text="guy")
        print('GUY')


class buttons_press(object):
    def __init__(self, but1, text1, fg1):
        self.but1.config(text=text1, fg=fg1)


def act1(text1, fg1):
    but1.config(text1, fg1)


root = Tk()
root.title("Schedualer")
root.geometry("200x200")
frame1 = Frame(root)
frame1.pack()
but1 = buttons(frame1, "Device1\nOff", "red", "", "left")
but2 = buttons(frame1, "Device2\nOn", "red", '', "left")

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command='')
filemenu.add_command(label="Open...", command='')
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command='')

# action1=buttons_press(but1,"ON","green")

root.mainloop()
