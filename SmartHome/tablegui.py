import tkinter as tk
from tkinter import ttk
import readfile_ssh


class CoreTable(ttk.Frame):
    def __init__(self, master=None, data_filename=''):
        ttk.Frame.__init__(self, master=None)
        self.table_frame = ttk.Frame(self)
        self.table_frame.grid(row=0, column=0)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=0, column=1)
        self.data_mat, self.add_row_flag = [], 0
        self.data_from_file = readfile_ssh.LoadFile(filename=data_filename).data_from_file

        self.button_gui()
        self.restart_table()

    def button_gui(self):
        self.new_row = ttk.Button(self.button_frame, text='Add Row', width=8,
                                  command=self.add_row_cb)
        self.new_row.grid(row=0, column=0)

        self.del_row = ttk.Button(self.button_frame, text='Delete Row', width=8,
                                  command=self.fill_table)
        self.del_row.grid(row=1, column=0)

        self.clear_row = ttk.Button(self.button_frame, text='Clear Row', width=8,
                                    command=self.crash_table)
        self.clear_row.grid(row=2, column=0)

        self.save_table = ttk.Button(self.button_frame, text='Save', width=8,
                                     command=self.restart_table)
        self.save_table.grid(row=3, column=0)

    def add_row_cb(self):
        self.add_row_flag = 1
        self.crash_table()
        self.restart_table()

    def extract_data(self):
        self.data_mat = []
        for i, row in enumerate(self.vars_vector):
            self.data_mat.append([])
            for n, cell in enumerate(row):
                self.data_mat[-1].append(cell.get())

    def fill_table(self):
        self.data_mat = self.data_from_file
        rows = len(self.data_mat) + self.add_row_flag
        self.table_structure(rows)

        for i, row in enumerate(self.data_mat):
            for x, cell in enumerate(row):
                self.vars_vector[i][x].set(cell)

        self.add_row_flag = 0

    def crash_table(self):
        self.frame.destroy()

    def build_header(self):
        for i, header in enumerate(self.headers):
            ttk.Label(self.frame, text=header).grid(row=0, column=i)

    def restart_table(self):
        self.frame = ttk.LabelFrame(self.table_frame, text='Device Configuration')
        self.frame.grid(row=0, column=0)

        self.vars_vector = []

        self.build_header()
        self.fill_table()


class DeviceConfigGUI(CoreTable):
    def __init__(self, master=None, data_file_name=''):
        self.headers = ['ID#', 'Enabled', 'Type', 'Name', 'IP Address', 'I/O In', 'I/O Out']
        CoreTable.__init__(self, data_filename=data_file_name)

    def table_structure(self, rows):
        for i in range(1, rows + 1):
            self.v, c = [], 0

            # DeviceNumber
            self.v.append(tk.IntVar())
            self.v[c].set(i)
            a1 = ttk.Label(self.frame, textvariable=self.v[c])
            a1.grid(row=i, column=c)
            c += 1

            # Enabled
            self.v.append(tk.IntVar())
            # self.v[c].set(self.data_from_file[i - 1][c])
            a2 = ttk.Checkbutton(self.frame, variable=self.v[c])
            a2.grid(row=i, column=c)
            c += 1

            # Type
            self.v.append(tk.StringVar())
            # self.v[c].set(self.data_from_file[i - 1][c])
            a3 = ttk.Combobox(self.frame, textvariable=self.v[c], width=14,
                              values=list(['guy', 'Anna', 'Schar', 'Oz']),
                              state='readonly', justify=tk.CENTER)
            a3.grid(row=i, column=c)
            c += 1

            # Name
            self.v.append(tk.StringVar())
            # self.v[c].set(self.data_from_file[i - 1][c])
            a4 = ttk.Entry(self.frame, textvariable=self.v[c], width=13, justify=tk.CENTER)
            a4.grid(row=i, column=c)
            c += 1

            # IP
            self.v.append(tk.StringVar())
            # self.v[c].set(self.data_from_file[i - 1][c])
            a5 = ttk.Entry(self.frame, textvariable=self.v[c], width=14, justify=tk.CENTER)
            a5.grid(row=i, column=c)
            c += 1

            # GPIO IN
            self.v.append(tk.StringVar())
            # self.v[c].set(self.data_from_file[i - 1][c])
            a6 = ttk.Entry(self.frame, textvariable=self.v[c], width=7, justify=tk.CENTER)
            a6.grid(row=i, column=c)
            c += 1

            # GPIO OUT
            self.v.append(tk.StringVar())
            # self.v[c].set(self.data_from_file[i - 1][c])
            a7 = ttk.Entry(self.frame, textvariable=self.v[c], width=7, justify=tk.CENTER)
            a7.grid(row=i, column=c)
            c += 1

            self.vars_vector.append(self.v)



root = tk.Tk()
# a = CoreTable(root)
# a.grid()
# filename = '/Users/guy/Documents/gitHub/Rpi/SmartHome/ButtonsDef2.csv'
filename = 'd:/users/guydvir/Documents/git/Rpi/SmartHome/ButtonsDef2.csv'
b = DeviceConfigGUI(root, data_file_name=filename)
b.grid()
root.mainloop()
