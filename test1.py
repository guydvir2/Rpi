
from tkinter import *
import random

tiles_letter = ['a', 'b', 'c', 'd', 'e']

def add_letter():
    rand = random.choice(tiles_letter)
    tile_frame = Label(frame, text=rand)
    tile_frame.pack()
    root.after(500, add_letter)
    tiles_letter.remove(rand)  # remove that tile from list of tiles

root =Tk()
frame= Frame(root)
frame.pack()
#root.after(0, add_letter)  # add_letter will run as soon as the mainloop starts.
add_letter()
root.mainloop()
