from tkinter import *


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.write2text("@init GUI")
        self.function1("@init GUI in function 1")
        self.run1 = run_schedule(self)


    def function1(self, text1):
        self.master.write2text(text1)


class run_schedule:
    def __init__(self, master):
        self.master = master
        self.master.master.write2text("@init run_scdule")
        self.loop_runs("@init run_schdle, in loop_runs function")

    def loop_runs(self, text2):
        self.master.master.write2text(text2)



class App:
    def __init__(self, master):
        self.text = Text(master)
        self.text.grid()
        self.text.insert(END, "@init\n")
        self.write2text("@init using wrte2text method")
        self.gui1 = GUI(self)

    def write2text(self, text1):
        self.text.insert(END, text1 + "\n")



root = Tk()
app = App(root)
root.mainloop()
