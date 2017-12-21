from tkinter import *
def test(*args):
    for i in range(len(args)):
        print(i, str(args[i]))



vars1=["guy","dvir","anna",'Dvir','Shachar']

kw={"bg=":"blue"}
test("guy","dvir","guy","dvir","anna",'Dvir','Shachar')
print (kw.values())
root=Tk()
