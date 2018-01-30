import tkinter as tk
from tkinter import ttk
import readfile_ssh


class CoreTable(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master=None)
        self.table_frame = ttk.Frame(self)
        self.table_frame.grid(row=0, column=0, padx=10)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=0, column=1)
        self.data_mat = []

        self.button_gui()

    def button_gui(self):
        self.new_row = ttk.Button(self.button_frame, text='Add Row', width=8,
                                  command=self.add_row_cb)
        self.new_row.grid(row=0, column=0)

        self.del_row = ttk.Button(self.button_frame, text='Delete Row', width=8,
                                  command=self.fill_table)
        self.del_row.grid(row=1, column=0)

        self.clear_row = ttk.Button(self.button_frame, text='Clear Row', width=8,
                                    command=self.add_row_cb)
        self.clear_row.grid(row=2, column=0)

        self.save_table = ttk.Button(self.button_frame, text='Save', width=8,
                                     command=self.add_row_cb)
        self.save_table.grid(row=3, column=0)

    def add_row_cb(self):
        print(len(self.vars_vector))
        pass

    def extract_data(self):
        self.data_mat = []
        for i, row in enumerate(self.vars_vector):
            self.data_mat.append([])
            for n, cell in enumerate(row):
                self.data_mat[-1].append(cell.get())

    def fill_table(self):
        print("SDSDS")
        for i, row in enumerate(self.data_mat):
            for x, cell in enumerate(row):
                # self.vars_vector[i][x].set(2)
                print(i,x)


class DeviceConfigGUI(CoreTable):
    def __init__(self, master=None, data_file_name='', rows=1):
        CoreTable.__init__(self)

        self.frame = ttk.LabelFrame(self.table_frame, text='Device Configuration')
        self.frame.grid()
        self.rows = rows
        self.vars_vector = []
        self.headers = ['ID#', 'Enabled', 'Type', 'Name', 'IP Address', 'I/O In', 'I/O Out']
        self.data_from_file = readfile_ssh.LoadFile(filename=data_file_name).data_from_file

        self.build_gui()

    def build_gui(self):
        for i, header in enumerate(self.headers):
            ttk.Label(self.frame, text=header).grid(row=0, column=i)

        for i in range(1, self.rows + 1):
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
            a5 = ttk.Entry(self.frame, textvariable=self.v[c], width=10, justify=tk.CENTER)
            a5.grid(row=i, column=c)
            c += 1

            # GPIO IN
            self.v.append(tk.StringVar())
            # self.v[c].set(self.data_from_file[i - 1][c])
            a6 = ttk.Entry(self.frame, textvariable=self.v[c], width=5, justify=tk.CENTER)
            a6.grid(row=i, column=c)
            c += 1

            # GPIO OUT
            self.v.append(tk.StringVar())
            # self.v[c].set(self.data_from_file[i - 1][c])
            a7 = ttk.Entry(self.frame, textvariable=self.v[c], width=5, justify=tk.CENTER)
            a7.grid(row=i, column=c)
            c += 1

            self.vars_vector.append(self.v)


root = tk.Tk()
# a = CoreTable(root)
# a.grid()
filename = '/Users/guy/Documents/gitHub/Rpi/SmartHome/ButtonsDef2.csv'
b = DeviceConfigGUI(root, rows=3, data_file_name=filename)
b.grid()
root.mainloop()
