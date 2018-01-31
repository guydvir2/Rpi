import tkinter as tk
from tkinter import ttk
import readfile_ssh


class CoreTable(ttk.Frame):
    def __init__(self, data_filename=''):
        ttk.Frame.__init__(self, master=None)

        self.style = ttk.Style()
        bg_color = 'slate gray'
        bg_color = 'gray31'
        # self.style.configure("bg.TButton", foreground='red')
        # self.style.configure("bg.TFrame", background=bg_color)
        # self.style.configure("bg.TButton", background=bg_color)
        # self.style.configure("bg.TEntry", background=bg_color)
        # self.style.configure("bg.TLabel", background=bg_color)
        # self.style.configure("bg_title.TLabel", background=bg_color, foreground='white')
        # self.style.configure("bg.TCheckbutton", background=bg_color)
        # print(self.style.theme_names())
        self.style.theme_use('clam')

        self.main_frame = ttk.Frame(self, style='bg.TFrame')
        self.main_frame.grid()

        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.grid(row=0, column=0)

        self.button_frame = ttk.Labelframe(self.main_frame)
        self.button_frame.grid(row=1, column=0, pady=1, sticky=tk.S)

        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.grid(row=2, column=0, columnspan=2, pady=5)

        self.data_mat, self.add_row_flag = [], 0
        self.filename = data_filename
        self.data_from_file = readfile_ssh.LoadFile(filename=self.filename).data_from_file

        self.button_gui()
        self.restart_table()
        self.status_bar()

    def button_gui(self):
        self.new_row = ttk.Button(self.button_frame, text='Add Row', width=8,
                                  command=self.add_row_cb, style='bg.TButton')
        self.new_row.grid(row=0, column=0)

        self.del_row = ttk.Button(self.button_frame, text='Delete Row', width=8,
                                  command=self.fill_table, style='bg.TButton')
        self.del_row.grid(row=0, column=1)

        self.save_table = ttk.Button(self.button_frame, text='Save', width=8,
                                     command=self.save_table, style='bg.TButton')
        self.save_table.grid(row=0, column=2)

    def add_row_cb(self):
        self.add_row_flag = 1
        self.crash_table()
        self.restart_table()

    def extract_data(self):
        self.data_mat = []
        for i, row in enumerate(self.vars_vector):
            self.data_mat.append([])
            for n, cell in enumerate(row):
                if n > 1 and cell.get() == '':
                    del self.data_mat[-1]
                    break
                else:
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
        self.table_frame.destroy()

    def build_header(self):
        for i, header in enumerate(self.headers):
            ttk.Label(self.table_frame, text=header, style='bg_title.TLabel').grid(row=0, column=i)

    def restart_table(self):
        self.table_frame = ttk.Frame(self.main_frame, style='bg.TFrame')
        self.table_frame.grid(row=0, column=0)

        self.vars_vector = []

        self.build_header()
        self.fill_table()

    def save_table(self):
        self.extract_data()
        readfile_ssh.LoadFile(filename=self.filename).save_to_file(mat=self.data_mat)

    def status_bar(self):
        ttk.Label(self.status_frame, text='filename: ' + str(self.filename), relief=tk.RIDGE,
                  style='bg.TLabel').grid()


class DeviceConfigGUI(CoreTable):
    def __init__(self, master, data_file_name=''):
        self.headers = ['ID#', 'Enabled', 'Type', 'Name', 'IP Address', 'I/O In', 'I/O Out']
        CoreTable.__init__(self, data_filename=data_file_name)

    def table_structure(self, rows):
        for i in range(1, rows + 1):
            self.v, c = [], 0

            # DeviceNumber
            self.v.append(tk.StringVar())
            self.v[c].set(i)
            a1 = ttk.Label(self.table_frame, textvariable=self.v[c], style='bg.TLabel')
            a1.grid(row=i, column=c)
            c += 1

            # Enabled
            self.v.append(tk.IntVar())
            a2 = ttk.Checkbutton(self.table_frame, variable=self.v[c], style='bg.TCheckbutton')
            a2.grid(row=i, column=c)
            c += 1

            # Type
            self.v.append(tk.StringVar())
            a3 = ttk.Combobox(self.table_frame, textvariable=self.v[c], width=14,
                              values=list(['guy', 'Anna', 'Schar', 'Oz']),
                              state='readonly', justify=tk.CENTER)
            a3.grid(row=i, column=c)
            c += 1

            # Name
            self.v.append(tk.StringVar())
            # self.v[c].set(self.data_from_file[i - 1][c])
            a4 = ttk.Entry(self.table_frame, textvariable=self.v[c], width=13, justify=tk.CENTER, style='bg.TEntry')
            a4.grid(row=i, column=c)
            c += 1

            # IP
            self.v.append(tk.StringVar())
            a5 = ttk.Entry(self.table_frame, textvariable=self.v[c], width=14, justify=tk.CENTER, style='bg.TEntry')
            a5.grid(row=i, column=c)
            c += 1

            # GPIO IN
            self.v.append(tk.StringVar())
            a6 = ttk.Entry(self.table_frame, textvariable=self.v[c], width=7, justify=tk.CENTER, style='bg.TEntry')
            a6.grid(row=i, column=c)
            c += 1

            # GPIO OUT
            self.v.append(tk.StringVar())
            a7 = ttk.Entry(self.table_frame, textvariable=self.v[c], width=7, justify=tk.CENTER, style='bg.TEntry')
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
