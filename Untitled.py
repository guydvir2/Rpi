from tkinter import *
from tkinter import ttk

root = Tk()
ttkentry = ttk.Entry(root, justify='center')
ttkentry.insert(0, "my centered text")
ttkentry.pack()
ttkentry.configure()
# Partial output of ttkentry.configure()
#{'foreground': ('foreground', 'textColor', 'TextColor', '', ''),..., 'justify': ('justify', 'justify', 'Justify', <index object: 'left'>, 'left'),...,'validate': ('validate', 'validate', 'Validate', <index object: 'none'>, 'none')}

# After this command, note that the text is centered.
#ttkentry.configure(justify='center')
