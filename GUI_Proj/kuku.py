import tkinter as tk
from tkinter import ttk


# root = tk.Tk()
# t = tk.StringVar()
# t.set('guy_dvir')
# style = ttk.Style()
# style.configure('TEntry', font=('Helvetica', 18), foreground='green')
# ent1 = ttk.Entry(root, textvariable=t, width=200, justify=tk.CENTER,  font=('Helvetica', 18))
# ent1.grid()
# root.mainloop()

def get_index(item, list1):
    result_vector = []
    for i, l in enumerate(list1):
        if item == l:
            result_vector.append(i)
    return result_vector


list_a = [1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0]
print(get_index(1, list_a))
